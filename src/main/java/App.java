import ar.edu.itba.ss.edmd.EventDrivenMolecularDynamics;

import java.io.IOException;

public class App {
    public static void main(String[] args) throws IOException {
        boolean debug = Boolean.parseBoolean(System.getProperty("debug", "false"));
        String staticOutputFileName = System.getProperty("staticSimulationOutFileName", "static.txt");
        String dynamicOutputFileName = System.getProperty("dynamicSimulationOutFileName", "dynamic.txt");
        String summaryFileName = System.getProperty("summaryOutFileName", "summary.txt");
        int numberOfParticles = Integer.parseInt(System.getProperty("numberOfParticles", "100"));
        double slitWidth = Double.parseDouble(System.getProperty("slitWidth", "0.01"));
        double threshold = Double.parseDouble(System.getProperty("threshold", "0.15"));
        double equilibriumTime = Double.parseDouble(System.getProperty("equilibriumTime", "0"));
        double velocity = Double.parseDouble(System.getProperty("velocity", "0.01"));
        EventDrivenMolecularDynamics edmd = new EventDrivenMolecularDynamics(numberOfParticles, 0.24, 0.09, slitWidth,
                velocity, 1.0, 0.0015, threshold, equilibriumTime, staticOutputFileName, dynamicOutputFileName,
                summaryFileName);
        edmd.run(debug);
    }
}
