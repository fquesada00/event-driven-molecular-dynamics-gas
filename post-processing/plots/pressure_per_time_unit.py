
import argparse
import os
import matplotlib.pyplot as plot


def pressure_per_time_unit_plot(threshold, time_unit, particles):
    print(
        f"Running simulation with {particles} particles, {threshold} left particles fraction threshold and {time_unit} time unit.")

    simulation_output_file_name = "simulation.txt"
    cmd = f"java -DnumberOfParticles={particles} -DleftParticlesFractionThreshold={threshold} -DsimulationOutFileName={simulation_output_file_name} -jar ../target/event-driven-molecular-dynamics-gas-1.0-SNAPSHOT.jar"
    print(f"Executing: {cmd}")
    os.system(cmd)
    print("Done")

    prev_time_step = 0.0
    next_time_step = prev_time_step + time_unit
    time_steps = []
    pressure_per_time_unit = []
    wall_length = 0
    total_events_on_current_time_step = 0
    total_wall_momentum = 0
    with open(simulation_output_file_name) as simulation_file:
        for line_number, line in enumerate(simulation_file):
            # Skip particle count
            if line_number == 0:
                continue
            elif line_number == 1:
                box_width, box_height = [
                    float(dimension) for dimension in line.split()]
                wall_length = box_height * 2 + box_width * 2
            elif line_number == 2:
                slit_width = float(line.split()[0])
            elif len(line.split()) == 2:
                line_data = line.split()

                # Get time step and wall momentum
                time_step = float(line_data[0])
                momentum = float(line_data[1])

                # print(f"Time step: {time_step} - Wall momentum: {momentum} - Prev time step: {prev_time_step} - Next time step: {next_time_step}")

                # Check if time step is in the range
                if time_step >= prev_time_step and time_step < next_time_step:
                    total_events_on_current_time_step += 1
                    total_wall_momentum += momentum
                else:
                    # Log previous time step pressure
                    time_steps.append(prev_time_step + time_unit)
                    pressure_per_time_unit.append(
                        ((total_wall_momentum / total_events_on_current_time_step) / time_unit) / wall_length)

                    # Go to next time step and reset counters
                    total_wall_momentum = momentum
                    total_events_on_current_time_step = 1
                    prev_time_step = next_time_step
                    next_time_step = prev_time_step + time_unit

    # Log last time step pressure
    time_steps.append(prev_time_step + time_unit)
    pressure_per_time_unit.append(
        ((total_wall_momentum / total_events_on_current_time_step) / time_unit) / wall_length)

    
    # Plot pressure per time unit
    plot.plot(time_steps, pressure_per_time_unit)
    plot.xlabel("Tiempo (s)")
    plot.ylabel("Presión (N/m)")
    plot.show()
    plot.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--threshold", default=0.5,
                        help="The threshold of the left particles fraction used in the simulations. Defaults to 0.5.", dest="threshold", required=False)
    parser.add_argument("--time_unit", default=1,
                        help="The frequency of the samples, in seconds. Defaults to 1.", dest="time_unit", required=False)
    parser.add_argument("--particles", default=100,
                        help="The number of particles used in the simulations. Defaults to 100.", dest="particles", required=False)

    args = parser.parse_args()

    pressure_per_time_unit_plot(float(args.threshold), float(
        args.time_unit), int(args.particles))
