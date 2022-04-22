package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.FixedObstacle;
import ar.edu.itba.ss.edmd.Particle;

import java.util.List;

public class ParticleFixedObstacleCollisionEvent extends Event {

    private final Particle particle;
    private final FixedObstacle obstacle;

    private final int particleCollisionCount;

    public ParticleFixedObstacleCollisionEvent(double time, Particle particle, FixedObstacle obstacle) {
        super(time);
        this.particle = particle;
        this.obstacle = obstacle;
        this.particleCollisionCount = particle.collisionCount();
    }

    public Particle getParticle() {
        return particle;
    }

    @Override
    public boolean isValid() {
        return (particle.collisionCount() == particleCollisionCount);
    }

    @Override
    public List<Event> execute(List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        this.particle.bounceFixedObstacle(this.obstacle);
        return super.calculateNextParticleEvents(this.particle, particles, obstacles, boxWidth, boxHeight, slitWidth);
    }

    @Override
    public char getEventType(Particle p) {
        return p.equals(this.particle) ? 'f' : '-';
    }
}
