import numpy as np


# ---  Radiative Heat Gain ---

# Constants
sigma = 5.67e-8  # Stefan-Boltzmann constant (W/m²K⁴)
epsilon = 0.95  # Emissivity of hand warmer surface


def calculate_view_factor(A1, A2, Dx, Dy, Dz, angle):
    """
    Calculate the view factor between a horizontal and a tilted rectangular surface.

    Parameters:
    - A1: Area of the first surface (horizontal)
    - A2: Area of the second surface (tilted)
    - Dx: Horizontal distance between the center points of the surfaces
    - Dy: Vertical distance between the center points of the surfaces
    - Dz: Depth distance (distance along the height)
    - angle: Tilt angle of the second surface relative to horizontal (degrees)

    Returns:
    - F12: View factor from surface 1 to surface 2
    """
    # convert tilt angle to radians
    theta = np.radians(angle)

    # x2 = Dx
    # y2 = Dy + Dz * np.cos(theta)
    # z2 = Dz * np.sin(theta)

    # get direct distance between the centers
    d = np.sqrt(Dx**2 + Dy**2 + Dz**2)

    # Normalize areas for simplification
    L1 = np.sqrt(A1)
    L2 = np.sqrt(A2)

    cos_theta = np.cos(theta)
    # sin_theta = np.sin(theta)

    # simplified view factor formula
    F12 = (cos_theta / (np.pi * d**2)) * (L1 * L2)

    F12 = max(min(F12, 1.0), 0.0)
    return F12


def radiative_heat_gain(A_device, A_hand, T_device, T_hand, d_x, d_y, d_z, theta):
    """
    Calculate the radiative heat flux between two surfaces.
    A_device: Area of the radiant device surface (m²)
    A_hand: Approximated area of the hand surface (m²)
    T_device: Temperature of the handwarmer surface (Kelvin)
    T_hand: Temperature of the hand (Kelvin)
    d_x: X distance between the center points of the surfaces (m)
    d_y: Y distance between the center points of the surfaces (m)
    d_z: Z distance between the center points of the surfaces (m)
    alpha_deg: Angle of the handwarmer surface (degrees)
    """

    F = calculate_view_factor(A_hand, A_device, d_x, d_y, d_z, theta)

    print(f"Angle: {theta:.1f}°"),
    print(f"View factor: {F:.3f}"),

    T_device_k = T_device + 273.15
    T_hand_k = T_hand + 273.15

    # Radiative heat gain rate (W)
    Q_rad = epsilon * sigma * F * A_device * (T_device_k**4 - T_hand_k**4)
    return Q_rad


# ---  Convective Heat Loss Calculation ---


def convective_heat_loss(T_hand, T_air, A_hand, h=10):
    """
    Calculate the convective heat loss between the hand and surrounding air.
    T_hand: Temperature of the hand (°C)
    T_air: Temperature of the surrounding air (°C)

    """
    T_hand_k = T_hand + 273.15
    T_air_k = T_air + 273.15

    # Convective heat loss rate (W)
    Q_conv = h * A_hand * (T_hand_k - T_air_k)
    return -Q_conv  # to plot in negative y-direction
