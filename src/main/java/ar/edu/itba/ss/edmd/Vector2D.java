package ar.edu.itba.ss.edmd;


public record Vector2D(double x, double y) {
    public Vector2D add(Vector2D other) {
        return new Vector2D(x + other.x, y + other.y);
    }

    public Vector2D subtract(Vector2D other) {
        return new Vector2D(this.x - other.x, this.y - other.y);
    }

    public double dot(Vector2D other) {
        return this.x * other.x + this.y * other.y;
    }

    public Vector2D scale(double factor) {
        return new Vector2D(this.x * factor, this.y * factor);
    }

    public double length() {
        return Math.sqrt(this.dot(this));
    }

    public double distance(Vector2D other) {
        return this.subtract(other).length();
    }

    public double angle(Vector2D other) {
        return Math.acos(this.dot(other) / (this.length() * other.length()));
    }

    public Vector2D applyTransform(Matrix2x2 transform) {
        return new Vector2D(
                transform.get(0, 0) * x + transform.get(0, 1) * y,
                transform.get(1, 0) * x + transform.get(1, 1) * y
        );
    }
}
