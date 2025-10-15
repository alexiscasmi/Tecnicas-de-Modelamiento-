import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np
import plotly.graph_objects as go

dash.register_page(
    __name__,
    path="/pagina3",
    name="Página 3"
)

layout = html.Div(
    id="pagina3",  
    children=[
        # =======================
        # SECCIÓN IZQUIERDA (PARÁMETROS)
        # =======================
        html.Div(
            children=[
                html.H2("Parámetros del modelo", className="p3-title"),

                html.Div(
                    children=[
                        html.Div([
                            html.Label("Población inicial P(0):", className="p3-label"),
                            dcc.Input(
                                id="input-p0",
                                type="number",
                                value=200,
                                className="p3-input",
                                placeholder="Ejemplo: 200"
                            )
                        ], className="p3-item"),

                        html.Div([
                            html.Label("Tasa de Crecimiento (r):", className="p3-label"),
                            dcc.Input(
                                id="input-r",
                                type="number",
                                value=0.04,
                                step=0.01,
                                className="p3-input",
                                placeholder="Ejemplo: 0.04"
                            )
                        ], className="p3-item"),

                        html.Div([
                            html.Label("Capacidad de Carga (K):", className="p3-label"),
                            dcc.Input(
                                id="input-k",
                                type="number",
                                value=750,
                                className="p3-input",
                                placeholder="Ejemplo: 750"
                            )
                        ], className="p3-item"),

                        html.Div([
                            html.Label("Tiempo Máximo (t):", className="p3-label"),
                            dcc.Input(
                                id="input-t",
                                type="number",
                                value=100,
                                className="p3-input",
                                placeholder="Ejemplo: 100"
                            )
                        ], className="p3-item"),

                        html.Button("Generar Gráfica", id="btn-generar", className="p3-btn"),
                    ],
                    className="p3-card"
                ),
            ],
            className="p3-left"
        ),

        # =======================
        # SECCIÓN DERECHA (GRÁFICA)
        # =======================
        html.Div(
            children=[
                html.H2("Gráfica del modelo", className="p3-title"),
                dcc.Graph(
                    id="grafica-poblacion",
                    style={"height": "430px", "width": "100%"},
                )
            ],
            className="p3-right"
        ),
    ],
    className="p3-container"
)

# =======================
# CALLBACK
# =======================
@callback(
    Output("grafica-poblacion", "figure"),
    Input("btn-generar", "n_clicks"),
    State("input-p0", "value"),
    State("input-r", "value"),
    State("input-k", "value"),
    State("input-t", "value"),
    prevent_initial_call=True,
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    t = np.linspace(0, t_max, 100)
    P = (P0 * K * np.exp(r * t)) / ((K - P0) + P0 * np.exp(r * t))

    trace_poblacion = go.Scatter(
        x=t, y=P, mode="lines+markers", name="Población P(t)",
        line=dict(color="blue", width=2),
        marker=dict(size=6, color="black"),
        hovertemplate="t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>"
    )

    trace_capacidad = go.Scatter(
        x=[0, t_max], y=[K, K], mode="lines", name="Capacidad de carga (K)",
        line=dict(color="red", width=2, dash="dot"),
        hovertemplate="K: %{y:.2f}<extra></extra>"
    )

    fig = go.Figure(data=[trace_poblacion, trace_capacidad])

    fig.update_layout(
        title=dict(
            text="<b>Modelo logístico de crecimiento poblacional</b>",
            font=dict(size=20, color="black"),
            x=0.5,
        ),
        xaxis_title="Tiempo (t)",
        yaxis_title="Población P(t)",
        margin=dict(l=40, r=40, t=70, b=40),
        paper_bgcolor="lightblue",
        plot_bgcolor="white",
        font=dict(family="Outfit", size=11, color="black"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
        range=[0, t_max]
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="lightpink",
        zeroline=True, zerolinewidth=2, zerolinecolor="red",
        showline=True, linecolor="black", linewidth=2, mirror=True,
        range=[0, K + K * 0.1]
    )

    return fig
