import dash
from dash import html, dcc, Output, Input, State, callback
from utils.funciones import fucion_graficas_ecu_log

dash.register_page(
    __name__,
    path="/pagina4",
    name="Página 4"
)

layout = html.Div(
    id="pagina4",  
    children=[

        # =======================
        # SECCIÓN IZQUIERDA (GRÁFICA)
        # =======================
        html.Div(
            children=[
                html.H2("Gráfica del modelo", className="p4-title"),

                dcc.Graph(
                    id="grafica",
                    style={"height": "430px", "width": "100%"},
                )
            ],
            className="p4-left"
        ),

        # =======================
        # SECCIÓN DERECHA (PARÁMETROS)
        # =======================
        html.Div(
            children=[
                html.H2("Parámetros del modelo", className="p4-title"),

                html.Div(
                    children=[

                        html.Div([
                            html.Label("Población inicial P(0):", className="p4-label"),
                            dcc.Input(
                                id="input-p0",
                                type="number",
                                value=200,
                                className="p4-input",
                                placeholder="Ejemplo: 200"
                            )
                        ], className="p4-item"),

                        html.Div([
                            html.Label("Tasa de Crecimiento (r):", className="p4-label"),
                            dcc.Input(
                                id="input-r",
                                type="number",
                                value=0.04,
                                step=0.01,
                                className="p4-input",
                                placeholder="Ejemplo: 0.04"
                            )
                        ], className="p4-item"),

                        html.Div([
                            html.Label("Capacidad de Carga (K):", className="p4-label"),
                            dcc.Input(
                                id="input-k",
                                type="number",
                                value=750,
                                className="p4-input",
                                placeholder="Ejemplo: 750"
                            )
                        ], className="p4-item"),

                        html.Div([
                            html.Label("Tiempo Máximo (t):", className="p4-label"),
                            dcc.Input(
                                id="input-t",
                                type="number",
                                value=100,
                                className="p4-input",
                                placeholder="Ejemplo: 100"
                            )
                        ], className="p4-item"),

                        html.Button("Generar Gráfica", id="btn-generar", className="p4-btn"),
                    ],
                    className="p4-card"
                ),
            ],
            className="p4-right"
        ),
    ],
    className="p4-container"
)


# =======================
# CALLBACK
# =======================
@callback(
    Output("grafica", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),
    State("input-t", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, P0, r, K, t_max):
    fig = fucion_graficas_ecu_log(P0=P0, K=K, t_max=t_max, r=r)
    return fig
