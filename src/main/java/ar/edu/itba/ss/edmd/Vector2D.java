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
}
