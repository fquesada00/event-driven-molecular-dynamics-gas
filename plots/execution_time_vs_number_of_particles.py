import argparse
import os
from statistics import stdev

import matplotlib.pyplot as plot


def execution_time_vs_number_of_particles(threshold, repetitions):
    print(
        f"Running simulation with {threshold} left particles fraction threshold and {repetitions} repetitions for each simulation.")
    particle_count = [100, 150, 200]
    average_execution_time = []
    average_execution_time_stdev = []
    for total_particles in particle_count:
        execution_time = []
        for i in range(repetitions):
            cmd = f"java -DnumberOfParticles={total_particles} -DleftParticlesFractionThreshold={threshold} -jar ../target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
            print(f"Simulation number {i + 1} with {total_particles} particles. Executing: {cmd}")
            os.system(cmd)
            print("Done")

            with open("summary.txt") as summary_file:
                for line_number, line in enumerate(summary_file):
                    if line_number == 3:
                        execution_time.append(float(line.split()[0]))

        average_execution_time.append(
            float(sum(execution_time) / len(execution_time)))
        average_execution_time_stdev.append(
            stdev(execution_time) if len(execution_time) > 1 else 0)

    # Plot execution time vs number of particles
    plot.errorbar(particle_count, average_execution_time, ls="none",
                  yerr=average_execution_time_stdev, ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)

    plot.xlabel("Number of particles")
    plot.ylabel("Execution time (s)")

    plot.show()
    plot.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--repetitions", default=1,
                        help="The number of repetitions of the simulation. Defaults to 1.", dest="repetitions", required=False)
    parser.add_argument("--threshold", default=0.5,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.5.", dest="threshold", required=False)

    args = parser.parse_args()

    execution_time_vs_number_of_particles(
        float(args.threshold), int(args.repetitions))
