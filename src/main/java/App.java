import ar.edu.itba.ss.edmd.EventDrivenMolecularDynamics;

import java.io.IOException;

public class App {
    public static void main(String[] args) throws IOException {
        String staticOutputFileName = System.getProperty("staticSimulationOutFileName", "static.txt");
        String dynamicOutputFileName = System.getProperty("dynamicSimulationOutFileName", "dynamic.txt");
        String summaryFileName = System.getProperty("summaryOutFileName", "summary.txt");
        int numberOfParticles = Integer.parseInt(System.getProperty("numberOfParticles", "100"));
        double slitWidth = Double.parseDouble(System.getProperty("slitWidth", "0.02"));
        double leftParticlesFractionThreshold = Double.parseDouble(System.getProperty("leftParticlesFractionThreshold", "0.5"));
        EventDrivenMolecularDynamics edmd = new EventDrivenMolecularDynamics(numberOfParticles, 0.24, 0.09, slitWidth, 0.01, 1.0, 0.001, leftParticlesFractionThreshold, staticOutputFileName,dynamicOutputFileName, summaryFileName);
        edmd.run();
    }
}
