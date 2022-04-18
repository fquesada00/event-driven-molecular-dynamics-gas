package ar.edu.itba.ss.edmd;

public class Event implements Comparable<Event> {
    private final double time;
    private final Particle particle1;
    private final Particle particle2;
    private final int particle1CollisionCount;
    private final int particle2CollisionCount;
    private final EventType eventType;
    private FixedObstacle fixedObstacle;

    public Event(double time, Particle particle1, Particle particle2, EventType eventType) {
        this.time = time;
        this.particle1 = particle1;
        this.particle2 = particle2;
        this.eventType = eventType;
        this.particle1CollisionCount = particle1 == null ? 0 : particle1.collisionCount();
        this.particle2CollisionCount = particle2 == null ? 0 : particle2.collisionCount();
    }

    public Event(double time, Particle particle, FixedObstacle obstacle, EventType eventType) {
        this(time, particle, (Particle) null, eventType);
        this.fixedObstacle = obstacle;

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

    public FixedObstacle getFixedObstacle() {
        return this.fixedObstacle;
    }

    public EventType getEventType() {
        return eventType;
    }

    public boolean isValid() {
        return (particle1 == null || particle1.collisionCount() == particle1CollisionCount) && (particle2 == null || particle2.collisionCount() == particle2CollisionCount);
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(this.time, o.time);
    }
}
