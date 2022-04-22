package ar.edu.itba.ss.edmd.events;

import ar.edu.itba.ss.edmd.FixedObstacle;
import ar.edu.itba.ss.edmd.Particle;

import java.util.List;

public class InitializeParticleEvent extends Event {
    private final Particle particle;

    public InitializeParticleEvent(double time, Particle particle) {
        super(time);
        this.particle = particle;
    }

    @Override
    public List<Event> execute(List<Particle> particles, List<FixedObstacle> obstacles, double boxWidth, double boxHeight, double slitWidth) {
        return super.calculateNextParticleEvents(this.particle, particles, obstacles, boxWidth, boxHeight, slitWidth);
    }

    @Override
    public boolean isValid() {
        return true;
    }
}
