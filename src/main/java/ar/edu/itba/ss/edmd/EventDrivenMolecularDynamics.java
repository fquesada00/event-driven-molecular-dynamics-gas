package ar.edu.itba.ss.edmd;

import java.util.PriorityQueue;

public class EventDrivenMolecularDynamics {
    private final PriorityQueue<Event> eventQueue;
    private final Particle[] particles;
    private int particleCount;
    private double boxWidth;
    private double boxHeight;
    private double slitWidth;

    public EventDrivenMolecularDynamics(int particleCount, double boxWidth, double boxHeight, double slitWidth, double initialVelocity, double particlesMass) {
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
        this.particles = new Particle[particleCount];
        this.eventQueue = new PriorityQueue<>();
        initializeParticles(initialVelocity, particlesMass);
        calculateInitialEvents();
    }

    private void initializeParticles(double initialVelocity, double particlesMass) {
        //TODO: implement
    }

    private void calculateInitialEvents() {
        //TODO: implement
    }

    public void run() {
        //TODO: implement
    }

    private void calculateNextEvent(Particle a, Particle b) {
        //TODO: implement
    }


}
