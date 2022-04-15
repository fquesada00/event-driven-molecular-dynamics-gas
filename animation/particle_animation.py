import argparse


def write_animation(out_filename, input_file):
    xyz_file = open(out_filename, "w")
    with input_file as simulation_steps_file:
        for i, line in enumerate(simulation_steps_file):
            if i == 0:
                N = int(line.split()[0])
            elif i > 2:
                line_data = line.split()

                # timestep
                if len(line_data) == 1:
                    xyz_file.write(f'{N}\ncomment\n')
                else:
                    xyz_file.write(line)

    xyz_file.close()


def write_walls(out_filename, input_file):
    walls_xyz_file = open(out_filename, "w")

    with input_file as simulation_steps_file:
        for i, line in enumerate(simulation_steps_file):
            if i == 1:
                box_width, box_height = [
                    float(dimension) for dimension in line.split()]
            elif i == 2:
                slit_width = float(line.split()[0])
            elif i > 2:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType('r'),
                        default=None, help="File of simulation timesteps", dest="simulation_steps", required=True)
    parser.add_argument("--output", type=str,
                        default="particles.xyz", help="Desired file name for XYZ output", dest="out_file_name", required=False)

    args = parser.parse_args()

    write_animation(args.out_file_name, args.simulation_steps)
