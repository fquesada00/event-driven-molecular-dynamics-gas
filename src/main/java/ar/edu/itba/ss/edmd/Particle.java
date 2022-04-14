package ar.edu.itba.ss.edmd;


public class Particle {
    private final double radius;
    private final double mass;
    private Vector2D position;
    private int collisionCount;
    private Vector2D velocity;

    public Particle(Vector2D position, Vector2D velocity, double radius, double mass) {
        this.position = position;
        this.velocity = velocity;
        this.radius = radius;
        this.mass = mass;
        this.collisionCount = 0;
    }

    // Get collision time with another particle
    public double collides(Particle other) {
        Vector2D deltaPos = other.position.subtract(this.position);
        Vector2D deltaVel = other.velocity.subtract(this.velocity);

        if (Double.compare(deltaVel.dot(deltaPos), 0) >= 0) return Double.NEGATIVE_INFINITY;

        double d = Math.pow((deltaVel.dot(deltaPos)), 2) - (deltaPos.dot(deltaPos) * (deltaVel.dot(deltaVel) - Math.pow(this.radius + other.radius, 2)));

        if (d < 0) return Double.NEGATIVE_INFINITY;

        return (-deltaVel.dot(deltaPos) - Math.sqrt(d)) / (deltaVel.dot(deltaVel));
    }

    // Get collision time with a horizontal wall
    public double collidesX(double boxHeight) {
        if (velocity.y() > 0) {
            return (boxHeight - radius - position.y()) / velocity.y();
        }

        if (velocity.y() < 0) {
            return (radius - position.y()) / velocity.y();
        }

        // vy = 0
        return Double.NEGATIVE_INFINITY;
    }

    // Get collision time with a vertical wall
    public double collidesY(double boxWidth) {
        if (velocity.x() > 0) {
            return (boxWidth - radius - position.x()) / velocity.x();
        }

        if (velocity.x() < 0) {
            return (radius - position.x()) / velocity.x();
        }

        // vx = 0
        return Double.NEGATIVE_INFINITY;
    }

    // Update particle velocity on collision
    public void bounce(Particle other) {
        Vector2D deltaPos = other.position.subtract(this.position);
        Vector2D deltaVel = other.velocity.subtract(this.velocity);
//Vector2D deltaPodeltaVel.dot(deltaPosr).velocity.subtract(this.velocity);
//        double J = 2 * this.mass * other.mass * ()
    }

    // Update particle velocity on collision with a horizontal wall
    public void bounceX() {
        this.collisionCount++;
        this.velocity = new Vector2D(this.velocity.x(), -this.velocity.y());
    }

    // Update particle velocity on collision with a vertical wall
    public void bounceY() {
        this.collisionCount++;
        this.velocity = new Vector2D(-this.velocity.x(), this.velocity.y());
    }

    public int getCollisionCount() {
        return collisionCount;
    }
}
