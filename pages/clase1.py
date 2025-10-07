import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/pagina1', name='Página 1')

# Datos y modelo

P0 = 100  # Población Inicial
r = 0.03  # Tasa de crecimiento
t = np.linspace(0, 100, 10)  # Tiempo
P = P0 * np.exp(r * t)  # Función de crecimiento exponencial


# Gráfica

trace = go.Scatter(
    x=t,
    y=P,
    mode="lines+markers",
    line=dict(dash='dot', color='black', width=2),
    marker=dict(color='blue', symbol='square', size=6),
    name='P(t) = P₀ · e^(rt)',
    hovertemplate='t: %{x}<br>P(t): %{y}<extra></extra>'
)

fig = go.Figure(data=[trace])
fig.update_layout(
    title=dict(
        text="<b>Crecimiento poblacional</b>",
        font=dict(size=20, color='green'),
        x=0.5,
        y=0.93
    ),
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='lightblue',
    plot_bgcolor='white',
    font=dict(family='Outfit', size=11, color='black')
)

fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True
)

fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True
)


# Layout de la página

layout = html.Div(
    className="page-container",
    children=[
        # Texto a la izquierda
        html.Div(
            className="content left",
            children=[
                html.H2("Crecimiento de la población y capacidad de carga"),
                dcc.Markdown("""
                Para modelar el crecimiento de la población mediante una ecuación diferencial, primero tenemos que introducir algunas variables y términos relevantes. 
                La variable *t* representará el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, meses o incluso años. 

                La variable *P* representará a la población. Como la población varía con el tiempo, se entiende que es una función del tiempo. Por lo tanto, utilizamos la notación $P(t)$ para la población en función del tiempo. 

                Si $P(t)$ es una función diferenciable, entonces la primera derivada $\\dfrac{dP}{dt}$ representa la tasa instantánea de cambio de la población en función del tiempo.
                """, mathjax=True),
                dcc.Markdown("""
                En *Crecimiento y decaimiento exponencial*, estudiamos el crecimiento y decaimiento exponencial de poblaciones y sustancias radiactivas. 

                Un ejemplo de función de crecimiento exponencial es  $P(t)=P_0 e^{rt}$.

                En esta función:
                - $P(t)$ representa la población en el momento $t$  
                - $P_0$ representa la población inicial (población en el tiempo $t=0$)  
                - La constante $r>0$ se denomina tasa de crecimiento.  

                Aquí $P_0=100$ y $r=0,03$.
                """, mathjax=True),
            ]
        ),

        # Gráfica a la derecha
        html.Div(
            className="content right",
            children=[
                html.H2("Gráfica", className="title"),
                dcc.Graph(figure=fig, style={'height': '350px', 'width': '100%'})
            ]
        ),
    ]
)
