package ar.edu.itba.ss.edmd;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class SimulationPrinter {
    private final String outputFileName;
    private final String summaryFileName;
    private final int particleCount;
    private final double boxWidth;
    private final double boxHeight;
    private final double slitWidth;

    public SimulationPrinter(String outputFileName, String summaryFileName, int particleCount, double boxWidth, double boxHeight, double slitWidth) {
        this.outputFileName = outputFileName;
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
        this.summaryFileName = summaryFileName;
    }

    public void printInitialParameters() throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(outputFileName));
        printWriter.printf("%d\n%f\t%f\n%f\n", particleCount, boxWidth, boxHeight, slitWidth);

        printWriter.close();
    }

    public void printSummary(double executionTime, double simulationTime, int eventCount, double leftParticlesFraction) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(summaryFileName));

        printWriter.printf("%d\n%f\t%f\n%f\n%f\n%f\n%d\n%f\n", particleCount, boxWidth, boxHeight, slitWidth, executionTime / 1000, simulationTime, eventCount, leftParticlesFraction);

        printWriter.close();
    }

    public void printStep(List<Particle> particles, double timeStep,double wallMomentum, boolean append) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(outputFileName, append));

        printWriter.printf("%f\t%f\n", timeStep,wallMomentum);

        for (Particle particle : particles) {
            int red = particle.x() > boxWidth / 2 ? 255 : 0;
            int blue = particle.x() < boxWidth / 2 ? 255 : 0;
            printWriter.printf("%f\t%f\t%f\t%f\t%f\t%f\t%d\t0\t%d\n", particle.x(), particle.y(), particle.vx(), particle.vy(), particle.mass(), particle.radius(), red, blue);
        }

        printWriter.close();
    }
}
