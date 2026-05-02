from tudatpy import constants
from tudatpy.interface import spice
from tudatpy.numerical_simulation import environment_setup, propagation_setup


spice.load_standard_kernels()

initial_epoch = spice.convert_date_string_to_ephemeris_time()

global_frame_origin = "SSB"
global_frame_orientation = "ECLIPJ2000"

vehicle_settings = {
    "mass": 4000.0,  # [kg]
    "specific_impulse": 3000.0,  # [s]
    "reflectivity_coefficient": 1.2,  # [-]
    "area": 85,  # [m**2]
}


acceleration_settings_on_vehicle = {
    "Sun": [
        propagation_setup.acceleration.point_mass_gravity(),
        propagation_setup.acceleration.relativistic_correction(
            use_schwarzschild=True,
            use_lense_thirring=False,
            use_de_sitter=False,
        ),
        propagation_setup.acceleration.radiation_pressure(),
    ],
    "Vehicle": [
        propagation_setup.acceleration.thrust_from_engine("LowThrustEngine")
    ],
    "Mercury": [
        propagation_setup.acceleration.point_mass_gravity()
    ],
    "Venus": [
        propagation_setup.acceleration.point_mass_gravity()
    ],
    "Earth": [
        propagation_setup.acceleration.spherical_harmonic_gravity(2, 0),
    ],
    "Moon": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Mars": [
        propagation_setup.acceleration.point_mass_gravity()
    ],
    "Ceres": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Vesta": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "MainAsteroidBelt": [
        propagation_setup.acceleration.ring_gravity()
    ],
    "Jupiter": [
        propagation_setup.acceleration.spherical_harmonic_gravity(2, 0)
    ],
    "Io": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Europa":[
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Ganymede": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Callisto": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Saturn": [
        propagation_setup.acceleration.point_mass_gravity(),
    ],
    "Uranus": [
        propagation_setup.acceleration.point_mass_gravity()
    ],
    "Neptune": [
        propagation_setup.acceleration.point_mass_gravity()
    ],
}

gravity_field_settings = {
    "Saturn": environment_setup.gravity_field.central(
        spice.get_body_gravitational_parameter("SATURN BARYCENTER")
    )
}

ephemeris_settings = {
    "Mercury": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - 16 * constants.JULIAN_DAY,
        final_epoch + 16 * constants.JULIAN_DAY,
        2 * constants.JULIAN_DAY,
    ),
    "Venus": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - 49 * constants.JULIAN_DAY,
        final_epoch + 49 * constants.JULIAN_DAY,
        7 * constants.JULIAN_DAY,
    ),
    "Jupiter": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - constants.JULIAN_DAY,
        final_epoch + constants.JULIAN_DAY,
        5 * constants.JULIAN_DAY,
        body_name_to_use="JUPITER BARYCENTER",
    ),
    "Saturn": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - constants.JULIAN_DAY,
        final_epoch + constants.JULIAN_DAY,
        25 * constants.JULIAN_DAY,
        body_name_to_use="SATURN BARYCENTER",
    ),
    "Uranus": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - constants.JULIAN_DAY,
        final_epoch + constants.JULIAN_DAY,
        100 * constants.JULIAN_DAY,
        body_name_to_use="URANUS BARYCENTER",
    ),
    "Neptune": environment_setup.ephemeris.interpolated_spice(
        initial_epoch - constants.JULIAN_DAY,
        final_epoch + constants.JULIAN_DAY,
        100 * constants.JULIAN_DAY,
        body_name_to_use="NEPTUNE BARYCENTER",
    ),
}

solar_system_bodies = [
    "Sun",
    "Mercury",
    "Venus",
    "Earth",
    "Moon",
    "Mars",
    "Deimos",
    "Phobos",
    "Jupiter",
    "Io",
    "Europa",
    "Ganymede",
    "Callisto",
    "Saturn",
    "Titan",
    "Rhea",
    "Iapetus",
    "Dione",
    "Tethys",
    "Enceladus",
    "Mimas",
    "Hyperion",
    "Amalthea",
    "Uranus",
    "Neptune",
    "Ceres",
    "Vesta",
    "Pallas",
]

main_asteroid_belt_total_mass_factor = 4.0079e-4  # From Pitjeva and Pitjev (2018)
main_asteroid_belt_mean_radius = 2.8 * constants.ASTRONOMICAL_UNIT  # From Kuchynka et al. (2010)