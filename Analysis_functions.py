import numpy as np


def dot(p1, p2):
    """
    Dot product for 4-vectors of the form (E, px, py, pz).
    Returns: E1*E2 - p1*p2
    """
    return p1[0] * p2[0] - p1[1] * p2[1] - p1[2] * p2[2] - p1[3] * p2[3]

def versor(p):
    """
    Returns the versor of the vector.
    """
    return p / np.linalg.norm(p)

def get_particles(particles, pdg):
    return [particle for particle in particles if particle.pdg == pdg]
