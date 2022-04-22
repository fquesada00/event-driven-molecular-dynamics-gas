import argparse

from ..helpers import parse_static_file


def write_animation(out_filename, input_file, N, radius, mass, box_width):
    xyz_file = open(out_filename, "w")
    input_file.seek(0)
    for i, line in enumerate(input_file):
        line_data = line.split()
        # timestep and momentum
        if len(line_data) == 1:
            xyz_file.write(f'{N}\ncomment\n')
        else:
            color = [255, 0, 0] if float(
                line_data[0]) > (box_width / 2) else [0, 0, 255]
            xyz_file.write(
                f"{line[:-2]} {mass} {radius} {color[0]} {color[1]} {color[2]}\n")

    xyz_file.close()


def write_walls(out_filename, static_data):
    walls_xyz_file = open(out_filename, "w")

    box_width = static_data.box_width
    box_height = static_data.box_height
    slit_width = static_data.slit_width

    number_of_particles = (box_height / 0.001) * 3 + \
        (box_width / 0.001) * 2 - slit_width / 0.001
    walls_xyz_file.write(f'{int(number_of_particles)}\ncomment\n')
    h = 0.0
    while h <= box_height:
        walls_xyz_file.write(f'0 {h}\n')
        walls_xyz_file.write(f'{box_width} {h}\n')
        if h > ((box_height + slit_width) / 2) or h < ((box_height - slit_width) / 2):
            walls_xyz_file.write(f'{box_width/2} {h}\n')
        h += 0.001

    w = 0.0
    while w <= box_width:
        walls_xyz_file.write(f'{w} 0\n')
        walls_xyz_file.write(f'{w} {box_height}\n')
        w += 0.001

    walls_xyz_file.close()
