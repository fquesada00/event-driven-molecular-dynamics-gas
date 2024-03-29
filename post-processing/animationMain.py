import argparse
from .animation.particle_animation import find_delta_t, write_walls, write_animation
from .helpers import parse_static_file
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-input", type=str,
                        default=None, help="File of simulation static data.", dest="simulation_static_data", required=True)
    parser.add_argument("--dynamic-input", type=argparse.FileType('r'),
                        default=None, help="File of simulation timesteps.", dest="simulation_steps", required=True)
    parser.add_argument("--output", type=str,
                        default="particles.xyz", help="Desired file name for XYZ output.", dest="out_file_name", required=False)
    parser.add_argument("--output-walls", type=str,
                        default="walls.xyz", help="Desired file name for walls XYZ output.", dest="walls_out_file_name", required=False)

    args = parser.parse_args()
    simulation = parse_static_file(args.simulation_static_data)
    write_walls(args.walls_out_file_name, simulation)
    delta_t = find_delta_t(args.simulation_steps)
    print(f"Delta t: {delta_t}")
    write_animation(args.out_file_name, args.simulation_steps,
                    simulation.particle_count, simulation.particle_radius, simulation.particle_mass, simulation.box_width, delta_t)
    args.simulation_steps.close()
