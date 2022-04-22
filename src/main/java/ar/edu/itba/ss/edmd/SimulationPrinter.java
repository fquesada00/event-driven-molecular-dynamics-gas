package ar.edu.itba.ss.edmd;

import ar.edu.itba.ss.edmd.events.Event;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

public class SimulationPrinter {
    private final String staticOutputFileName;
    private final String dynamicOutputFileName;
    private final String summaryFileName;
    private final int particleCount;
    private final double boxWidth;
    private final double boxHeight;
    private final double slitWidth;

    private final double particleMass;

    private final double particleRadius;

    public SimulationPrinter(String staticOutputFileName, String dynamicOutputFileName, String summaryFileName, int particleCount, double boxWidth, double boxHeight, double slitWidth, double particleMass, double particleRadius) {
        this.staticOutputFileName = staticOutputFileName;
        this.dynamicOutputFileName = dynamicOutputFileName;
        this.particleCount = particleCount;
        this.boxWidth = boxWidth;
        this.boxHeight = boxHeight;
        this.slitWidth = slitWidth;
        this.summaryFileName = summaryFileName;
        this.particleMass = particleMass;
        this.particleRadius = particleRadius;
    }

    public void printStaticParameters() throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(staticOutputFileName));
        printWriter.printf("%d\n%f\t%f\n%f\n%f\n%f", particleCount, boxWidth, boxHeight, slitWidth, particleMass, particleRadius);

        printWriter.close();
    }

    public void printSummary(double executionTime, double simulationTime, int eventCount, double leftParticlesFraction) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(summaryFileName));

        printWriter.printf("%d\n%f\t%f\n%f\n%f\n%f\n%d\n%f\n", particleCount, boxWidth, boxHeight, slitWidth, executionTime / 1000, simulationTime, eventCount, leftParticlesFraction);

        printWriter.close();
    }

    public void printStep(List<Particle> particles, Event event, double timeStep, boolean append,boolean isFirst) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(dynamicOutputFileName, append));
        if (!isFirst) {
            printWriter.println();
        }
        printWriter.printf("%f\n", timeStep);
        for (int i = 0; i < particles.size(); i++) {
            Particle particle = particles.get(i);
            if(i != 0){
                printWriter.println();
            }
            printWriter.printf("%f\t%f\t%f\t%f\t%c", particle.x(), particle.y(), particle.vx(), particle.vy(), event.getEventType(particle));
        }

        printWriter.close();
    }
}
