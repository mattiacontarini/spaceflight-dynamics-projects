
import numpy as np
import os

from setup import EnvironmentConfig as EnvConfig

from tudatpy import astro
from tudatpy.interface import spice


class TransferProblem:
    """
    Class representing an Earth-Jupiter interplanetary transfer multi-objective optimisation problem. The interplanetary
    transfer trajectory includes flybys of the Solar System planets in the following order:
        - launch from Kourou, French Guyana, on an escape trajectory
        - flyby at Venus
        - flyby at Earth
        - flyby at Earth
        - arrival at Jupiter

    The problem is first solved analytically with the method of the patched conics. The analytical solution can then be
    numerically integrated.

    Input parameters:

    Objective functions: total ToF and total Delta-V

    Control variables:
        - departure epoch
        - time of flight leg 1 (Earth - Venus)
        - time of flight leg 2 (Venus - Earth)
        - time of flight leg 3 (Earth - Earth)
        - time of flight leg 4 (Earth - Jupiter)

    """

    def __init__(
            self,
            bodies,
            ):
        control_variables = ...


    def get_departure_deltav(self,
                             departure_epoch,
                             time_of_flight,
                             ):
        earth_state = spice.get_body_cartesian_state_at_epoch(
            "Earth",
            EnvConfig.global_frame_origin,
            EnvConfig.global_frame_orientation,
            "None",
            departure_epoch
        )
        earth_position = earth_state[:3]
        venus_position = spice.get_body_cartesian_position_at_epoch(
            "Venus",
            EnvConfig.global_frame_origin,
            EnvConfig.global_frame_orientation,
            "None",
            departure_epoch + time_of_flight
        )
        sun_gravitational_parameter = spice.get_body_gravitational_parameter("Sun")
        earth_venus_targeter = astro.two_body_dynamics.LambertTargeterIzzo(
            earth_position,
            venus_position,
            departure_epoch,
            sun_gravitational_parameter,
        )
        radial_departure_velocity = earth_venus_targeter.get_radial_departure_velocity()
        transverse_departure_velocity = earth_venus_targeter.get_transverse_departure_velocity()
        earth_velocity = earth_state[3:]
        departure_speed = np.sqrt(radial_departure_velocity**2 + transverse_departure_velocity**2)
        hyperbolic_excess_speed = departure_speed - np.linalg.norm(earth_velocity)




    def fitness(self,
                control_variables
                ):

        ...




    def propagate_trajectory(
            self,
            initial_state
            ):
        ...
