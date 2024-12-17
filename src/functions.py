import numpy as np

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import plotly.graph_objects as go


# ---  Radiative Heat Gain ---

# radiation constants
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

    theta = np.radians(angle)

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
    Q_radinf = epsilon * sigma * (1 - F) * A_device * (T_device_k**4 - 293**4)
    print(Q_radinf)
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


# ---  Plot geometry configuration ---


def plot_geometry_plotly(Dx, Dy, Dz, angle_deg, A1, A2, view_factor):
    """
    Visualize the geometry of two surfaces: a horizontal surface (hand) and a tilted surface (handwarmer) using Plotly.

    Parameters:
    - Dx: Horizontal distance between the centers of the surfaces in the x-direction (m)
    - Dy: Horizontal distance between the centers of the surfaces in the y-direction (m)
    - Dz: Vertical distance between the surfaces (m)
    - angle_deg: Tilt angle of the second surface (degrees)
    - A1: Area of the first surface (m²)
    - A2: Area of the second surface (m²)
    """

    angle_rad = np.radians(angle_deg)

    # dimensions of the rectangles assuming they are squares
    L1 = np.sqrt(A1)
    L2 = np.sqrt(A2)

    # center of the hand rectangle (at the origin)
    hand_center = np.array([0, 0, 0])
    hand_corners = np.array(
        [
            [-L1 / 2, -L1 / 2, 0],
            [L1 / 2, -L1 / 2, 0],
            [L1 / 2, L1 / 2, 0],
            [-L1 / 2, L1 / 2, 0],
        ]
    )

    # center of the handwarmer rectangle
    handwarmer_center = np.array([Dx, Dy, Dz])
    handwarmer_corners = (
        np.array(
            [
                [L2 / 2, L2 / 2 * np.cos(angle_rad), L2 / 2 * np.sin(angle_rad)],
                [-L2 / 2, L2 / 2 * np.cos(angle_rad), L2 / 2 * np.sin(angle_rad)],
                [-L2 / 2, -L2 / 2 * np.cos(angle_rad), -L2 / 2 * np.sin(angle_rad)],
                [L2 / 2, -L2 / 2 * np.cos(angle_rad), -L2 / 2 * np.sin(angle_rad)],
            ]
        )
        + handwarmer_center
    )

    fig = go.Figure()

    # hand rectangle
    fig.add_trace(
        go.Mesh3d(
            x=hand_corners[:, 0],
            y=hand_corners[:, 1],
            z=hand_corners[:, 2],
            color="blue",
            opacity=0.5,
            name="Hand Surface",
            flatshading=True,
            showlegend=True,
        )
    )

    # handwarmer rectangle
    fig.add_trace(
        go.Mesh3d(
            x=handwarmer_corners[:, 0],
            y=handwarmer_corners[:, 1],
            z=handwarmer_corners[:, 2],
            color="red",
            opacity=0.5,
            name="Handwarmer Surface",
            flatshading=True,
            showlegend=True,
        )
    )

    # line connecting centers
    fig.add_trace(
        go.Scatter3d(
            x=[hand_center[0], handwarmer_center[0]],
            y=[hand_center[1], handwarmer_center[1]],
            z=[hand_center[2], handwarmer_center[2]],
            mode="lines",
            line=dict(color="black", dash="dash"),
            name="Center Distance",
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="X (m)",
            xaxis=dict(range=[-0.2, 0.2]),
            yaxis_title="Y (m)",
            yaxis=dict(range=[-0.2, 0.2]),
            zaxis_title="Z (m)",
            zaxis=dict(range=[0, 0.2]),
            aspectmode="cube",
        ),
        title=f"Resulting View Factor (F12): {view_factor:.2f}",
        showlegend=True,
        width=800,
        height=800,
    )

    fig.update_legends(
        dict(
            x=0,
            y=1,
            traceorder="normal",
            orientation="h",
            font=dict(
                size=12,
            ),
            bgcolor="rgba(0,0,0,0)",
        )
    )

    return fig
