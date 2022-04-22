package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.FixedObstacle;
import ar.edu.itba.ss.edmd.Particle;

import java.util.ArrayList;
import java.util.List;

public abstract class Event implements Comparable<Event> {
    private final double time;

    public Event(double time) {
        this.time = time;
    }

    public double getTime() {
        return this.time;
    }

    public boolean isValid() {
        return false;
    }

    public List<Event> execute(List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        throw new UnsupportedOperationException();
    }

    public char getEventType(Particle p) {
        return '-';
    }

    protected List<Event> calculateNextParticleEvents(Particle p, List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        List<Event> events = new ArrayList<>();
        events.addAll(calculateNextParticlesCollisionEvents(p, particles));
        events.addAll(calculateNextParticleWallCollisionEvents(p, boxWidth, boxHeight, slitWidth));
        events.addAll(calculateNextFixedObstacleCollisionEvents(p, obstacles));
        return events;
    }

    private List<Event> calculateNextFixedObstacleCollisionEvents(Particle p, List<FixedObstacle> obstacles) {
        List<Event> events = new ArrayList<>();
        for (FixedObstacle obstacle : obstacles) {
            double collisionTime = p.collides(obstacle) + time;

            if (collisionTime != Double.POSITIVE_INFINITY && collisionTime >= 0) {
                events.add(new ParticleFixedObstacleCollisionEvent(collisionTime, p, obstacle));
            }
        }
        return events;
    }

    private List<Event> calculateNextParticleWallCollisionEvents(Particle particle, double boxWidth, double boxHeight, double slitWidth) {
        List<Event> events = new ArrayList<>();
        double collidesXTime = particle.collidesX(boxHeight) + time;
        double collidesYTime = particle.collidesY(boxWidth, boxHeight, slitWidth) + time;

        if (collidesXTime < collidesYTime) {
            events.add(new ParticleXWallCollisionEvent(collidesXTime, particle));
        } else if (collidesYTime != Double.POSITIVE_INFINITY) {
            events.add(new ParticleYWallCollisionEvent(collidesYTime, particle));
        }
        return events;
    }

    private List<Event> calculateNextParticlesCollisionEvents(Particle particle, List<Particle> particles) {
        List<Event> events = new ArrayList<>();
        for (Particle p : particles) {
            if (p == particle) continue;
            Event particlesCollision = calculateNextParticlesCollisionEvent(particle, p);
            if (particlesCollision != null) {
                events.add(particlesCollision);
            }
        }
        return events;
    }

    private Event calculateNextParticlesCollisionEvent(Particle a, Particle b) {
        double collisionTime = a.collides(b) + time;
        if (collisionTime != Double.POSITIVE_INFINITY && collisionTime >= 0) {
            return new ParticlesCollisionEvent(collisionTime, a, b);
        }
        return null;
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(this.time, o.time);
    }


}
