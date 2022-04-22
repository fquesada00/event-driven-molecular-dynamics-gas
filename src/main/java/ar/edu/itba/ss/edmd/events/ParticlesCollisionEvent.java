package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.FixedObstacle;
import ar.edu.itba.ss.edmd.Particle;

import java.util.ArrayList;
import java.util.List;

public class ParticlesCollisionEvent extends Event {

    private final Particle particle1;
    private final Particle particle2;

    private final int particle1CollisionCount;
    private final int particle2CollisionCount;

    public ParticlesCollisionEvent(double time, Particle particle1, Particle particle2) {
        super(time);
        if (particle1 == null || particle2 == null) {
            throw new IllegalArgumentException("Particles cannot be null");
        }
        this.particle1 = particle1;
        this.particle2 = particle2;
        this.particle1CollisionCount = particle1.collisionCount();
        this.particle2CollisionCount = particle2.collisionCount();

    }

    @Override
    public List<Event> execute(List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        particle1.bounce(particle2);
        List<Event> events = new ArrayList<>(2);
        events.addAll(super.calculateNextParticleEvents(particle1, particles, obstacles, boxWidth, boxHeight, slitWidth));
        events.addAll(super.calculateNextParticleEvents(particle2, particles, obstacles, boxWidth, boxHeight, slitWidth));
        return events;
    }

    @Override
    public boolean isValid() {
        return (particle1.collisionCount() == particle1CollisionCount) && (particle2.collisionCount() == particle2CollisionCount);
    }

    @Override
    public char getEventType(Particle p) {
        return this.particle1.equals(p) || this.particle2.equals(p) ? 'p' : '-';
    }
}
