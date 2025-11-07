import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_modelo_sir

dash.register_page(__name__, path='/modelo-sir', name='Modelo SIR')

layout = html.Div(
    id="pagina6",
    children=[
        # ==============================
        # SECCIÓN IZQUIERDA – PARÁMETROS DEL MODELO
        # ==============================
        html.Div(
            className="p6-left",
            children=[
                html.H1("Modelo SIR - Epidemiología", className="p6-title"),

                html.P(
                    "El modelo SIR (Susceptibles, Infectados, Recuperados) describe cómo se propaga "
                    "una enfermedad infecciosa en una población. Este modelo permite analizar "
                    "la dinámica de contagios y recuperaciones en el tiempo.",
                    className="p6-description",
                ),

                html.Div(
                    className="p6-card",
                    children=[
                        html.H3("Parámetros del Modelo", className="p6-subtitle"),

                        html.Div(className="p6-item", children=[
                            html.Label("Población Total (N):", className="p6-label"),
                            dcc.Input(id="sir-n", type="number", value=1000, className="p6-input")
                        ]),

                        html.Div(className="p6-item", children=[
                            html.Label("Tasa de transmisión (β):", className="p6-label"),
                            dcc.Input(id="sir-beta", type="number", value=0.3, step=0.01, className="p6-input")
                        ]),

                        html.Div(className="p6-item", children=[
                            html.Label("Tasa de recuperación (γ):", className="p6-label"),
                            dcc.Input(id="sir-gamma", type="number", value=0.1, step=0.01, className="p6-input")
                        ]),

                        html.Div(className="p6-item", children=[
                            html.Label("Infectados iniciales (I₀):", className="p6-label"),
                            dcc.Input(id="sir-i0", type="number", value=1, className="p6-input")
                        ]),

                        html.Div(className="p6-item", children=[
                            html.Label("Tiempo de simulación (días):", className="p6-label"),
                            dcc.Input(id="sir-t", type="number", value=100, className="p6-input")
                        ]),

                        html.Button("Simular Epidemia", id="btn-simular-sir", n_clicks=0, className="p6-btn"),
                    ],
                ),
            ],
        ),

        # ==============================
        # SECCIÓN DERECHA – VISUALIZACIÓN
        # ==============================
        html.Div(
            className="p6-right",
            children=[
                html.Div(
                    className="p6-graph-card",
                    children=[
                        html.H2("Evolución de la Epidemia", className="p6-graph-title"),
                        dcc.Graph(id="grafica-sir", className="p6-graph")
                    ],
                )
            ],
        ),
    ],
)


# ==============================
# CALLBACK
# ==============================
@callback(
    Output('grafica-sir', 'figure'),
    Input('btn-simular-sir', 'n_clicks'),
    State('sir-n', 'value'),
    State('sir-beta', 'value'),
    State('sir-gamma', 'value'),
    State('sir-i0', 'value'),
    State('sir-t', 'value'),
    prevent_initial_call=False
)
def update_sir_graph(n_clicks, N, beta, gamma, I0, T):
    N = N if N is not None and N > 0 else 1000
    beta = beta if beta is not None else 0.3
    gamma = gamma if gamma is not None else 0.1
    I0 = I0 if I0 is not None and I0 > 0 else 1
    T = T if T is not None and T > 0 else 100
    fig = generar_modelo_sir(N, I0, beta, gamma, T)
    return fig
