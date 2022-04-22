import argparse
import os
from statistics import mean, stdev

import matplotlib.pyplot as plot
from ..helpers.equilibrium_iterations import get_equilibrium_time

def get_simulation_equilibrium_time(threshold, slit_width, particles):
    simulation_dynamic_output_file_name = "dynamic.txt"

    cmd = f"java -DnumberOfParticles={particles} -Dthreshold={threshold} -DslitWidth={slit_width} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
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
    particle_count = [100, 150, 200]
    average_execution_times = []
    yerror_bars = []
    for total_particles in particle_count:
        average_equilibrium_time, yerror_bar = equilibrium_time_with_error(            
            threshold, repetitions, slit_width, total_particles)
        average_execution_times.append(average_equilibrium_time)
        yerror_bars.append(yerror_bar)
    

    plot.errorbar(particle_count, average_execution_times, ls="none",
                  yerr=yerror_bars, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)

    plot.xlabel("Número de partículas")
    plot.ylabel("Tiempo de equilibrio (s)")

    plot.show()
    plot.close()

def equilibrium_time_vs_slit_width(threshold, repetitions, particles):
    slit_widths = [0.005, 0.01, 0.02, 0.05, 0.065, 0.08]
    # slit_widths = [0.02, 0.05]
    average_execution_times = []
    yerror_bars = []
    for slit_width in slit_widths:
        average_equilibrium_time, yerror_bar = equilibrium_time_with_error(
            threshold, repetitions, slit_width, particles)
        average_execution_times.append(average_equilibrium_time)
        yerror_bars.append(yerror_bar)

    plot.errorbar(slit_widths, average_execution_times, ls="none",
                    yerr=yerror_bars, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)
    
    plot.xlabel("Ancho del tabique (m)")
    plot.ylabel("Tiempo de equilibrio (s)")
    plot.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--slit-width", default=0.02,
                        help="The fixed slit width used in the simulations. Defaults to 0.02.", dest="slit_width", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--repetitions", default=5,
                        help="The number of repetitions of the simulation. Defaults to 1.", dest="repetitions", required=False)
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