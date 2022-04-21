import argparse
from .animation.particle_animation import write_walls, write_animation
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
    write_animation(args.out_file_name, args.simulation_steps,
                    simulation.particle_count)
    args.simulation_steps.close()
