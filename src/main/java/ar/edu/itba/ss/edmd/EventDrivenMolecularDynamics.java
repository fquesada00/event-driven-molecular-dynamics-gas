package ar.edu.itba.ss.edmd;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

import static ar.edu.itba.ss.edmd.EventType.*;

public class EventDrivenMolecularDynamics {
    private final PriorityQueue<Event> eventQueue;
    private final List<Particle> particles;
    private final int particleCount;
    private final double boxWidth;
    private final double boxHeight;
    private final double slitWidth;
    private final SimulationPrinter simulationPrinter;

    public EventDrivenMolecularDynamics(int particleCount, double boxWidth, double boxHeight, double slitWidth, double initialVelocity, double particlesMass, double particleRadius, String outputFileName) {
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
        this.particles = new ArrayList<>();
        this.eventQueue = new PriorityQueue<>();
        this.simulationPrinter = new SimulationPrinter(outputFileName, particleCount, boxWidth, boxHeight, slitWidth);
        initializeParticles(particleCount, initialVelocity, particlesMass, particleRadius);
        calculateInitialEvents();
    }

    private void initializeParticles(int particleCount, double initialVelocity, double particlesMass, double particleRadius) {
        Random random = new Random();
        for (int i = 0; i < particleCount; i++) {
            double x = random.nextDouble(particleRadius, boxWidth / 2 - particleRadius);
            double y = random.nextDouble(particleRadius, boxHeight - particleRadius);

            double velocityAngle = random.nextDouble() * 2 * Math.PI;
            double velocityX = initialVelocity * Math.cos(velocityAngle);
            double velocityY = initialVelocity * Math.sin(velocityAngle);
            Particle newParticle = new Particle(x, y, velocityX, velocityY, particleRadius, particlesMass);

            // Check if particle overlaps with any other
            boolean overlap = false;
            for (Particle p : particles) {
                if (newParticle.overlaps(p)) {
                    i--;
                    overlap = true;
                    break;
                }
            }

            if (!overlap) {
                particles.add(newParticle);
            }
        }
    }

    private void calculateInitialEvents() {
        for (Particle p1 : particles) {
            calculateNextParticleEvents(p1, 0);
        }
    }

    public void run() throws IOException {
        double fp = 1;
        double prevTime = 0;
        int steps = 0;

        simulationPrinter.printInitialParameters();

        while (fp >= 0.5) {
            simulationPrinter.printStep(particles, prevTime, true);

            steps++;
            Event nextEvent = eventQueue.poll();

            if (nextEvent == null) throw new RuntimeException("No events in the queue");

            if (!nextEvent.isValid()) continue;

            double newTime = nextEvent.getTime();

            updateParticlePositions(newTime - prevTime);


            switch (nextEvent.getEventType()) {
                case PARTICLES_COLLISION -> {
                    Particle p1 = nextEvent.getParticle1();
                    Particle p2 = nextEvent.getParticle2();
                    p1.bounce(p2);
                    calculateNextParticleEvents(p1, newTime);
                    calculateNextParticleEvents(p2, newTime);
                }
                case PARTICLE_X_WALL_COLLISION -> {
                    nextEvent.getParticle1().bounceX();
                    calculateNextParticleEvents(nextEvent.getParticle1(), newTime);
                }
                case PARTICLE_Y_WALL_COLLISION -> {
                    nextEvent.getParticle1().bounceY();
                    calculateNextParticleEvents(nextEvent.getParticle1(), newTime);
                }
            }
            prevTime = newTime;

            fp = calculateParticleFraction();
        }
        System.out.println(steps);
    }


    private void updateParticlePositions(double deltaT) {
        for (Particle p : particles) {
            p.updatePosition(deltaT);
        }
    }

    private double calculateParticleFraction() {
        int count = 0;
        for (Particle p : particles) {
            if (p.x() < boxWidth / 2) {
                count++;
            }
        }
        return (double) count / particleCount;
    }

    private void calculateNextParticleEvents(Particle p, double offsetTime) {
        calculateNextParticlesCollisionEvents(p, offsetTime);
        calculateNextParticleWallCollisionEvents(p, offsetTime);
    }

    private void calculateNextParticleWallCollisionEvents(Particle particle, double offsetTime) {
        double collidesXTime = particle.collidesX(this.boxHeight) + offsetTime;
        double collidesYTime = particle.collidesY(this.boxWidth, this.boxHeight, this.slitWidth) + offsetTime;

        if (collidesXTime < collidesYTime) {
            eventQueue.add(new Event(collidesXTime, particle, null, PARTICLE_X_WALL_COLLISION));
        } else if(collidesYTime != Double.POSITIVE_INFINITY) {
            eventQueue.add(new Event(collidesYTime, particle, null, PARTICLE_Y_WALL_COLLISION));
        }

    }

    private void calculateNextParticlesCollisionEvents(Particle particle, double offsetTime) {
        for (Particle p : particles) {
            if (p == particle) continue;
            Event particlesCollision = calculateNextParticlesCollisionEvent(particle, p, offsetTime);
            if (particlesCollision != null) {
                eventQueue.add(particlesCollision);
            }
        }
    }

    private Event calculateNextParticlesCollisionEvent(Particle a, Particle b, double offsetTime) {
        double collisionTime = a.collides(b) + offsetTime;
        if (collisionTime != Double.POSITIVE_INFINITY && collisionTime >= 0) {
            return new Event(collisionTime, a, b, PARTICLES_COLLISION);
        }
        return null;
    }


}
