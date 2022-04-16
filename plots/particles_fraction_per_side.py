import argparse
import os
from statistics import stdev
import matplotlib.pyplot as plot

from utils import left_particles_counter


def particles_fraction_per_side_plot(particle_count, slit_width, repetitions, threshold, log_frequency):
    print(f"Running {repetitions} simulation{'s' if repetitions > 1 else ''} with {particle_count} particles, {slit_width} slit width and {threshold} left particles fraction threshold. Logging every {log_frequency} time steps.")

    simulation_output_file_name = "simulation.txt"
    simulations_left_particles_fraction = []
    log_every_n_time_steps = log_frequency

    for i in range(repetitions):
        cmd = f"java -DnumberOfParticles={particle_count} -DsimulationOutFileName={simulation_output_file_name} -DslitWidth={slit_width} -DleftParticlesFractionThreshold={threshold} -jar ../target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
        print(f"Simulation number {i + 1}. Executing: {cmd}")
        os.system(cmd)
        print("Done")

        left_particles_fraction, right_particle_fraction, time_steps = left_particles_counter(
            simulation_output_file_name, log_every_n_time_steps)

        simulations_left_particles_fraction.append(left_particles_fraction)

    # Calculate standard deviation for both left and right particles fraction
    left_particles_fraction_stdev = []
    right_particles_fraction_stdev = []

    # FIXME: This is not working, because we have to iterate over the maximum number of time steps, and maybe the first simulation is not the one with the maximum number of time steps
    for i in range(len(simulations_left_particles_fraction[0])):
        left_particles_fraction_at_i_time_step = [
            row[i] for row in simulations_left_particles_fraction]
        left_particles_fraction_stdev.append(
            stdev(left_particles_fraction_at_i_time_step))
        right_particles_fraction_at_i_time_step = [
            1 - row[i] for row in simulations_left_particles_fraction]
        right_particles_fraction_stdev.append(
            stdev(right_particles_fraction_at_i_time_step))
            
    plot.errorbar(time_steps, left_particles_fraction, ls="none",
                  yerr=left_particles_fraction_stdev, color='red', marker='o', ecolor="blue", elinewidth=0.5, capsize=5)
    plot.errorbar(time_steps, right_particle_fraction, ls="none",
                  yerr=right_particles_fraction_stdev, color='red', marker='o',  ecolor="black", elinewidth=0.5, capsize=5)

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
