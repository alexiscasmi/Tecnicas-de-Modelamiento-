import dash
from dash import html, dcc, Input, Output, State, callback
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint
from typing import List, Tuple, Any, Dict, Union

# ============================================================
# ⚙️ REGISTRO DE PÁGINA DASH
# ============================================================
dash.register_page(
    __name__,
    path='/Proyecto2.3',
    name='PROYECTO 2.3'
)

# ============================================================
# 🔬 MODELO SIR (ECUACIONES DIFERENCIALES)
# ============================================================
def modelo_sir(y: List[float], t: float, beta: float, gamma: float, N: float) -> List[float]:
    """
    Define el sistema de ecuaciones diferenciales del Modelo SIR.

    Argumentos:
        y (list): Vector de estado [S, I, R] en el tiempo t.
        t (float): Instante de tiempo (días).
        beta (float): Tasa de contacto/infección (β).
        gamma (float): Tasa de recuperación (γ).
        N (float): Población total.

    Retorna:
        list: Las derivadas [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = y
    
    # Ecuaciones fundamentales del modelo SIR
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]


# ============================================================
# 📊 GENERADOR DE GRÁFICO Y CÁLCULOS
# ============================================================
def generar_grafico_sir(
    S0: int, I0: int, R0: int, beta: float, gamma: float, t_max: int
) -> Tuple[go.Figure, float, float, float, float, float, float]:
    """
    Calcula la solución del modelo SIR y genera la figura de Plotly.

    Argumentos:
        S0, I0, R0 (int): Población inicial S, I, R.
        beta (float): Tasa de infección (β).
        gamma (float): Tasa de recuperación (γ).
        t_max (int): Tiempo máximo de la simulación (días).

    Retorna:
        tuple: (figura_plotly, R0, tiempo_pico, valor_pico, S_final, R_final, tasa_ataque_final).
    """
    # Preparación de datos para la integración
    N = S0 + I0 + R0
    t = np.linspace(0, t_max, 1000)
    y0 = [S0, I0, R0]

    # Solución de las EDOs mediante integración numérica
    solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, N))
    S, I, R = solucion.T

    # --- Cálculo de Indicadores Clave ---
    R0_val = beta / gamma if gamma != 0 else float('inf')
    
    idx_pico = np.argmax(I)
    tiempo_pico = t[idx_pico]
    valor_pico = I[idx_pico]

    S_final = S[-1]
    R_final = R[-1]
    tasa_ataque_final = (R_final / N) * 100

    # --- Configuración de la Figura de Plotly ---
    fig = go.Figure()

    # Trazas de las curvas (S, I, R)
    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines',
        name='Susceptibles (S)',
        line=dict(color='#1f77b4', width=3)  # Azul (ligeramente más intenso)
    ))

    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines',
        name='Infectados (I)',
        line=dict(color='#d62728', width=3)  # Rojo
    ))

    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines',
        name='Recuperados (R)',
        line=dict(color='#2ca02c', width=3)  # Verde
    ))

    # Marcador de la Infección Pico
    fig.add_vline(
        x=tiempo_pico,
        line_dash="dash",
        line_color="#ff7f0e",  # Naranja
        annotation_text=f"Pico: día {tiempo_pico:.1f}",
        annotation_position="top right"
    )

    fig.add_trace(go.Scatter(
        x=[tiempo_pico],
        y=[valor_pico],
        mode='markers',
        marker=dict(size=12, color='#ff7f0e', symbol='star'),
        name='Pico de infección',
        showlegend=True
    ))

    # Configuración de Layout y Estilo
    fig.update_layout(
        title={
            'text': f'Modelo SIR - Dinámica de la Población (R₀ = {R0_val:.2f})',
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title='Tiempo (días)',
        yaxis_title='Población',
        hovermode='x unified',
        template='plotly_white', # Estilo limpio
        height=550,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="top", y=1.05,
            xanchor="right", x=1
        )
    )

    return fig, R0_val, tiempo_pico, valor_pico, S_final, R_final, tasa_ataque_final


# ============================================================
# 🎨 LAYOUT (ESTRUCTURA DE LA INTERFAZ)
# ============================================================
# He añadido algunas clases CSS para mejorar la semántica del HTML y permitir estilos más limpios
layout = html.Div(className="sir-dashboard-layout", children=[

    # --- PANEL DE CONTROL IZQUIERDO ---
    html.Div(className="sir-control-panel", children=[
        html.H2("🎮 Modelo SIR: Parámetros", className="panel-title"),
        html.Hr(className="separator"),

        # ------------------------ POBLACIÓN INICIAL ------------------------
        html.Div(className="input-section", children=[
            html.H3("👥 Población Inicial", className="section-subtitle"),

            html.Div(className="sir-input-row", children=[
                html.Label("Población Total (N):", className="sir-input-label"),
                dcc.Input(id="input-n-sir", type="number", value=100000, min=1, className="sir-input-field form-control")
            ]),

            html.Div(className="sir-input-row", children=[
                html.Label("Susceptibles Iniciales (S₀):", className="sir-input-label susceptible-label"),
                dcc.Input(id="input-s0-sir", type="number", value=99500, min=0, className="sir-input-field form-control")
            ]),

            html.Div(className="sir-input-row", children=[
                html.Label("Infectados Iniciales (I₀):", className="sir-input-label infected-label"),
                dcc.Input(id="input-i0-sir", type="number", value=500, min=0, className="sir-input-field form-control")
            ]),

            html.Div(className="sir-input-row", children=[
                html.Label("Recuperados Iniciales (R₀):", className="sir-input-label recovered-label"),
                dcc.Input(id="input-r0-sir", type="number", value=0, min=0, className="sir-input-field form-control")
            ]),
        ]),
        html.Hr(className="separator"),

        # ------------------------ PARÁMETROS DEL MODELO ------------------------
        html.Div(className="input-section", children=[
            html.H3("🧪 Parámetros Epidemiológicos", className="section-subtitle"),

            html.Div(className="sir-input-row", children=[
                html.Label("Tasa de Infección (β) [1/día]:", className="sir-input-label"),
                dcc.Input(id="input-beta-sir", type="number", value=0.1143, step="0.0001",
                          min=0, className="sir-input-field form-control")
            ]),

            html.Div(className="sir-input-row", children=[
                html.Label("Tasa de Recuperación (γ) [1/día]:", className="sir-input-label"),
                dcc.Input(id="input-gamma-sir", type="number", value=0.0286, step="0.0001",
                          min=0, className="sir-input-field form-control")
            ]),

            html.Div(className="sir-input-row", children=[
                html.Label("Horizonte de tiempo (días):", className="sir-input-label"),
                dcc.Input(id="input-t-max-sir", type="number", value=365, min=10, className="sir-input-field form-control")
            ]),
        ]),
        html.Hr(className="separator"),

        # ------------------------ R0 + BOTÓN DE ACCIÓN ------------------------
        html.Div(className="action-footer-panel", children=[
            html.Div(className="r0-display-box", children=[
                html.Div("Número Reproductivo Básico (R₀):", className="r0-label"),
                html.Div(id="r0-value-display", className="r0-value")
            ]),
            html.Button("🚀 Generar Simulación", id="btn-generar",
                        className="btn-primary btn-lg", n_clicks=0) # Estilo de botón primario
        ])
    ]),

    # --- PANEL DE VISUALIZACIÓN DERECHO ---
    html.Div(className="sir-visualization-panel", children=[
        html.H2("📈 Simulación Dinámica SIR", className="panel-title"),

        html.Div(className="sir-graph-card", children=[
            dcc.Graph(
                id='grafico-sir-interactivo',
                config={'displayModeBar': True, 'responsive': True},
                style={'height': '100%', 'width': '100%'}
            )
        ]),

        html.Div(className="sir-info-card", children=[
            html.H3("📝 Resultados y Resumen", className="info-title"),
            html.Div(id="simulation-info", className="sir-info-panel")
        ])
    ])
])


# ============================================================
# ➡️ CALLBACKS DE LA APLICACIÓN
# ============================================================

# --- 1. CÁLCULO AUTOMÁTICO DE R0 ---
@callback(
    Output('r0-value-display', 'children'),
    Input('input-beta-sir', 'value'),
    Input('input-gamma-sir', 'value')
)
def actualizar_r0(beta: Union[float, None], gamma: Union[float, None]) -> str:
    """Calcula y muestra R₀ a partir de β y γ."""
    if beta is not None and gamma is not None and gamma > 0:
        return f"R₀ = {beta / gamma:.4f}" # Mayor precisión para R0
    return "R₀ = No definido"


# --- 2. AJUSTE AUTOMÁTICO DE S0 + I0 + R0 = N ---
@callback(
    [Output('input-s0-sir', 'value'),
     Output('input-i0-sir', 'value'),
     Output('input-r0-sir', 'value')],
    Input('input-n-sir', 'value'),
    [State('input-s0-sir', 'value'),
     State('input-i0-sir', 'value'),
     State('input-r0-sir', 'value')]
)
def actualizar_poblacion_total(N: int, S0: int, I0: int, R0: int) -> Tuple[int, int, int]:
    """Asegura que S₀ + I₀ + R₀ siempre sea igual a N."""
    # Validación inicial de tipos y existencia
    if None in [N, S0, I0, R0]:
        # Retorna los valores actuales si falta alguno, esperando la siguiente actualización
        return S0, I0, R0 

    total_actual = S0 + I0 + R0

    # Lógica de reescalado
    if total_actual != N:
        if total_actual > 0:
            # Reescalar proporcionalmente
            factor = N / total_actual
            S0_nuevo = int(S0 * factor)
            I0_nuevo = int(I0 * factor)
            # Asegura que la suma sea exactamente N debido a los redondeos
            R0_nuevo = N - S0_nuevo - I0_nuevo 
            
            return S0_nuevo, I0_nuevo, R0_nuevo
        else:
            # Si la suma es 0, asigna N a S0 (o distribuye según preferencia)
            return N, 0, 0

    # Si ya son iguales, no hay cambios
    return S0, I0, R0


# --- 3. GENERAR Y ACTUALIZAR SIMULACIÓN ---
@callback(
    [Output('grafico-sir-interactivo', 'figure'),
     Output('simulation-info', 'children')],
    Input('btn-generar', 'n_clicks'),
    [State('input-s0-sir', 'value'),
     State('input-i0-sir', 'value'),
     State('input-r0-sir', 'value'),
     State('input-beta-sir', 'value'),
     State('input-gamma-sir', 'value'),
     State('input-t-max-sir', 'value')]
)
def actualizar_grafica_sir(
    n_clicks: int, S0: int, I0: int, R0: int, beta: float, gamma: float, t_max: int
) -> Tuple[go.Figure, Union[html.Div, str]]:
    """Ejecuta la simulación SIR y actualiza la gráfica y el resumen."""

    # Se ejecuta solo si el botón ha sido presionado al menos una vez
    if n_clicks is None or n_clicks == 0:
        return _fig_placeholder("Presiona 'Generar Simulación' para empezar."), "Esperando parámetros..."

    # Validación de entradas (Null check)
    if None in [S0, I0, R0, beta, gamma, t_max]:
        fig_err = _fig_error("Error: Complete todos los campos de entrada.", t_max)
        return fig_err, html.Div("❌ Error: Todos los campos deben estar completos y ser numéricos.", className="error-message")

    # Validación de población
    N = S0 + I0 + R0
    if N <= 0 or S0 < 0 or I0 < 0 or R0 < 0:
        fig_err = _fig_error("Error: La población debe ser positiva.", t_max)
        return fig_err, html.Div("❌ Error: La población total (N) y sus componentes (S₀, I₀, R₀) deben ser mayores a cero.", className="error-message")

    if beta < 0 or gamma < 0 or t_max < 0:
        fig_err = _fig_error("Error: Parámetros inválidos.", t_max)
        return fig_err, html.Div("❌ Error: Las tasas de contagio (β), recuperación (γ) y el tiempo máximo deben ser positivos.", className="error-message")


    try:
        # Ejecutar la simulación principal
        fig, R0_val, t_pico, v_pico, S_fin, R_fin, ataque = generar_grafico_sir(
            S0, I0, R0, beta, gamma, t_max
        )

        # Lógica de interpretación de R₀
        if R0_val > 1.01: # Usamos un pequeño buffer para evitar errores de coma flotante cerca de 1
            comportamiento = "Epidemia en **crecimiento** (el juego se propagará ampliamente)"
            clase_comp = "status-critical"
        elif R0_val < 0.99:
            comportamiento = "Epidemia en **declive** (el juego no se propagará)"
            clase_comp = "status-safe"
        else:
            comportamiento = "**Estado estacionario** (propagación muy limitada)"
            clase_comp = "status-warning"
        
        # Formateo de los resultados para el resumen
        info = html.Div(className="simulation-summary", children=[
            html.H4("Resumen de la Simulación", className="info-title"),

            html.Div(className="info-details", children=[
                html.P([html.Strong("Población total (N): "), f"{N:,.0f} personas"]),
                html.P([html.Strong("Número reproductivo básico: "), html.Span(f"R₀ = {R0_val:.3f}", className="r0-result")]),
                html.P([html.Strong("Comportamiento: "), html.Span(comportamiento, className=clase_comp)]),

                html.Hr(className="info-separator"),

                html.P([html.Strong("Pico de infección: "), f"{v_pico:,.0f} infectados activos"]),
                html.P([html.Strong("Día del pico: "), f"Día {t_pico:.1f}"]),

                html.Hr(className="info-separator"),

                html.P([html.Strong("Susceptibles finales (S): "),
                        f"{S_fin:,.0f} personas ({S_fin/N*100:.1f}%)"]),
                html.P([html.Strong("Recuperados finales (R): "),
                        f"{R_fin:,.0f} personas"]),
                html.P([html.Strong("Tasa de ataque final: "),
                        html.Span(f"{ataque:.1f}% de la población total", className="attack-rate-value")])
            ])
        ])

        return fig, info

    except Exception as e:
        # Manejo de errores de ejecución
        fig_err = _fig_error("Error en la simulación (ODE)", t_max)
        return fig_err, html.Div([
            html.H4("❌ Error de Ejecución"),
            html.P(f"Ocurrió un error al intentar resolver las ecuaciones: {str(e)}", className="error-message")
        ])


# ============================================================
# 🛠️ FUNCIONES AUXILIARES DE GRÁFICO
# ============================================================
def _fig_error(msg: str, t_max: int = 365) -> go.Figure:
    """Genera una figura de Plotly para mostrar un mensaje de error."""
    fig = go.Figure()
    fig.add_annotation(
        text=msg,
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=20, color="#d62728")
    )
    fig.update_layout(
        title="",
        xaxis_title='Tiempo (días)',
        yaxis_title='Población',
        xaxis=dict(range=[0, t_max]),
        template='plotly_white',
        height=550
    )
    return fig

def _fig_placeholder(msg: str) -> go.Figure:
    """Genera una figura de Plotly para mostrar un mensaje de inicio."""
    fig = go.Figure()
    fig.add_annotation(
        text=msg,
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=20, color="#7f7f7f")
    )
    fig.update_layout(
        title="",
        xaxis_title='Tiempo (días)',
        yaxis_title='Población',
        template='plotly_white',
        height=550
    )
    return fig