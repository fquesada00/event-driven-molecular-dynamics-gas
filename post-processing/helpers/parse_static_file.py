from ..models import Simulation

def parse_static_file(file_path):
    with open(file_path) as file:
        for line_number, line in enumerate(file):
            if line_number == 0:
                particle_count = int(line.split()[0])
            elif line_number == 1:
                box_width, box_height= [
                    float(dimension) for dimension in line.split()]
            elif line_number == 2:
                slit_width = float(line.split()[0])
            elif line_number == 3:
                particle_mass = float(line.split()[0])
            elif line_number == 4:
                particle_radius = float(line.split()[0])
            else:
                break
    return Simulation(particle_count, box_width, box_height, slit_width, particle_mass, particle_radius)