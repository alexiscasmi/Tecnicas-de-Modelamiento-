def fucion_graficas_ecu_log(P0,K,t_max,r):
    
    import numpy as np 
    import plotly.graph_objects as go

    t=np.linspace(0, t_max, 20)

    P=(P0*K*np.exp(r*t))/((K-P0)+P0*np.exp(r*t))

    trace_poblacion=go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Población P(t)',
        line=dict(
            color='green',
            width=2
        ),
        marker=dict(
            size=6,
            color='black',
            symbol='circle'
        ),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y: .2f}<extra></extra>'
    )
    trace_capacidad= go.Scatter(
        x=[0, t_max],
        y=[K,K],
        mode='lines',
        name='Capacidad de carga (K)',
        line=dict(
            color='red',
            width=2,
            dash='dot'
        ),
         hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig=go.Figure(data=[trace_poblacion, trace_capacidad])
    
    fig.update_layout(
    title=dict(
        text='<b>Modelo logístico de crecimiento poblacional</b>',
        font=dict(size=20, color='black'),
        x=0.5,
        y=0.95
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=70, b=40),
    paper_bgcolor='white',
    plot_bgcolor='lightpink',
    font=dict(
        family='Outfit', 
        size=11, 
        color='black'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        ) 
    )
    
    fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='black',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range=[0, t_max]
    )

    fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='black',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range=[0, K+K*0.1]
    )
    return fig


# ---------------------------------------------------------------------
# 👇 A partir de aquí se agregan las funciones para páginas 5, 6 y 7
# ---------------------------------------------------------------------

import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint


def funcion_graficas_ecu_log(P0, r, K, t_max):
    t = np.linspace(0, t_max, 200)
    P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', name='Población',
        line=dict(color='#3498db', width=3),
        hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))

    fig.add_hline(y=K, line=dict(color='#e74c3c', dash='dash', width=2),
                  annotation_text=f"Capacidad (K={K})", annotation_position="bottom right")

    fig.update_layout(
        title='<b>Modelo Logístico de Crecimiento</b>',
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        paper_bgcolor='white', plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    return fig


def funcion_grafica_logistica_con_cosecha(P0, r, K, t_max, h):
    t = np.linspace(0, t_max, 500)

    def modelo(P, t, r, K, h):
        return r * P * (1 - P / K) - h

    P = odeint(modelo, P0, t, args=(r, K, h)).flatten()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', name='Población con Cosecha',
        line=dict(color='#27ae60', width=3),
        hovertemplate='Tiempo: %{x:.1f}<br>Población: %{y:.1f}<extra></extra>'
    ))

    fig.add_hline(y=K, line=dict(color='#e74c3c', dash='dash', width=2),
                  annotation_text=f"Capacidad Original (K={K})", annotation_position="top right")

    fig.update_layout(
        title='<b>Modelo Logístico con Cosecha Constante</b>',
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        paper_bgcolor='white', plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12),
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode='x unified'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0', zeroline=False)
    return fig


def generar_campo_vectorial(ecu_dx_dt, ecu_dy_dt, rango_x, rango_y, mallado):
    x = np.linspace(-rango_x, rango_x, mallado)
    y = np.linspace(-rango_y, rango_y, mallado)
    X, Y = np.meshgrid(x, y)

    dx_dt = np.nan_to_num(eval(ecu_dx_dt, {'__builtins__': None, 'X': X, 'Y': Y, 'np': np}))
    dy_dt = np.nan_to_num(eval(ecu_dy_dt, {'__builtins__': None, 'X': X, 'Y': Y, 'np': np}))

    magnitudes = np.sqrt(dx_dt**2 + dy_dt**2)
    dx_dt_norm = np.where(magnitudes == 0, 0, dx_dt / magnitudes)
    dy_dt_norm = np.where(magnitudes == 0, 0, dy_dt / magnitudes)

    escala_vector = min(rango_x, rango_y) / (mallado * 1.5)

    fig = go.Figure(
        data=go.Cone(
            x=X.flatten(),
            y=Y.flatten(),
            z=np.zeros_like(X).flatten(),
            u=dx_dt_norm.flatten() * escala_vector,
            v=dy_dt_norm.flatten() * escala_vector,
            w=np.zeros_like(X).flatten(),
            sizemode="absolute",
            sizeref=escala_vector * 0.5,
            colorscale=[[0, '#3498db'], [1, '#2c3e50']],
            colorbar=None,
            showscale=False,
            anchor="tail"
        )
    )

    fig.add_trace(go.Scatter(x=[-rango_x, rango_x], y=[0, 0], mode='lines',
                             line=dict(color='red', width=1), showlegend=False))
    fig.add_trace(go.Scatter(x=[0, 0], y=[-rango_y, rango_y], mode='lines',
                             line=dict(color='red', width=1), showlegend=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-rango_x, rango_x], title='X'),
            yaxis=dict(range=[-rango_y, rango_y], title='Y'),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        title_text='<b>Visualización del Campo Vectorial</b>',
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9',
        font=dict(family='Poppins', size=12, color='black'),
        height=600
    )
    return fig


def generar_modelo_sir(N, I0, beta, gamma, T):
    t = np.linspace(0, T, T*5)
    S0 = N - I0
    R0 = 0
    y0 = S0, I0, R0

    def deriv(y, t, N, beta, gamma):
        S, I, R = y
        dSdt = - (beta * S * I) / N
        dIdt = (beta * S * I) / N - (gamma * I)
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='#3498db', width=3)))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='#e74c3c', width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='#27ae60', width=3)))

    fig.update_layout(title='<b>Evolución del Modelo SIR</b>',
                      xaxis_title='Tiempo (días)',
                      yaxis_title='Número de personas',
                      paper_bgcolor='white', plot_bgcolor='#f9f9f9')
    return fig


def generar_modelo_seir(N, E0, I0, beta, sigma, gamma, T):
    t = np.linspace(0, T, T*5)
    R0 = 0
    S0 = N - E0 - I0
    y0 = S0, E0, I0, R0

    def deriv(y, t, N, beta, sigma, gamma):
        S, E, I, R = y
        dSdt = - (beta * S * I) / N
        dEdt = (beta * S * I) / N - (sigma * E)
        dIdt = (sigma * E) - (gamma * I)
        dRdt = gamma * I
        return dSdt, dEdt, dIdt, dRdt

    ret = odeint(deriv, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='#3498db', width=3)))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Expuestos (E)', line=dict(color='#f39c12', width=3, dash='dash')))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='#e74c3c', width=3)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='#27ae60', width=3)))

    fig.update_layout(title='<b>Evolución del Modelo SEIR</b>',
                      xaxis_title='Tiempo (días)',
                      yaxis_title='Número de personas',
                      paper_bgcolor='white', plot_bgcolor='#f9f9f9')
    return fig
