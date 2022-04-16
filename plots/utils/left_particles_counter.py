
def is_left_particle(x_coordinate, box_width):
    return x_coordinate < (box_width / 2)


def left_particles_counter(simulation_file_name, log_every_n_time_steps=1):
    left_particle_count = []
    time_steps = []
    discrete_time_steps = []
    current_number_of_time_step = 0
    with open(simulation_file_name) as simulation_file:
        for line_number, line in enumerate(simulation_file):
            if line_number == 0:
                particle_count = int(line.split()[0])
            elif line_number == 1:
                box_width, box_height = [
                    float(dimension) for dimension in line.split()]
            elif line_number == 2:
                slit_width = float(line.split()[0])
            else:
                line_data = line.split()
                log = (current_number_of_time_step %
                       log_every_n_time_steps) == 0
                current_index = int(
                    current_number_of_time_step / log_every_n_time_steps)
                if len(line_data) == 1:
                    time_steps.append(float(line_data[0]))
                    current_number_of_time_step += 1
                    if log:
                        discrete_time_steps.append(current_index)
                        left_particle_count.append(0)
                elif log:
                    # Count if left particle
                    x = float(line_data[0])
                    if is_left_particle(x, box_width):
                        left_particle_count[current_index - 1] += 1
                

    left_particle_fraction = []
    right_particle_fraction = []
    is_total_time_steps_divisible_by_log_frequency = current_number_of_time_step % log_every_n_time_steps == 0
    for i in range(len(left_particle_count)):
        if not is_total_time_steps_divisible_by_log_frequency and i == (len(left_particle_count) - 1):
            discrete_time_steps.pop()
            break
        left_particle_fraction.append(left_particle_count[i] / particle_count)
        right_particle_fraction.append(1 - left_particle_fraction[i])


    return left_particle_fraction, right_particle_fraction, discrete_time_steps
