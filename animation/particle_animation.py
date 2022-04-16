import argparse


def write_animation(out_filename, input_file):
    xyz_file = open(out_filename, "w")
    input_file.seek(0)
    for i, line in enumerate(input_file):
        if i == 0:
            N = int(line.split()[0])
        elif i > 2:
            line_data = line.split()

            # timestep and momentum
            if len(line_data) == 2:
                xyz_file.write(f'{N}\ncomment\n')
            else:
                xyz_file.write(line)

    xyz_file.close()


def write_walls(out_filename, input_file):
    walls_xyz_file = open(out_filename, "w")
    input_file.seek(0)
    for i, line in enumerate(input_file):
        if i == 1:
            box_width, box_height = [
                float(dimension) for dimension in line.split()]
        elif i == 2:
            slit_width = float(line.split()[0])
        elif i > 2:
            break

    number_of_particles = (box_height / 0.01) * 3 + \
        (box_width / 0.01) * 2 - slit_width / 0.01
    walls_xyz_file.write(f'{int(number_of_particles)}\ncomment\n')
    h = 0.0
    while h < box_height:
        walls_xyz_file.write(f'0 {h}\n')
        walls_xyz_file.write(f'{box_width} {h}\n')
        if h > ((box_height + slit_width) / 2) or h < ((box_height - slit_width) / 2):
            walls_xyz_file.write(f'{box_width/2} {h}\n')
        h += 0.01

    w = 0.0
    while w < box_width:
        walls_xyz_file.write(f'{w} 0\n')
        walls_xyz_file.write(f'{w} {box_height}\n')
        w += 0.01

    walls_xyz_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=argparse.FileType('r'),
                        default=None, help="File of simulation timesteps", dest="simulation_steps", required=True)
    parser.add_argument("--output", type=str,
                        default="particles.xyz", help="Desired file name for XYZ output", dest="out_file_name", required=False)
    parser.add_argument("--output-walls", type=str,
                        default="walls.xyz", help="Desired file name for walls XYZ output", dest="walls_out_file_name", required=False)

    args = parser.parse_args()
    write_walls(args.walls_out_file_name, args.simulation_steps)
    write_animation(args.out_file_name, args.simulation_steps)
    args.simulation_steps.close()
