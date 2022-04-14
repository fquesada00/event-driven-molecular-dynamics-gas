import ar.edu.itba.ss.edmd.EventDrivenMolecularDynamics;

public class App {
    public static void main(String[] args) {
        EventDrivenMolecularDynamics edmd = new EventDrivenMolecularDynamics(100,0.24,0.09,0.02,0.01,1.0,0.001);
        edmd.run();
    }
}
