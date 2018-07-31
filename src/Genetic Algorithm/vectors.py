import numpy as np
import numpy.linalg as la
import krpc
import math
from decimal import Decimal

def cross_product(u, v):
    return (u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0])

def dot_product(u, v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

def magnitude(v):
    return math.sqrt(dot_product(v, v))

def angle_between_vectors(u, v):
    """ Compute the angle between vector u and v """
    dp = dot_product(u, v)
    if dp == 0:
        return 0
    um = magnitude(u)
    vm = magnitude(v)
    return math.acos(dp / (um*vm)) * (180. / math.pi)

def calc_rot(conn,docking_target, main_target):

    vessel_direction = docking_target.direction(main_target.surface_reference_frame)
    # Compute the roll
    # Compute the plane running through the vessels direction
    # and the upwards direction
    up = (1, 0, 0)
    plane_normal = cross_product(vessel_direction, up)
    # Compute the upwards direction of the vessel
    vessel_up = conn.space_center.transform_direction(
        (0, 0, -1), docking_target.reference_frame, main_target.surface_reference_frame)
    # Compute the angle between the upwards direction of
    # the vessel and the plane normal
    roll = angle_between_vectors(vessel_up, plane_normal)
    # Adjust so that the angle is between -180 and 180 and
    # rolling right is +ve and left is -ve

    if vessel_up[0] > 0:
        roll -=90
        roll *= -1
    else:
        roll -=90
        roll -=180

    return roll