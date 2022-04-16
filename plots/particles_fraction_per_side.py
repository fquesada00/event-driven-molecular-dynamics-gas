import argparse
import os
from statistics import stdev
import matplotlib.pyplot as plot

from utils import left_particles_counter


def particles_fraction_per_side_plot(particle_count, slit_width, repetitions, threshold, log_frequency):
    print(f"Running {repetitions} simulation{'s' if repetitions > 1 else ''} with {particle_count} particles, {slit_width} slit width and {threshold} left particles fraction threshold. Logging every {log_frequency} time steps.")

    simulation_output_file_name = "simulation.txt"
    simulations_left_particles_fraction = []
    simulations_right_particles_fraction = []
    log_every_n_time_steps = log_frequency

    max_number_of_time_steps = -1
    max_time_steps_array = []

    for i in range(repetitions):
        cmd = f"java -DnumberOfParticles={particle_count} -DsimulationOutFileName={simulation_output_file_name} -DslitWidth={slit_width} -DleftParticlesFractionThreshold={threshold} -jar ../target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
        print(f"Simulation number {i + 1}. Executing: {cmd}")
        os.system(cmd)
        print("Done")

        left_particles_fraction, right_particle_fraction, time_steps = left_particles_counter(
            simulation_output_file_name, log_every_n_time_steps)

        simulations_left_particles_fraction.append(left_particles_fraction)
        simulations_right_particles_fraction.append(right_particle_fraction)

        if len(time_steps) > max_number_of_time_steps:
            max_number_of_time_steps = len(time_steps)
            max_time_steps_array = time_steps

    # Calculate standard deviation for both left and right particles fraction
    left_particles_fraction_stdev = []
    right_particles_fraction_stdev = []
    average_left_particles_fraction = []
    average_right_particles_fraction = []

    for i in range(max_number_of_time_steps):
        left_particles_fraction_at_i_time_step = []
        right_particles_fraction_at_i_time_step = []
        total_simulations_at_i_time_step = 0
        # Iterate through all simulations
        for j in range(repetitions):
            # Load left particles fraction at i time step if exists
            if i < len(simulations_left_particles_fraction[j]):
                left_particles_fraction_at_i_time_step.append(
                    simulations_left_particles_fraction[j][i])
                right_particles_fraction_at_i_time_step.append(
                    1 - simulations_left_particles_fraction[j][i])
                total_simulations_at_i_time_step += 1

        # Calculate average left particles fraction at i time step
        average_left_particles_fraction.append(
            sum(left_particles_fraction_at_i_time_step) / total_simulations_at_i_time_step)
        # Calculate average right particles fraction at i time step
        average_right_particles_fraction.append(
            sum(right_particles_fraction_at_i_time_step) / total_simulations_at_i_time_step)
        # Calculate standard deviation for left particles fraction at i time step
        left_particles_fraction_stdev.append(
            stdev(left_particles_fraction_at_i_time_step) if total_simulations_at_i_time_step > 1 else 0)
        # Calculate standard deviation for right particles fraction at i time step
        right_particles_fraction_stdev.append(
            stdev(right_particles_fraction_at_i_time_step) if total_simulations_at_i_time_step > 1 else 0)

    plot.errorbar(max_time_steps_array, average_left_particles_fraction, ls="none",
                  yerr=left_particles_fraction_stdev, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)
    plot.errorbar(max_time_steps_array, average_right_particles_fraction, ls="none",
                  yerr=right_particles_fraction_stdev, ecolor='blue', marker='o',  color="green", elinewidth=0.5, capsize=5)

    plot.xlabel("Número de evento")
    plot.ylabel("Fracción de partículas en cada recinto")

    # plot.legend(["100 particulas", "200 particulas", "350 particulas"])
    plot.legend(["Fracción de partículas en recinto izquierdo",
                "Fracción de partículas en recinto derecho"])
    plot.show()
    plot.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--repetitions", default=1,
                        help="The number of repetitions of the simulation. Defaults to 1.", dest="repetitions", required=False)
    parser.add_argument("--slit_width", default=0.02,
                        help="The fixed slit width used in the simulations. Defaults to 0.02.", dest="slit_width", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--threshold", default=0.5,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.5.", dest="threshold", required=False)
    parser.add_argument("--log_frequency", default=1,
                        help="The log frequency of the plot. Defaults to 1.", dest="log_frequency", required=False)

    args = parser.parse_args()

    particles_fraction_per_side_plot(
        int(args.particles), float(args.slit_width), int(args.repetitions), float(args.threshold), int(args.log_frequency))
