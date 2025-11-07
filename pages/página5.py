import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import generar_campo_vectorial

dash.register_page(__name__, path='/campo-vectorial', name='Campo Vectorial 2D')

layout = html.Div(
    id="pagina5",
    children=[
        # ==============================
        # SECCIÓN IZQUIERDA - PARÁMETROS Y EXPLICACIÓN
        # ==============================
        html.Div(
            className="p5-left",
            children=[
                html.H1("Campo Vectorial 2D", className="p5-title"),

                html.P(
                    "Un campo vectorial 2D asocia a cada punto (x, y) un vector que representa "
                    "una dirección y magnitud. Este concepto es fundamental para estudiar flujos, "
                    "velocidades y trayectorias dinámicas.",
                    className="p5-description",
                ),

                html.Div(
                    className="p5-equation",
                    children=[
                        html.Span("𝐹(x, y) = (P(x, y), Q(x, y))", className="p5-equation-text"),
                    ],
                ),

                html.Div(
                    className="p5-card",
                    children=[
                        html.H3("Parámetros del Campo", className="p5-subtitle"),

                        html.Div(className="p5-item", children=[
                            html.Label("Ecuación dx/dt =", className="p5-label"),
                            dcc.Input(
                                id="ecu-dx-dt",
                                type="text",
                                value="Y*(X**2 + Y**2)",
                                className="p5-input"
                            ),
                        ]),

                        html.Div(className="p5-item", children=[
                            html.Label("Ecuación dy/dt =", className="p5-label"),
                            dcc.Input(
                                id="ecu-dy-dt",
                                type="text",
                                value="-X*(X**2 + Y**2)",
                                className="p5-input"
                            ),
                        ]),

                        html.Div(className="p5-grid-inputs", children=[
                            html.Div(className="p5-item", children=[
                                html.Label("Rango X:", className="p5-label"),
                                dcc.Input(
                                    id="rango-x",
                                    type="number",
                                    value=5,
                                    step=1,
                                    className="p5-input-small"
                                ),
                            ]),
                            html.Div(className="p5-item", children=[
                                html.Label("Rango Y:", className="p5-label"),
                                dcc.Input(
                                    id="rango-y",
                                    type="number",
                                    value=5,
                                    step=1,
                                    className="p5-input-small"
                                ),
                            ]),
                            html.Div(className="p5-item", children=[
                                html.Label("Mallado:", className="p5-label"),
                                dcc.Input(
                                    id="mallado",
                                    type="number",
                                    value=20,
                                    step=1,
                                    min=5,
                                    max=50,
                                    className="p5-input-small"
                                ),
                            ]),
                        ]),

                        html.Button(
                            "Generar Campo Vectorial",
                            id="btn-primary-action",
                            n_clicks=0,
                            className="p5-btn"
                        ),
                    ],
                ),

                html.Div(
                    className="p5-examples",
                    children=[
                        html.H3("Ejemplos sugeridos", className="p5-subtitle"),
                        html.Ul([
                            html.Li("dx/dt = Y, dy/dt = -X → Giro horario"),
                            html.Li("dx/dt = -Y, dy/dt = X → Giro antihorario"),
                            html.Li("dx/dt = X, dy/dt = Y → Fuente"),
                            html.Li("dx/dt = -X, dy/dt = -Y → Sumidero"),
                            html.Li("dx/dt = X + Y, dy/dt = cos(Y)"),
                            html.Li("dx/dt = Y*(X²+Y²), dy/dt = -X*(X²+Y²)"),
                        ])
                    ]
                ),
            ],
        ),

        # ==============================
        # SECCIÓN DERECHA - VISUALIZACIÓN
        # ==============================
        html.Div(
            className="p5-right",
            children=[
                html.Div(
                    className="p5-graph-card",
                    children=[
                        html.H2("Visualización del Campo Vectorial", className="p5-graph-title"),
                        dcc.Graph(id="grafica-campo-vectorial", className="p5-graph")
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
    Output("grafica-campo-vectorial", "figure"),
    Input("btn-primary-action", "n_clicks"),
    State("ecu-dx-dt", "value"),
    State("ecu-dy-dt", "value"),
    State("rango-x", "value"),
    State("rango-y", "value"),
    State("mallado", "value"),
    prevent_initial_call=False,
)
def update_vector_field(n_clicks, ecu_dx, ecu_dy, r_x, r_y, malla):
    ecu_dx = ecu_dx if ecu_dx else "Y"
    ecu_dy = ecu_dy if ecu_dy else "-X"
    r_x = r_x if r_x is not None else 5
    r_y = r_y if r_y is not None else 5
    malla = malla if malla is not None else 20
    fig = generar_campo_vectorial(ecu_dx, ecu_dy, r_x, r_y, malla)
    return fig
