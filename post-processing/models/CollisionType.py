from enum import Enum


class ColissionType(Enum):
    PARTICLE_X_WALL_COLLISION = 0
    PARTICLE_Y_WALL_COLLISION = 1
    PARTICLES_COLLISION = 2