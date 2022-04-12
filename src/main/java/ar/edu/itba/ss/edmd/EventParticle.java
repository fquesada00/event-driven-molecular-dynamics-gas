package ar.edu.itba.ss.edmd;


public class EventParticle {
    private  double radius;
    private  double mass;
    private Position2D position;
    private int collisionCount;
    private Velocity2D velocity;
    public EventParticle(Position2D position,Velocity2D velocity, double radius,double mass) {
        this.position = position;
        this.velocity = velocity;
        this.radius = radius;
        this.mass = mass;
        this.collisionCount = 0;
    }

    public double collides(EventParticle b){
        //TODO
        return 0.0;
    }

    public double collidesX(){
        //TODO
        return 0.0;
    }

    public double collidesY(){
        //TODO
        return 0.0;
    }

    public void bounce(EventParticle b){
        //TODO
    }

    public void bounceX(){
        //TODO
    }

    public void bounceY(){
        //TODO
    }

    public int getCollisionCount() {
        return collisionCount;
    }
}
