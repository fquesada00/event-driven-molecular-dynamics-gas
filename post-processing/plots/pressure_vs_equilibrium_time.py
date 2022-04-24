import argparse
import os
import matplotlib.pyplot as plt

from ..helpers import get_equilibrium_iterations, parse_static_file

# Only for testing
def pressures_every_delta_eq_in_simulation(particles, threshold, velocity, equilibrium_time, delta_eq):
    print(
        f"Running simulation with {particles} particles, {velocity} velocity and {threshold} threshold. Time to reach on equilibrium state: {equilibrium_time}, with delta equilibrium of {delta_eq}.")

    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particles} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -Dthreshold={threshold} -DequilibriumTime={equilibrium_time} -Dvelocity={velocity} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")
    
    simulation = parse_static_file(simulation_static_output_file_name)
    simulation_perimeter = (simulation.box_width + simulation.box_height) * \
        2 + (simulation.box_height - simulation.slit_width) * 2

    total_impulse = 0
    pressures = []
    time_steps = []
    current_delta_eq_index = 0
    equilibrium_start_time = -1
    with open(simulation_dynamic_output_file_name, "r") as f:
        for idx, iterations in enumerate(f):
            iteration_data = iterations.split()
            if len(iteration_data) == 1:

                if equilibrium_start_time == -1:
                    equilibrium_start_time = float(iteration_data[0])

                # If the delta_eq is reached, load data and reset impulse
                if (equilibrium_start_time + (delta_eq * (current_delta_eq_index + 1))) < float(iteration_data[0]):
                    # Load pressure and time step
                    pressure = (total_impulse / delta_eq) / simulation_perimeter
                    pressures.append(pressure)
                    time_steps.append(delta_eq * (current_delta_eq_index + 1))

                    # Reset
                    total_impulse = 0
                    current_delta_eq_index += 1

            elif (iteration_data[4] == "x" or iteration_data[4] == "y"):
                # Format: x y vx vy <'x' | 'y' | 'p' | '-'

                vx = float(iteration_data[2])
                vy = float(iteration_data[3])
                wall_direction = iteration_data[4]

                if wall_direction == "x":
                    total_impulse += abs(2 * simulation.particle_mass * vy)
                else:
                    total_impulse += abs(2 * simulation.particle_mass * vx)

    # Load last delta_eq data
    pressure = (total_impulse / delta_eq) / simulation_perimeter
    pressures.append(pressure)
    time_steps.append(delta_eq * (current_delta_eq_index + 1))

    return pressures, time_steps


def pressures_every_delta_eq(particles, threshold, velocity, equilibrium_time, delta_eq):
    print(
        f"Running simulation with {particles} particles, {velocity} velocity and {threshold} threshold. Time to reach on equilibrium state: {equilibrium_time}, with delta equilibrium of {delta_eq}.")

    simulation_dynamic_output_file_name = "dynamic.txt"
    simulation_static_output_file_name = "static.txt"

    cmd = f"java -DnumberOfParticles={particles} -DdynamicSimulationOutFileName={simulation_dynamic_output_file_name} -DstaticSimulationOutFileName={simulation_static_output_file_name} -Dthreshold={threshold} -DequilibriumTime={equilibrium_time} -Dvelocity={velocity} -jar ./target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")
    
    simulation = parse_static_file(simulation_static_output_file_name)
    simulation_perimeter = (simulation.box_width + simulation.box_height) * \
        2 + (simulation.box_height - simulation.slit_width) * 2

    total_impulse = 0
    last_n_iterations = get_equilibrium_iterations(
        simulation_dynamic_output_file_name, equilibrium_time)

    delta_eqs = [i * delta_eq for i in range(1, int(equilibrium_time / delta_eq) + 1)]

    pressures = []
    time_steps = []
    current_delta_eq_index = 0
    equilibrium_start_time = -1
    for iterations in last_n_iterations:
        iteration_data = iterations.split()
        if len(iteration_data) == 1:

            if equilibrium_start_time == -1:
                equilibrium_start_time = float(iteration_data[0])

            # If the delta_eq is reached, load data and reset impulse
            if (equilibrium_start_time + delta_eqs[current_delta_eq_index]) < float(iteration_data[0]):
                # Load pressure and time step
                pressure = (total_impulse / delta_eq) / simulation_perimeter
                pressures.append(pressure)
                time_steps.append(delta_eq * (current_delta_eq_index + 1))

                # Reset
                total_impulse = 0
                current_delta_eq_index += 1

        elif (iteration_data[4] == "x" or iteration_data[4] == "y"):
            # Format: x y vx vy <'x' | 'y' | 'p' | '-'

            vx = float(iteration_data[2])
            vy = float(iteration_data[3])
            wall_direction = iteration_data[4]

            if wall_direction == "x":
                total_impulse += abs(2 * simulation.particle_mass * vy)
            else:
                total_impulse += abs(2 * simulation.particle_mass * vx)

    # Load last delta_eq data
    pressure = (total_impulse / delta_eq) / simulation_perimeter
    pressures.append(pressure)
    time_steps.append(delta_eq * (current_delta_eq_index + 1))

    return pressures, time_steps


def pressure_vs_equilibrium_time_plot(particles, threshold, equilibrium_time, delta_eq):
    velocities = [0.005, 0.01, 0.02, 0.025, 0.03, 0.035]
    # velocities = [0.01, 0.02, 0.025]
    legends = []
    for velocity in velocities:
        pressures, time_steps = pressures_every_delta_eq(particles, threshold, velocity, equilibrium_time, delta_eq)        

        # Plot
        plt.plot(time_steps, pressures)
        legends.append(f"Presión con V0 = {velocity}")

    plt.legend(legends)
    plt.xlabel("Tiempo de equilibrio (s)")
    plt.ylabel("Presión (N/m)")
    plt.show()
    plt.close()
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)
    parser.add_argument("--threshold", default=0.05,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.05.", dest="threshold", required=False)
    parser.add_argument("--equilibrium-time", default=100,
                        help="Time to reach from the equilibrium state of the simulations, in seconds. Defaults to 10 seconds.", dest="equilibrium_time", required=False)
    parser.add_argument("--delta-eq", default=5,
                        help="The delta used to calculate the equilibrium state. Defaults to 0.1 seconds.", dest="delta_eq", required=False)
    args = parser.parse_args()

    pressure_vs_equilibrium_time_plot(int(args.particles), float(
        args.threshold), float(args.equilibrium_time), float(args.delta_eq))
