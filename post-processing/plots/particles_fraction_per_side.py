import argparse
import os
import matplotlib.pyplot as plot

from .utils import left_particles_counter


def particles_fraction_per_side_plot(particle_count, slit_width, threshold, equilibrium_iterations):
    print(f"Running simulation with {particle_count} particles, {slit_width} slit width and {threshold} left particles fraction threshold. Number of equilibrium iterations: {equilibrium_iterations}.")

    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particle_count} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -DslitWidth={slit_width} -Dthreshold={threshold} -DequilibriumIterations={equilibrium_iterations} -jar ../target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")

    left_particles_fraction, right_particle_fraction, time_steps = left_particles_counter(
        simulation_dynamic_output_file_name, simulation_static_output_file_name)

    plot.plot(time_steps, left_particles_fraction)
    plot.plot(time_steps, right_particle_fraction)

    plot.xlabel("Tiempo (s)")
    plot.ylabel("Fracción de partículas en cada recinto")

    # plot.legend(["100 particulas", "200 particulas", "350 particulas"])
    plot.legend(["Fracción de partículas en recinto izquierdo",
                "Fracción de partículas en recinto derecho"])
    plot.show()
    plot.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--slit_width", default=0.02,
                        help="The fixed slit width used in the simulations. Defaults to 0.02.", dest="slit_width", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--equilibrium-iterations", default=0.05,
                    help="The number of consecutive iterations on the equilibrium state used in the simulations. Defaults to 10.", dest="equilibrium_iterations", required=False)

    args = parser.parse_args()

    particles_fraction_per_side_plot(
        int(args.particles), float(args.slit_width), float(args.threshold), int(args.equilibrium_iterations))
