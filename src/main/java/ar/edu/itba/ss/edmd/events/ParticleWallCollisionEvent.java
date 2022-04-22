package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.Particle;

public abstract class ParticleWallCollisionEvent extends Event {

    protected final Particle particle;
    private final int particleCollisionCount;

    public ParticleWallCollisionEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
        particleCollisionCount = particle.collisionCount();
    }


    public Particle getParticle() {
        return particle;
    }

    @Override
    public boolean isValid() {
        return (particle.collisionCount() == particleCollisionCount);
    }
}
