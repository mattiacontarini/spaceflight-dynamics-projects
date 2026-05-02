
import numpy as np

from setup import EnvironmentConfig as EnvConfig

from tudatpy import numerical_simulation
from tudatpy import constants
from tudatpy.interface import spice

def get_bodies(body_settings=None):

    # Retrieve body settings
    if body_settings is None:
        body_settings = get_body_settings()

    # Create system of bodies
    bodies = numerical_simulation.environment_setup.create_system_of_bodies(
        body_settings
    )

    # Create vehicle object and add it to the system of bodies
    bodies.create_empty_body("Vehicle")
    bodies.get_body('Vehicle').mass = EnvConfig.vehicle_settings["mass"]
    thrust_magnitude_settings = (
        numerical_simulation.propagation_setup.thrust.custom_thrust_magnitude_fixed_isp(
            lambda time: 0.0,
            EnvConfig.vehicle_settings["specific_impulse"]
        )
    )
    numerical_simulation.environment_setup.add_engine_model(
        'Vehicle',
        'LowThrustEngine',
        thrust_magnitude_settings,
        bodies
    )
    numerical_simulation.environment_setup.add_rotation_model(
        bodies,
        'Vehicle',
        numerical_simulation.environment_setup.rotation_model.custom_inertial_direction_based(
            lambda time: np.array([1, 0, 0]),
            EnvConfig.global_frame_orientation,
            'VehcleFixed'))

    return bodies



def get_body_settings():
    global_frame_origin = EnvConfig.global_frame_origin
    global_frame_orientation = EnvConfig.global_frame_orientation

    bodies_to_create = [
        body
        for body in list(EnvConfig.acceleration_settings_on_vehicle) if body in EnvConfig.solar_system_bodies
    ]

    body_settings = numerical_simulation.environment_setup.get_default_body_settings(
        bodies_to_create,
        global_frame_origin,
        global_frame_orientation
    )

    if "MainAsteroidBelt" in list(EnvConfig.acceleration_settings_on_vehicle):

        body_settings.add_empty_settings('MainAsteroidBelt')
        body_settings.get('MainAsteroidBelt').ephemeris_settings = numerical_simulation.environment_setup.ephemeris.constant(
            [0, 0, 0, 0, 0, 0]
        )

        Earth_gravitational_parameter = spice.get_body_gravitational_parameter("Earth")
        main_asteroid_belt_gravitational_parameter = EnvConfig.main_asteroid_belt_total_mass_factor * Earth_gravitational_parameter
        if "Ceres" or "Vesta" or "Pallas" or "Hygiea" in list(EnvConfig.acceleration_settings_on_vehicle):
            if "Ceres" in list(EnvConfig.acceleration_settings_on_vehicle):
                main_asteroid_belt_gravitational_parameter -= spice.get_body_gravitational_parameter("Ceres")
            if "Vesta" in list(EnvConfig.acceleration_settings_on_vehicle):
                main_asteroid_belt_gravitational_parameter -= spice.get_body_gravitational_parameter("Vesta")
            if "Pallas" in list(EnvConfig.acceleration_settings_on_vehicle):
                main_asteroid_belt_gravitational_parameter -= spice.get_body_gravitational_parameter("Pallas")
            if "Hygiea" in list(EnvConfig.acceleration_settings_on_vehicle):
                main_asteroid_belt_gravitational_parameter -= spice.get_body_gravitational_parameter("Hygiea")
        body_settings.get("MainAsteroidBelt").gravity_field_settings = numerical_simulation.environment_setup.gravity_field.ring_model(
            gravitational_parameter=main_asteroid_belt_gravitational_parameter,
            ring_radius=EnvConfig.main_asteroid_belt_mean_radius,
            associated_reference_frame=EnvConfig.global_frame_orientation,
            elliptic_integral_s_from_d_and_b=True
        )


    return body_settings