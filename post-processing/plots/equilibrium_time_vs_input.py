import argparse
import os
from statistics import mean, stdev
from turtle import right

import matplotlib.pyplot as plot
from .utils import left_particles_counter
from ..helpers.equilibrium_iterations import get_equilibrium_time

def load_fp_iteration_data(left_particle_fractions: list, right_particle_fractions: list, time_steps: list, legends: list, total_particles: int, slit_width: float, vary = "N"):
    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    left_particle_fraction, right_particle_fraction, time_step = left_particles_counter(
        simulation_dynamic_output_file_name, simulation_static_output_file_name)
    left_particle_fractions.append(left_particle_fraction)
    right_particle_fractions.append(right_particle_fraction)
    time_steps.append(time_step)
    if vary == "N":
        legends.append(f"Recinto izquierdo (N = {total_particles})")
        legends.append(f"Recinto derecho (N = {total_particles})")
    else:
        legends.append(f"Recinto izquierdo (D = {slit_width} m)")
        legends.append(f"Recinto derecho (D = {slit_width} m)")


def prepare_fp_plot(iterations: int, time_steps: list, left_particle_fractions: list, right_particle_fractions: list, legends: list,threshold: float, vary="N"):
    plot.figure(2)
    for iteration in range(iterations):
        plot.plot(time_steps[iteration], left_particle_fractions[iteration])
        plot.plot(time_steps[iteration], right_particle_fractions[iteration])
    
    plot.axhline(y=0.5+threshold, color='r', linestyle='--')
    plot.axhline(y=0.5-threshold, color='r', linestyle='--')

    legends.append(f"Umbral ({threshold})")
    plot.legend(legends, loc='upper right')

    plot.xlabel("Tiempo (s)")
    plot.ylabel("Fracción de partículas en recinto")

    if vary == "N":
        plot.savefig("fp_vs_number_of_particles.png", dpi=300)
    else:
        plot.savefig("fp_vs_slit_width.png", dpi=300)



def get_simulation_equilibrium_time(threshold, slit_width, particles):
    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particles} -Dthreshold={threshold} -DslitWidth={slit_width} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")

    return get_equilibrium_time(simulation_dynamic_output_file_name)


def equilibrium_time_with_error(threshold, repetitions, slit_width, particles):
    equilibrium_times = []
    for repetition in range(repetitions):
        print(f"Running simulation {repetition + 1} out of {repetitions}")
        simulation_equilibrium_time = get_simulation_equilibrium_time(
            threshold, slit_width, particles)
        equilibrium_times.append(simulation_equilibrium_time)

    return mean(equilibrium_times), stdev(equilibrium_times)


def equilibrium_time_vs_number_of_particles(threshold, repetitions, slit_width):
    particle_count = [50, 85, 130, 185, 250, 300]
    # particle_count = [300]
    average_execution_times = []
    yerror_bars = []
    plot.figure(figsize=(15, 10))

    left_particle_fractions = []
    right_particle_fractions = []
    time_steps = []
    legends = []

    for total_particles in particle_count:
        average_equilibrium_time, yerror_bar = equilibrium_time_with_error(
            threshold, repetitions, slit_width, total_particles)
        average_execution_times.append(average_equilibrium_time)
        yerror_bars.append(yerror_bar)

        # Get left and right particle fractions
        load_fp_iteration_data(left_particle_fractions, right_particle_fractions, time_steps, legends, total_particles, slit_width, "N")


    plot.figure(1)
    plot.errorbar(particle_count, average_execution_times, ls="none",
                  yerr=yerror_bars, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)

    plot.xlabel("Número de partículas")
    plot.ylabel("Tiempo de equilibrio (s)")
    plot.savefig("equilibrium_time_vs_number_of_particles.png", dpi=300)

    prepare_fp_plot(len(particle_count), time_steps, left_particle_fractions, right_particle_fractions, legends, threshold, "N")
    plot.xlim(right=175)

    plot.show()
    plot.close()


def equilibrium_time_vs_slit_width(threshold, repetitions, particles):
    slit_widths = [0.01, 0.02, 0.035, 0.05, 0.065, 0.08]
    # slit_widths = [0.01, 0.08]
    average_execution_times = []
    yerror_bars = []
    plot.figure(figsize=(15, 10))

    left_particle_fractions = []
    right_particle_fractions = []
    time_steps = []
    legends = []

    for slit_width in slit_widths:
        average_equilibrium_time, yerror_bar = equilibrium_time_with_error(
            threshold, repetitions, slit_width, particles)
        average_execution_times.append(average_equilibrium_time)
        yerror_bars.append(yerror_bar)

        # Get left and right particle fractions
        load_fp_iteration_data(left_particle_fractions, right_particle_fractions, time_steps, legends, particles, slit_width, "D")

    plot.errorbar(slit_widths, average_execution_times, ls="none",
                  yerr=yerror_bars, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)

    plot.xlabel("Ancho del tabique (m)")
    plot.ylabel("Tiempo de equilibrio (s)")
    plot.savefig("equilibrium_time_vs_slit_width.png", dpi=300)

    prepare_fp_plot(len(slit_widths), time_steps, left_particle_fractions, right_particle_fractions, legends, threshold, "D")
    plot.xlim(right=435)

    plot.show()
    plot.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--slit-width", default=0.02,
                        help="The fixed slit width used in the simulations. Defaults to 0.02.", dest="slit_width", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--repetitions", default=5,
                        help="The number of repetitions of the simulation. Defaults to 5.", dest="repetitions", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--vary", default="N",
                        help="Specify with which parameter the simulation should be run. Defaults to particle count.", dest="vary", required=False)

    args = parser.parse_args()

    if args.vary == "N":
        equilibrium_time_vs_number_of_particles(
            float(args.threshold), int(args.repetitions), float(args.slit_width))
    elif args.vary == "D":
        equilibrium_time_vs_slit_width(
            float(args.threshold), int(args.repetitions), int(args.particles))
    else:
        print("Invalid argument for --vary")
        exit(1)
