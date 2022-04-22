package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.FixedObstacle;
import ar.edu.itba.ss.edmd.Particle;

import java.util.List;

public class ParticleYWallCollisionEvent extends ParticleWallCollisionEvent {
    public ParticleYWallCollisionEvent(double time, Particle particle) {
        super(time, particle);
    }

    @Override
    public List<Event> execute(List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        this.particle.bounceY();
        return super.calculateNextParticleEvents(this.particle, particles, obstacles, boxWidth, boxHeight, slitWidth);
    }

    @Override
    public char getEventType(Particle p) {
        return p.equals(particle) ? 'y' : '-';
    }
}
