
from ...helpers import parse_static_file


def is_left_particle(x_coordinate, box_width):
    return x_coordinate < (box_width / 2)


def left_particles_counter(simulation_dynamic_output_file_name, simulation_static_output_file_name):
    left_particle_count = []
    # Store every time step in the simulation
    time_steps = []
    current_number_of_time_step = -1

    simulation = parse_static_file(
        simulation_static_output_file_name)

    box_width = simulation.box_width
    particle_count = simulation.particle_count

    with open(simulation_dynamic_output_file_name) as simulation_file:
        for line_number, line in enumerate(simulation_file):
            line_data = line.split()
            if len(line_data) == 1:
                time_steps.append(float(line_data[0]))
                left_particle_count.append(0)
                current_number_of_time_step += 1
            else:
                # Count if left particle
                x = float(line_data[0])
                if is_left_particle(x, box_width):
                    left_particle_count[current_number_of_time_step] += 1

    left_particle_fraction = []
    right_particle_fraction = []

    for i in range(len(left_particle_count)):
        left_particle_fraction.append(left_particle_count[i] / particle_count)
        right_particle_fraction.append(1 - left_particle_fraction[i])

    return left_particle_fraction, right_particle_fraction, time_steps
