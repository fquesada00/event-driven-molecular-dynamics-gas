package ar.edu.itba.ss.edmd;

public class Event implements Comparable<Event> {
    private final double time;
    private final Particle particle1;
    private final Particle particle2;
    private final int particle1CollisionCount;
    private final int particle2CollisionCount;

    public Event(double time, Particle particle1, Particle particle2) {
        this.time = time;
        this.particle1 = particle1;
        this.particle2 = particle2;

        this.particle1CollisionCount = particle1 == null ? 0 : particle1.getCollisionCount();
        this.particle2CollisionCount = particle2 == null ? 0 : particle2.getCollisionCount();
    }

    public double getTime() {
        return this.time;
    }

    public Particle getParticle1() {
        return this.particle1;
    }

    public Particle getParticle2() {
        return this.particle2;
    }

    public boolean isValid() {
        return (particle1 == null || particle1.getCollisionCount() == particle1CollisionCount) && (particle2 == null || particle2.getCollisionCount() == particle2CollisionCount);
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(this.time, o.time);
    }
}
