package ar.edu.itba.ss.edmd;

import ar.edu.itba.ss.edmd.events.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public class EventDrivenMolecularDynamics {
    private final PriorityQueue<Event> eventQueue;
    private final List<Particle> particles;
    private final List<FixedObstacle> fixedObstacles;
    private final int particleCount;
    private final double boxWidth;
    private final double boxHeight;
    private final double slitWidth;
    private final SimulationPrinter simulationPrinter;
    private final double threshold;

    private final double equilibriumTime;

    public EventDrivenMolecularDynamics(int particleCount, double boxWidth, double boxHeight, double slitWidth, double initialVelocity, double particlesMass, double particleRadius, double threshold, double equilibriumTime, String staticOutputFileName, String dynamicOutputFileName, String summaryFileName) {
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
        this.particles = new ArrayList<>();
        this.fixedObstacles = new ArrayList<>();
        this.eventQueue = new PriorityQueue<>();
        this.threshold = threshold;
        this.equilibriumTime = equilibriumTime;
        this.simulationPrinter = new SimulationPrinter(staticOutputFileName, dynamicOutputFileName, summaryFileName, particleCount, boxWidth, boxHeight, slitWidth, particlesMass, particleRadius);
        initializeParticles(particleCount, initialVelocity, particlesMass, particleRadius);
        initializeFixedObstacles();
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

    private void initializeFixedObstacles() {
        FixedObstacle topSlitVertex = new FixedObstacle(boxWidth / 2, (boxHeight + slitWidth) / 2, 0.000001);
        FixedObstacle bottomSlitVertex = new FixedObstacle(boxWidth / 2, (boxHeight - slitWidth) / 2, 0.000001);

        fixedObstacles.add(topSlitVertex);
        fixedObstacles.add(bottomSlitVertex);
    }

    private void calculateInitialEvents() {
        for (Particle p1 : particles) {
            eventQueue.addAll(new InitializeParticleEvent(0, p1).execute(particles, fixedObstacles, boxWidth, boxHeight, slitWidth));
        }
    }

    public void run(boolean debug) throws IOException {
        double fp = 1;
        double prevTime = 0;
        int eventCount = 0;

        long startExecTime = System.currentTimeMillis();

        simulationPrinter.printStaticParameters();
        Timer timer = null;


        while (true) {

            Event nextEvent = eventQueue.poll();

            if (nextEvent == null) throw new RuntimeException("No events in the queue");

            if (!nextEvent.isValid()) continue;

            if (nextEvent.finished()){
                if (debug) {
                    System.out.println("Simulation finished after " + eventCount + " events and " + prevTime + " simulation seconds with fp = " + fp);
                    System.out.println("Remaining events: " + eventQueue.size());
                }
                break;
            }

            simulationPrinter.printStep(particles, nextEvent, prevTime, eventCount != 0, eventCount == 0);

            eventCount++;

            double newTime = nextEvent.getTime();

            if (fp < 0.5 + threshold && fp > 0.5 - threshold && timer == null) {
                if (debug) {
                    System.out.println("Timer set at " + newTime + " with fp = " + fp);
                }
                timer = new Timer();
                eventQueue.add(new TimerEvent(newTime + this.equilibriumTime,timer));
            }


            updateParticlePositions(newTime - prevTime);

            eventQueue.addAll(nextEvent.execute(particles, fixedObstacles, boxWidth, boxHeight, slitWidth));

            prevTime = newTime;

            fp = calculateParticleFraction();
        }

        long endExecTime = System.currentTimeMillis();
        long simulationExecTime = endExecTime - startExecTime;

        simulationPrinter.printSummary(simulationExecTime, prevTime, eventCount, fp);
        System.out.println(eventCount);
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


}
