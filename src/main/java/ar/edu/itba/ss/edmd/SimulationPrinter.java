package ar.edu.itba.ss.edmd;

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

    public void printStep(List<Particle> particles, Event event, double timeStep, boolean append) throws IOException {
        PrintWriter printWriter = new PrintWriter(new FileWriter(dynamicOutputFileName, append));

        printWriter.printf("%f\n", timeStep);
        char value = '-';
        Particle eventParticle = event.getParticle1();
        Particle eventParticle2 = event.getParticle2();
        switch (event.getEventType()) {
            case PARTICLE_X_WALL_COLLISION -> value = 'x';
            case PARTICLE_Y_WALL_COLLISION -> value = 'y';
            case PARTICLES_COLLISION -> value = 'p';
        }
        for (Particle particle : particles) {
            printWriter.printf("%f\t%f\t%f\t%f\t%c\n", particle.x(), particle.y(), particle.vx(), particle.vy(), particle.equals(eventParticle) || particle.equals(eventParticle2) ? value : '-');
        }

        printWriter.close();
    }
}
