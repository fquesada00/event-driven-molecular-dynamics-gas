package ar.edu.itba.ss.edmd;

public class Matrix2x2 {
    private final double[][] matrix;

    public Matrix2x2(double a00, double a01, double a10, double a11) {
        matrix = new double[2][2];
        matrix[0][0] = a00;
        matrix[0][1] = a01;
        matrix[1][0] = a10;
        matrix[1][1] = a11;
    }

    public void set(int row, int column, double value) {
        matrix[row][column] = value;
    }

    public double get(int row, int column) {
        return matrix[row][column];
    }

}
