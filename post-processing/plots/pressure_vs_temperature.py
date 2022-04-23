import argparse
import os
from statistics import mean, stdev
import matplotlib.pyplot as plt
import numpy as np
from .quadratic_error import quadratic_error
from ..helpers import get_equilibrium_iterations, parse_static_file
from ..models.CollisionType import ColissionType


def pressure_at_velocity(particles, threshold, equilibrium_time, velocity):
    print(
        f"Running simulation with {particles} particles, {velocity} velocity and {threshold} threshold. Time to reach on equilibrium state: {equilibrium_time}.")

    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particles} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -Dthreshold={threshold} -DequilibriumTime={equilibrium_time} -Dvelocity={velocity} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")

    simulation = parse_static_file(simulation_static_output_file_name)
    simulation_perimeter = (simulation.box_width + simulation.box_height) * 2
    event_type = None
    detected_collision = False
    total_impulse = 0
    equilibrium_start_time = equilibrium_end_time = 0
    last_n_iterations = get_equilibrium_iterations(
        simulation_dynamic_output_file_name, equilibrium_time)
    for iterations in last_n_iterations:
        iteration_data = iterations.split()
        if len(iteration_data) == 1:
            # Reset
            detected_collision = False

            # First event (no detected collision yet)
            if event_type is None:
                equilibrium_start_time = float(iteration_data[0])
                continue

            # Next event (detected collision)
            if event_type == ColissionType.PARTICLE_X_WALL_COLLISION:
                total_impulse += abs(2 * simulation.particle_mass * vy)
            elif event_type == ColissionType.PARTICLE_Y_WALL_COLLISION:
                total_impulse += abs(2 * simulation.particle_mass * vx)

            equilibrium_end_time = float(iteration_data[0])
        elif not detected_collision and (iteration_data[4] == "x" or iteration_data[4] == "y"):
            # Format: x y vx vy <'x' | 'y' | 'p' | '-'

            detected_collision = True

            vx = float(iteration_data[2])
            vy = float(iteration_data[3])
            wall_direction = iteration_data[4]

            if wall_direction == "x":
                event_type = ColissionType.PARTICLE_X_WALL_COLLISION
            else:
                event_type = ColissionType.PARTICLE_Y_WALL_COLLISION

    return (total_impulse / (equilibrium_end_time -
                             equilibrium_start_time)) / simulation_perimeter


def get_pressure_with_error_at_velocity(particles, threshold, equilibrium_time, velocity, repetitions):
    pressures = []
    for repetition in range(repetitions):
        print(f"Running simulation {repetition + 1} out of {repetitions}")
        pressure = pressure_at_velocity(
            particles, threshold, equilibrium_time, velocity)
        pressures.append(pressure)

    return mean(pressures), stdev(pressures)


def pressure_vs_temperature_plot(particles, threshold, equilibrium_time, repetitions, adjust):
    velocities = [0.005, 0.01, 0.02, 0.025, 0.03, 0.035]
    # velocities = [0.01, 0.02, 0.025]
    particle_mass = 1
    temperatures = []
    average_pressures = []
    yerror_bars = []

    for velocity in velocities:
        average_pressure, yerror_bar = get_pressure_with_error_at_velocity(
            particles, threshold, equilibrium_time, velocity, repetitions)
        temperatures.append((1 / 2) * particle_mass * velocity**2)
        average_pressures.append(average_pressure)
        yerror_bars.append(yerror_bar)

    if adjust:
        m_tries = list(np.arange(10000, 15000, 1))

        errors = quadratic_error(temperatures, average_pressures, m_tries)

        min_error = min(errors)
        min_error_index = errors.index(min_error)
        print(f"Minimum error: {min_error}")
        print(f"Minimum error index: {min_error_index}")
        print(f"Minimum error m: {m_tries[min_error_index]}")
        plt.subplot(1, 2, 2)
        plt.plot(m_tries, errors)
        plt.xlabel("Pendiente")
        plt.ylabel("Error cuadrático")
        plt.subplot(1, 2, 1)
        plt.plot(temperatures, m_tries[min_error_index]
                 * np.array(temperatures), '--k')

    plt.errorbar(temperatures, average_pressures, yerr=yerror_bars, ls="none",
                 ecolor='blue', marker='o', color="red", elinewidth=0.5, capsize=5)
    plt.xlabel("Energía Cinética (J)")
    plt.ylabel("Presión (N/m)")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--repetitions", default=5,
                        help="The number of repetitions of each simulation. Defaults to 5.", dest="repetitions", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--equilibrium-time", default=10,
                        help="Time to reach from the equilibrium state of the simulations, in seconds. Defaults to 10 seconds.", dest="equilibrium_time", required=False)
    parser.add_argument("--adjust", action="store_true", default=False,
                        help="Adjust the parameters of the simulation plot (P~T).", dest="adjust", required=False)
    args = parser.parse_args()

    pressure_vs_temperature_plot(int(args.particles), float(
        args.threshold), float(args.equilibrium_time), int(args.repetitions), bool(args.adjust))
