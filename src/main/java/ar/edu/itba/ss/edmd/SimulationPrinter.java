package ar.edu.itba.ss.edmd;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class SimulationPrinter {
    private final String outputFileName;
    private final int particleCount;
    private final double boxWidth;
    private final double boxHeight;
    private final double slitWidth;

    public SimulationPrinter(String outputFileName, int particleCount, double boxWidth, double boxHeight, double slitWidth) {
        this.outputFileName = outputFileName;
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
    }

    public void printInitialParameters() throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(outputFileName));
        printWriter.printf("%d\n%f\t%f\n%f\n", particleCount, boxWidth, boxHeight, slitWidth);

        printWriter.close();
    }

    public void printStep(List<Particle> particles, double timeStep, boolean append) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(outputFileName, append));

        printWriter.printf("%f\n", timeStep);

        for (Particle particle : particles) {
            printWriter.printf("%f\t%f\t%f\t%f\t%f\t%f\n", particle.x(), particle.y(), particle.vx(), particle.vy(), particle.mass(), particle.radius());
        }

        printWriter.close();
    }
}
