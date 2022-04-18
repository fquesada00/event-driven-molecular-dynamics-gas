package ar.edu.itba.ss.edmd;

public class FixedObstacle {
    private final Vector2D position;
    private final double radius;

    public FixedObstacle(double x, double y, double radius) {
        this.position = new Vector2D(x, y);
        this.radius = radius;
    }

    public Vector2D position() {
        return position;
    }

    public double radius() {
        return radius;
    }

    public double x() {
        return position.x();
    }

    public double y() {
        return position.y();
    }
}
