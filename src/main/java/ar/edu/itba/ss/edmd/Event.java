package ar.edu.itba.ss.edmd;

public class Event implements Comparable<Event>{
    private double t;
    private EventParticle a;
    private EventParticle b;
    private final int aCollisionCount;
    private final int bCollisionCount;

    public Event(double t, EventParticle a, EventParticle b) {
        this.t = t;
        this.a = a;
        this.b = b;

        this.aCollisionCount = a == null ? 0 : a.getCollisionCount();
        this.bCollisionCount = b == null ? 0 :b.getCollisionCount();
    }

    public double getTime() {
        return this.t;
    }

    public EventParticle getParticle1() {
        return this.a;
    }

    public EventParticle getParticle2() {
        return this.b;
    }

    public boolean isValid(){
        return  (a == null || a.getCollisionCount() == aCollisionCount) && (b == null || b.getCollisionCount() == bCollisionCount);
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(this.t,o.t);
    }
}
