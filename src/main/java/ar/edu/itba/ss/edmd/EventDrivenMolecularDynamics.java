package ar.edu.itba.ss.edmd;

import java.util.PriorityQueue;

public class EventDrivenMolecularDynamics {
    private int N;
    private double W;
    private double H;
    private double D;

    private PriorityQueue<Event> events;

    private EventParticle[] particles;

    public EventDrivenMolecularDynamics(int N, double W, double H, double D,double initialVelocity,double particlesMass) {
        this.N = N;
        this.W = W;
        this.H = H;
        this.D = D;
        this.particles = new EventParticle[N];
        this.events = new PriorityQueue<>();
        initializeParticles(initialVelocity,particlesMass);
        calculateInitialEvents();
    }

    private void initializeParticles(double initialVelocity,double particlesMass) {
        //TODO: implement
    }

    private void calculateInitialEvents() {
        //TODO: implement
    }

    public void run() {
        //TODO: implement
    }

    private void calculateNextEvent(EventParticle a, EventParticle b) {
        //TODO: implement
    }


}
