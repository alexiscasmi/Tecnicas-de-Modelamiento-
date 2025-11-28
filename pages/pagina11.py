import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

from styles import INPUT_STYLE_COMPACT, INFO_CARD_STYLE

dash.register_page(
    __name__,
    name="PROYECTO 2.2",
    path="/proyecto-sir"   
)

LABEL_STYLE = {
    "color": "#4A4A4A",
    "fontWeight": "600",
    "fontSize": "1rem",
}

# ===========================================================
# LAYOUT COMPLETO
# ===========================================================

layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [

                    # =====================================================
                    #     TITULO PRINCIPAL
                    # =====================================================
                    html.H2(
                        "Modelo Epidemiológico SIR - ASIGNACION 2",
                        className="text-center",
                        style={
                            "fontWeight": "800",
                            "letterSpacing": "2px",
                            "color": "#2E2E2E",
                            "marginBottom": "25px",
                        },
                    ),

                    html.P(
                        "Este modelo describe la propagación de una enfermedad dividiendo "
                        "la población en Susceptibles (S), Infectados (I) y Recuperados (R).",
                        className="text-center",
                        style={"color": "#2E2E2E"},
                    ),

                    html.Hr(),

                    # =====================================================
                    #     ECUACIONES + INTERPRETACIÓN
                    # =====================================================
                    html.Div(
                        [
                            # ---------------- ECUACIONES ----------------
                            html.Div(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "SISTEMA DE ECUACIONES DIFERENCIALES",
                                                style={
                                                    "textAlign": "center",
                                                    "fontWeight": "700",
                                                    "letterSpacing": "1px",
                                                    "color": "#2E2E2E",
                                                    "marginBottom": "12px",
                                                },
                                            ),

                                            html.Img(
                                                src=(
                                                    r"https://latex.codecogs.com/svg.latex?"
                                                    r"\frac{dS}{dt}=-\beta SI,\;"
                                                    r"\frac{dI}{dt}=\beta SI-\gamma I,\;"
                                                    r"\frac{dR}{dt}=\gamma I"
                                                ),
                                                style={
                                                    "display": "block",
                                                    "margin": "10px auto",
                                                    "height": "60px",
                                                },
                                            ),
                                        ]
                                    ),
                                    style=INFO_CARD_STYLE,
                                ),
                                style={"width": "50%"},
                            ),

                            # ---------------- INTERPRETACIÓN ----------------
                            html.Div(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "INTERPRETACIÓN",
                                                style={
                                                    "textAlign": "center",
                                                    "fontWeight": "700",
                                                    "letterSpacing": "1px",
                                                    "color": "#2E2E2E",
                                                    "marginBottom": "12px",
                                                },
                                            ),

                                            dcc.Markdown(
                                                """
* **S(t):** Población susceptible.  
* **I(t):** Población infectada.  
* **R(t):** Población recuperada.  
* **β:** Tasa de contagio.  
* **γ:** Tasa de recuperación.  
* **N = S + I + R:** Población total constante.  
                                                """,
                                                style={"color": "#2E2E2E"},
                                            ),
                                        ]
                                    ),
                                    style=INFO_CARD_STYLE,
                                ),
                                style={"width": "50%"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "row",
                            "gap": "20px",
                            "alignItems": "stretch",
                            "marginBottom": "30px",
                        },
                    ),

                    html.Hr(),

                    # =====================================================
                    #  PARÁMETROS + GRÁFICA
                    # =====================================================
                    html.Div(
                        [

                            # ======================= IZQUIERDA =======================
                        html.Div(
                            [
                                html.H3(
                                    "PARÁMETROS",
                                    className="text-center",
                                    style={
                                        "fontWeight": "700",
                                        "letterSpacing": "2px",
                                        "color": "#2E2E2E",
                                        "marginBottom": "25px",
                                    },
                                ),

                                html.Div([
                                    dbc.Label("Susceptibles Iniciales (S₀):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-s0", type="number", value=990, min=0,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div([
                                    dbc.Label("Infectados Iniciales (I₀):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-i0", type="number", value=10, min=1,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div([
                                    dbc.Label("Recuperados Iniciales (R₀):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-r0", type="number", value=0, min=0,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div([
                                    dbc.Label("Tasa de contagio (β):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-beta", type="number", value=0.002, step=0.001,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div([
                                    dbc.Label("Tasa de recuperación (γ):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-gamma", type="number", value=0.5, step=0.01,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div([
                                    dbc.Label("Tiempo máximo (tₘₐₓ):", style=LABEL_STYLE),
                                    dcc.Input(id="sir-tmax", type="number", value=60, min=1, step=1,
                                            style=INPUT_STYLE_COMPACT),
                                ], style={"marginBottom": "20px"}),

                                html.Div(
                                    id="sir-result",
                                    className="mt-3",
                                    style={
                                        "fontWeight": "700",
                                        "color": "#E25822",
                                        "fontSize": "1.1rem",
                                    },
                                ),
                            ],
                            style={
                                "width": "30%",
                                "paddingRight": "25px",
                                "marginTop": "35px",
                            },
                        ),


                            # ======================= DERECHA =======================
                            html.Div(
                                [
                                    html.H3(
                                        "Dinámica del Modelo SIR",
                                        style={
                                            "textAlign": "center",
                                            "color": "#2E2E2E",
                                            "marginBottom": "18px",
                                            "fontWeight": "600",
                                        },
                                    ),

                                    dcc.Graph(
                                        id="sir-graph",
                                        style={
                                            "height": "520px",
                                            "backgroundColor": "white",
                                            "borderRadius": "16px",
                                            "boxShadow": "6px 6px 14px rgba(0,0,0,0.25)",
                                            "padding": "10px",
                                        },
                                    ),
                                ],
                                style={"width": "70%"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "row",
                            "gap": "20px",
                            "alignItems": "center",
                        },
                    ),
                ]
            ),
            style={
                "padding": "35px",
                "backgroundColor": "#FFFBF5",
                "borderRadius": "16px",
                "boxShadow": "0 6px 14px rgba(0,0,0,0.35)",
                "maxWidth": "1600px",
                "margin": "0 auto",
                "marginTop": "25px",
            },
        )
    ]
)


# ===========================================================
# CALLBACK SIR
# ===========================================================

@callback(
    Output("sir-graph", "figure"),
    Output("sir-result", "children"),
    Input("sir-s0", "value"),
    Input("sir-i0", "value"),
    Input("sir-r0", "value"),
    Input("sir-beta", "value"),
    Input("sir-gamma", "value"),
    Input("sir-tmax", "value"),
)
def update_sir(s0, i0, r0, beta, gamma, tmax):

    if None in (s0, i0, r0, beta, gamma, tmax):
        return dash.no_update, ""

    def sir_eq(y, t):
        S, I, R = y
        return -beta * S * I, beta * S * I - gamma * I, gamma * I

    t = np.linspace(0, tmax, 400)
    S, I, R = odeint(sir_eq, (s0, i0, r0), t).T

    fig = go.Figure([
        go.Scatter(x=t, y=S, mode="lines", name="Susceptibles"),
        go.Scatter(x=t, y=I, mode="lines", name="Infectados"),
        go.Scatter(x=t, y=R, mode="lines", name="Recuperados"),
    ])

    fig.update_layout(
        xaxis_title="Tiempo",
        yaxis_title="Población",
        template="plotly_white",
    )

    return fig, f"Pico máximo de infectados: {np.max(I):.2f}"