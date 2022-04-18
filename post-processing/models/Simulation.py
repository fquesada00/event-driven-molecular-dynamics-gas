class Simulation():
    def __init__(self, particle_count, box_width, box_height, slit_width, particle_mass, particle_radius):
        self._particle_count = particle_count
        self._box_width = box_width
        self._box_height = box_height
        self._slit_width = slit_width
        self._particle_mass = particle_mass
        self._particle_radius = particle_radius
    
    @property
    def particle_count(self):
        return self._particle_count

    @property
    def box_width(self):
        return self._box_width

    @property
    def box_height(self):
        return self._box_height

    @property
    def slit_width(self):
        return self._slit_width

    @property
    def particle_mass(self):
        return self._particle_mass

    @property
    def particle_radius(self):
        return self._particle_radius

    def __str__(self):
        return "Simulation: particle_count = {}, box_width = {}, box_height = {}, slit_width = {}, particle_mass = {}, particle_radius = {}".format(
            self.particle_count, self.box_width, self.box_height, self.slit_width, self.particle_mass, self.particle_radius)

    