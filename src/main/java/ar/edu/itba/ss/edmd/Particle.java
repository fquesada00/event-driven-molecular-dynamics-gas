package ar.edu.itba.ss.edmd;


public class Particle {
    private final double radius;
    private final double mass;
    private Vector2D position;
    private int collisionCount;
    private Vector2D velocity;

    public Particle(double x, double y, double vx, double vy, double radius, double particlesMass) {
        this.position = new Vector2D(x, y);
        this.velocity = new Vector2D(vx, vy);
        this.radius = radius;
        this.mass = particlesMass;
        this.collisionCount = 0;
    }

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

        if (Double.compare(deltaVel.dot(deltaPos), 0) >= 0) return Double.POSITIVE_INFINITY;

        double d =
                Math.pow((deltaVel.dot(deltaPos)), 2) - (deltaVel.dot(deltaVel) * (deltaPos.dot(deltaPos) - Math.pow(this.radius + other.radius, 2)));

        if (d < 0) return Double.POSITIVE_INFINITY;

        return -(deltaVel.dot(deltaPos) + Math.sqrt(d)) / (deltaVel.dot(deltaVel));
    }

    public double collides(FixedObstacle obstacle) {
        return collides(new Particle(obstacle.x(), obstacle.y(), 0, 0, obstacle.radius(), 0));
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
        return Double.POSITIVE_INFINITY;
    }

    // Get collision time with a vertical wall
    public double collidesY(double boxWidth, double boxHeight, double slitWidth) {
        double deltaTime;

        if (position.x() < boxWidth / 2) {
            if (velocity.x() > 0) {
                deltaTime = (boxWidth / 2 - radius - position.x()) / velocity.x();

                if (deltaTime >= 0) {
                    double nextY = position.y() + velocity.y() * deltaTime;

                    // check if the particle is in the slit and going
                    if (nextY >= (boxHeight + slitWidth) / 2 || nextY <= (boxHeight - slitWidth) / 2) {
                        return deltaTime;
                    } else {
                        return (boxWidth - radius - position.x()) / velocity.x();
                    }
                }else {
                    return (boxWidth - radius - position.x()) / velocity.x();
                }
            } else if (velocity.x() < 0) {
                return (radius - position.x()) / velocity.x();
            }
        }
        // If the particle is in the second half, then it will bounce if it is going to the left and its y position is not in the slit,
        // or if it is going to the right
        else {
            if (velocity.x() > 0) {
                return (boxWidth - radius - position.x()) / velocity.x();
            } else if (velocity.x() < 0) {
                deltaTime = ((radius + boxWidth / 2) - position.x()) / velocity.x();

                if (deltaTime >= 0) {
                    double nextY = position.y() + velocity.y() * deltaTime;
                    if (nextY >= (boxHeight + slitWidth) / 2 || nextY <= (boxHeight - slitWidth) / 2) {
                        return deltaTime;
                    } else {
                        return (radius - position.x()) / velocity.x();
                    }
                }else{
                    return (radius - position.x()) / velocity.x();
                }
            }
        }

        //Check if the particle is in the slit at the collision time

        return Double.POSITIVE_INFINITY;
    }

    // Update particle velocity on collision
    public void bounce(Particle other) {
        collisionCount++;
        other.collisionCount++;
        Vector2D deltaPos = other.position.subtract(this.position);
        Vector2D deltaVel = other.velocity.subtract(this.velocity);
        double sigma = this.radius + other.radius;
        double J = 2 * this.mass * other.mass * (deltaVel.dot(deltaPos)) / (sigma * (this.mass + other.mass));
        double Jx = J * deltaPos.x() / sigma;
        double Jy = J * deltaPos.y() / sigma;
        this.velocity = new Vector2D(this.velocity.x() + Jx / this.mass, this.velocity.y() + Jy / this.mass);
        other.velocity = new Vector2D(other.velocity.x() - Jx / other.mass, other.velocity.y() - Jy / other.mass);
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

    public void bounceFixedObstacle(FixedObstacle obstacle) {
        this.collisionCount++;

        Vector2D normal = this.position.subtract(obstacle.position());

        double angle = new Vector2D(1, 0).angle(normal);

        double cn = 1;
        double ct = 1;

        double cos = Math.cos(angle);
        double sin = Math.sin(angle);

        Matrix2x2 transform = new Matrix2x2(-cn * Math.pow(cos, 2) + ct * Math.pow(sin, 2),
                -(cn + ct) * sin * cos,
                -(cn + ct) * sin * cos,
                -cn * Math.pow(sin, 2) + ct * Math.pow(cos, 2));

        this.velocity = this.velocity.applyTransform(transform);
    }

    public double x() {
        return position.x();
    }

    public double y() {
        return position.y();
    }

    public double vx() {
        return velocity.x();
    }

    public double vy() {
        return velocity.y();
    }

    public double radius() {
        return radius;
    }

    public double mass() {
        return mass;
    }

    public int collisionCount() {
        return collisionCount;
    }

    public void updatePosition(double deltaTime) {
        Vector2D newPosition = this.position.add(this.velocity.scale(deltaTime));
        if(newPosition.x() < 0 || newPosition.x() > 0.24 || newPosition.y() < 0 || newPosition.y() > 0.09) {
            System.out.println("error");
        }
        this.position = newPosition;
    }

    public boolean overlaps(Particle other) {
        return this.position.distance(other.position) < this.radius + other.radius;
    }
}
