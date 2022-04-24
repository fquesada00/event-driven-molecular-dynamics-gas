import argparse
import os
import matplotlib.pyplot as plot

from .utils import left_particles_counter


def particles_fraction_per_side_plot(particle_count, slit_width, threshold, equilibrium_time):
    print(
        f"Running simulation with {particle_count} particles, {slit_width} slit width and {threshold} threshold. Time to reach on equilibrium state: {equilibrium_time}.")

    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particle_count} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -DslitWidth={slit_width} -Dthreshold={threshold} -DequilibriumTime={equilibrium_time} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")

    left_particles_fraction, right_particle_fraction, time_steps = left_particles_counter(
        simulation_dynamic_output_file_name, simulation_static_output_file_name)
    plot.figure(figsize=(15, 10))
    plot.plot(time_steps, left_particles_fraction)
    plot.plot(time_steps, right_particle_fraction)

    plot.axhline(y=0.5+threshold, color='r', linestyle='--')
    plot.axhline(y=0.5-threshold, color='r', linestyle='--')

    plot.xlabel("Tiempo (s)")
    plot.ylabel("Fracción de partículas en recinto")

    # plot.legend(["100 particulas", "200 particulas", "350 particulas"])
    plot.legend(["Recinto izquierdo",
                "Recinto derecho", f"Umbral ({threshold})"], loc='upper right')
    plot.savefig(
        f"particles_fraction_per_side_{particle_count}_{slit_width}_{threshold}.png", dpi=300,)
    plot.show()
    plot.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--slit-width", default=0.02,
                        help="The fixed slit width used in the simulations. Defaults to 0.02.", dest="slit_width", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--equilibrium-time", default=10,
                        help="Time to reach from the equilibrium state of the simulations, in seconds. Defaults to 10 seconds.", dest="equilibrium_time", required=False)

    args = parser.parse_args()

    particles_fraction_per_side_plot(
        int(args.particles), float(args.slit_width), float(args.threshold), float(args.equilibrium_time))
