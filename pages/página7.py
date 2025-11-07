import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_modelo_seir
from dash_iconify import DashIconify

dash.register_page(__name__, path='/modelo-seir', name='Modelo SEIR')

layout = html.Div(className='epidemic-page-container', children=[

    # ======== COLUMNA IZQUIERDA ========
    html.Div(className='controls-column', children=[
        html.Div(className='section-card', children=[
            html.Div(className='section-header', children=[
                DashIconify(icon="mdi:virus-outline", width=35, className='section-icon'),
                html.H2("Modelo SEIR - Epidemiología", className='column-header'),
            ]),

            html.Div(className='parametros-grid', children=[
                html.Div(className='parametro-item', children=[
                    html.Label("Población Total (N):", className='param-label'),
                    dcc.Input(id="seir-n", type="number", value=1000, className="input-field"),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Tasa de transmisión (β):", className='param-label'),
                    dcc.Input(id="seir-beta", type="number", value=0.35, step=0.01, className="input-field"),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Tasa de incubación (σ):", className='param-label'),
                    dcc.Input(
                        id="seir-sigma", type="number", value=0.2, step=0.01, 
                        placeholder="Ej: 0.2 (5 días de incubación)", className="input-field"
                    ),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Tasa de recuperación (γ):", className='param-label'),
                    dcc.Input(
                        id="seir-gamma", type="number", value=0.1, step=0.01,
                        placeholder="Ej: 0.1 (10 días de infección)", className="input-field"
                    ),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Expuestos iniciales (E₀):", className='param-label'),
                    dcc.Input(id="seir-e0", type="number", value=1, className="input-field"),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Infectados iniciales (I₀):", className='param-label'),
                    dcc.Input(id="seir-i0", type="number", value=0, className="input-field"),
                ]),
                html.Div(className='parametro-item', children=[
                    html.Label("Tiempo de simulación (días):", className='param-label'),
                    dcc.Input(id="seir-t", type="number", value=160, className="input-field"),
                ]),
            ]),

            html.Button("Simular Epidemia", id="btn-simular-seir", n_clicks=0, className="btn-primary-action")
        ]),
    ]),

    # ======== COLUMNA DERECHA ========
    html.Div(className='visualization-column', children=[
        html.Div(className='section-card', children=[
            html.Div(className='section-header center-header', children=[
                DashIconify(icon="mdi:chart-line", width=35, className='section-icon'),
                html.H2("Evolución de la Epidemia", className='column-header'),
            ]),
            html.Div(className='sir-graph-container', children=[
                dcc.Graph(id="grafica-seir", config={"displayModeBar": False})
            ])
        ])
    ])
])


@callback(
    Output('grafica-seir', 'figure'),
    Input('btn-simular-seir', 'n_clicks'),
    State('seir-n', 'value'),
    State('seir-beta', 'value'),
    State('seir-sigma', 'value'),
    State('seir-gamma', 'value'),
    State('seir-e0', 'value'),
    State('seir-i0', 'value'),
    State('seir-t', 'value'),
    prevent_initial_call=False
)
def update_seir_graph(n_clicks, N, beta, sigma, gamma, E0, I0, T):
    # Validación de parámetros
    N = N if N and N > 0 else 1000
    beta = beta if beta else 0.35
    sigma = sigma if sigma else 0.2
    gamma = gamma if gamma else 0.1
    E0 = E0 if E0 is not None else 1
    I0 = I0 if I0 is not None else 0
    T = T if T and T > 0 else 160

    fig = generar_modelo_seir(N, E0, I0, beta, sigma, gamma, T)
    return fig
