import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/pagina2', name='Página 2')

# ==========================
# DATOS DEL MODELO LOGÍSTICO
# ==========================
r = 0.1   # tasa de crecimiento
K = 1000  # capacidad de carga
P0 = 50   # población inicial

t = np.linspace(0, 100, 200)
P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# ==========================
# GRÁFICO (Plotly)
# ==========================
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=t,
    y=P,
    mode="lines",
    line=dict(color="green", width=3),
    name="P(t) = K / [1 + ((K - P₀)/P₀)e^{-rt}]"
))

fig.update_layout(
    title=dict(
        text="<b>Crecimiento poblacional con capacidad de carga</b>",
        x=0.5,
        y=0.95,
        font=dict(size=18, color="#0074D9")
    ),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    plot_bgcolor="white",
    paper_bgcolor="lightblue",
    font=dict(family="Outfit, sans-serif", size=12, color="black"),
    margin=dict(l=40, r=40, t=60, b=40)
)

fig.update_xaxes(showgrid=True, gridcolor="#cbd5e1", zeroline=True, zerolinecolor="red")
fig.update_yaxes(showgrid=True, gridcolor="#cbd5e1", zeroline=True, zerolinecolor="red")

# ==========================
# LAYOUT DE LA PÁGINA
# ==========================
layout = html.Div(
    className="page2-container",  # 🔹 Nueva clase principal para controlar el layout lado a lado
    children=[
        # MITAD IZQUIERDA: TEXTO
        html.Div(
            className="page2-text",
            children=[
                html.H2("Crecimiento de la población y capacidad de carga", className="titulo-capacidad"),
                html.P("""
                Para modelar el crecimiento de la población mediante una ecuación diferencial, 
                primero introducimos algunas variables relevantes. 
                La variable t representa el tiempo, mientras que P(t) denota la población como función del tiempo.
                """, className="texto-capacidad"),

                html.P("""
                Si P(t) es diferenciable, entonces dP/dt representa la tasa instantánea de cambio de la población en el tiempo.
                Un modelo más realista que el crecimiento exponencial es el modelo logístico:
                """, className="texto-capacidad"),

                html.P("dP/dt = rP (1 - P/K)", className="ecuacion-destacada"),

                html.P("""
                Donde:
                - r es la tasa de crecimiento,
                - K es la capacidad de carga (la población máxima sostenible).
                """, className="texto-capacidad"),

                html.P("La solución de esta ecuación diferencial es:", className="texto-capacidad"),

                html.P("P(t) = K / [1 + ((K - P₀) / P₀) e^{-rt}]", className="ecuacion-destacada"),

                html.P("""
                En esta función, la población crece rápidamente al principio, pero a medida que se acerca a 
                la capacidad de carga K, su crecimiento se desacelera y finalmente se estabiliza.
                """, className="texto-capacidad"),
            ]
        ),

        # MITAD DERECHA: GRÁFICA
        html.Div(
            className="page2-graph",
            children=[
                html.H3("Gráfica del modelo logístico", style={"textAlign": "center"}),
                dcc.Graph(figure=fig, style={"height": "400px", "width": "100%"})
            ]
        ),
    ]
)
