import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

from src.functions import (
    radiative_heat_gain,
    convective_heat_loss,
    calculate_view_factor,
    plot_geometry_plotly,
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div(
    [
        html.H1("Handwarmer Heat Gain Calculator", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Device Temperature (°C)"),
                dcc.Input(id="T_device", type="number", value=70, step=1),
                html.Br(),
                html.Label("Hand Temperature (°C)"),
                dcc.Input(id="T_hand", type="number", value=33, step=1),
                html.Br(),
                html.Label("Air Temperature (°C)"),
                dcc.Input(id="T_air", type="number", value=20, step=1),
                html.Br(),
                html.Label("Device Surface Area (m²)"),
                dcc.Input(id="A_device", type="number", value=0.007, step=0.001),
                html.Br(),
                html.Label("Hand Surface Area (m²)"),
                dcc.Input(id="A_hand", type="number", value=0.015, step=0.001),
                html.Br(),
                html.Label("X Distance (m)"),
                dcc.Input(id="d_x", type="number", value=0.0, step=0.01),
                html.Br(),
                html.Label("Y Distance (m)"),
                dcc.Input(id="d_y", type="number", value=0.0, step=0.01),
                html.Br(),
                html.Label("Z Distance (m)"),
                dcc.Input(id="d_z", type="number", value=0.1, step=0.01),
                html.Br(),
                html.Label("Angle Handwarmer (degrees)"),
                dcc.Input(id="theta", type="number", value=0, step=5),
                html.Br(),
                html.Label("Convective Heat Transfer Coefficient (W/m²K)"),
                dcc.Input(id="h", type="number", value=5, step=1),
            ],
            style={"columnCount": 2},
        ),
        html.Hr(),
        html.Div(
            [
                html.H3("Results"),
                html.P(id="q_rad_output"),
                html.P(id="q_conv_output"),
                # html.P(id="view_factor"),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="heat_gain_rate_chart"),
                    width={"size": 4},
                ),
                dbc.Col(
                    dcc.Graph(id="geometry_chart"),
                    width={"size": 8},
                ),
            ],
        ),
    ]
)


@app.callback(
    [
        Output("q_rad_output", "children"),
        Output("q_conv_output", "children"),
        # Output("view_factor", "children"),
        Output("heat_gain_rate_chart", "figure"),
        Output("geometry_chart", "figure"),
    ],
    [
        Input("T_device", "value"),
        Input("T_hand", "value"),
        Input("T_air", "value"),
        Input("A_device", "value"),
        Input("A_hand", "value"),
        Input("d_x", "value"),
        Input("d_y", "value"),
        Input("d_z", "value"),
        Input("theta", "value"),
        Input("h", "value"),
    ],
)
def update_output(
    T_device,
    T_hand,
    T_air,
    A_device,
    A_hand,
    d_x,
    d_y,
    d_z,
    theta,
    h,
):
    Q_rad = radiative_heat_gain(
        A_device, A_hand, T_device, T_hand, d_x, d_y, d_z, theta
    )
    Q_conv = convective_heat_loss(T_hand, T_air, A_hand, h)
    view_factor = calculate_view_factor(A_hand, A_device, d_x, d_y, d_z, theta)
    print(f"Radiative Heat Gain Rate: {Q_rad:.2f} W")
    print(f"Convective Heat Loss Rate: {Q_conv:.2f} W")
    print(f"Device Area (A_device): {A_device:.3f} m²"),
    print(f"Hand Area (A_hand): {A_hand:.3f} m²"),

    bar_chart = go.Figure(
        data=[
            go.Bar(
                name="Radiative Heat Gain",
                x=["Radiative Heat Gain"],
                y=[Q_rad],
                marker_color="orange",
            ),
            go.Bar(
                name="Convective Heat Loss",
                x=["Convective Heat Loss"],
                y=[Q_conv],
                marker_color="blue",
            ),
        ]
    )
    bar_chart.update_layout(
        title="Heat Gain/Loss Contributions",
        xaxis_title="Heat Gain/Loss Type",
        yaxis_title="Heat Gain Rate (W)",
        yaxis_range=[-7.5, 7.5],
        barmode="group",
    )

    geometry_chart = plot_geometry_plotly(
        d_x, d_y, d_z, theta, A_hand, A_device, view_factor
    )

    return (
        f"Radiative Heat Gain (Q_rad): {Q_rad:.2f} W",
        f"Convective Heat Loss (Q_conv): {Q_conv:.2f} W",
        # f"View Factor (F12): {view_factor:.2f}",
        bar_chart,
        geometry_chart,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
