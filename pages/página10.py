# ------------------------------------------------------------
# Imports esenciales
# ------------------------------------------------------------
import dash
from dash import html, dcc, Input, Output, callback, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint
from typing import List, Tuple, Union, Any

# ============================================================
# ⚙️ REGISTRO DE PÁGINA DASH
# ============================================================
dash.register_page(
    __name__,
    path="/Proyecto2.1",
    name="PROYECTO 2.1"
)


# ============================================================
# 🎨 LAYOUT (ESTRUCTURA HTML SEMÁNTICA)
# ============================================================
# Se utilizan las clases CSS previamente diseñadas (sir-control-panel, sir-input-row, etc.)
layout = html.Div(className="app-container", children=[
    
    html.Div(className="sir-dashboard-layout", children=[
        
        # ------------------------- PANEL DE CONTROL IZQUIERDO -------------------------
        html.Div(className="sir-control-panel", children=[
            html.H2("🗣️ Modelo SIR - Dinámica de Rumores", className="panel-title"),
            html.Hr(className="separator"),

            html.Div(className="input-section", children=[
                html.H3("Parámetros de la Simulación", className="section-subtitle"),
                
                # Input: Población total (N)
                html.Div(className="sir-input-row", children=[
                    html.Label("Población total (N):", className="sir-input-label"),
                    dcc.Input(id="sirN", type="number", value=275, min=1, className="sir-input-field form-control")
                ]),

                # Input: Tasa de transmisión (b)
                html.Div(className="sir-input-row", children=[
                    html.Label("Tasa de transmisión del rumor (b):", className="sir-input-label"),
                    dcc.Input(id="sirB", type="number", value=0.004, step=0.0001, min=0, className="sir-input-field form-control")
                ]),

                # Input: Constante de racionalización (k)
                html.Div(className="sir-input-row", children=[
                    html.Label("Constante de racionalización (k):", className="sir-input-label"),
                    dcc.Input(id="sirK", type="number", value=0.01, step=0.0001, min=0, className="sir-input-field form-control")
                ]),

                # Input: Tiempo máximo
                html.Div(className="sir-input-row", children=[
                    html.Label("Duración de la simulación (días):", className="sir-input-label"),
                    dcc.Input(id="sirTmax", type="number", value=15, min=1, className="sir-input-field form-control")
                ]),
            ]),
            html.Hr(className="separator"),

            html.Div(className="input-section", children=[
                html.H3("Población Inicial (t=0)", className="section-subtitle"),
                
                # Input: Ignorantes iniciales (S₀)
                html.Div(className="sir-input-row", children=[
                    html.Label("Ignorantes iniciales S₀:", className="sir-input-label susceptible-label"),
                    dcc.Input(id="sirS0", type="number", value=266, min=0, className="sir-input-field form-control")
                ]),

                # Input: Divulgadores iniciales (I₀)
                html.Div(className="sir-input-row", children=[
                    html.Label("Divulgadores iniciales I₀:", className="sir-input-label infected-label"),
                    dcc.Input(id="sirI0", type="number", value=1, min=0, className="sir-input-field form-control")
                ]),

                # Input: Racionales iniciales (R₀)
                html.Div(className="sir-input-row", children=[
                    html.Label("Racionales iniciales R₀:", className="sir-input-label recovered-label"),
                    dcc.Input(id="sirR0", type="number", value=8, min=0, className="sir-input-field form-control")
                ]),
            ]),
            html.Hr(className="separator"),

            # Footer y Botón
            html.Div(className="action-footer-panel", children=[
                html.Button("🔄 Reiniciar a Valores por Defecto", id="btnResetSir6", 
                            className="btn-secondary btn-lg", n_clicks=0),
                
                html.Div(
                    "Se simula la propagación de un rumor en un grupo de 275 personas, con datos iniciales observados.",
                    className="content-description" # Clase descriptiva
                )
            ])
        ]),

        # ------------------------- PANEL DE VISUALIZACIÓN DERECHO -------------------------
        html.Div(className="sir-visualization-panel", children=[
            html.H2("📈 Evolución y Dinámica del Rumor", className="panel-title"),
            
            html.Div(className="sir-graph-card", children=[
                dcc.Graph(id='graficaSIR6', style={'height': '100%', 'width': '100%'})
            ]),
            
            html.Div(className="sir-info-card", children=[
                html.H3("📝 Resumen e Interpretación", className="info-title"),
                html.Div(id="interpretacionSIR6", className="simulation-summary")
            ])
        ])
    ])
])


# ============================================================
# 🧠 MODELO Y FUNCIONES AUXILIARES
# ============================================================

def sir_rumor(y: List[float], t: float, b: float, k: float) -> List[float]:
    """
    Define el sistema de EDOs para el Modelo SIR de propagación de rumores.
    
    S: Ignorantes (Susceptibles al rumor)
    I: Divulgadores (Infectados, propagan el rumor)
    R: Racionales (Recuperados, han dejado de propagarlo)
    
    Argumentos:
        y (list): Vector de estado [S, I, R] en el tiempo t.
        t (float): Instante de tiempo (días).
        b (float): Tasa de transmisión (beta).
        k (float): Constante de racionalización (gamma).

    Retorna:
        list: Las derivadas [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = y
    
    # El modelo de rumor no divide por N, asume interacciones totales
    dSdt = -b * S * I
    dIdt = b * S * I - k * I
    dRdt = k * I
    
    return [dSdt, dIdt, dRdt]


# ============================================================
# ➡️ CALLBACKS DE LA APLICACIÓN
# ============================================================

# --- 1. Actualización del gráfico e interpretación ---
@callback(
    Output('graficaSIR6', 'figure'),
    Output('interpretacionSIR6', 'children'),
    Input('sirN', 'value'),
    Input('sirB', 'value'),
    Input('sirK', 'value'),
    Input('sirS0', 'value'),
    Input('sirI0', 'value'),
    Input('sirR0', 'value'),
    Input('sirTmax', 'value')
)
def actualizar_sir_modificado(
    N: Union[float, str], b: Union[float, str], k: Union[float, str], 
    S0: Union[float, str], I0: Union[float, str], R0: Union[float, str], 
    tmax: Union[int, str]
) -> Tuple[go.Figure, html.Div]:
    """
    Resuelve el modelo SIR del rumor, calcula el pico y genera el gráfico.
    """
    # Valores por defecto para robustez
    N_def, b_def, k_def, S0_def, I0_def, R0_def, tmax_def = 275.0, 0.004, 0.01, 266.0, 1.0, 8.0, 15
    
    # Conversión y manejo de None/Cadenas vacías
    N_val = float(N) if N else N_def
    b_val = float(b) if b else b_def
    k_val = float(k) if k else k_def
    S0_val = float(S0) if S0 else S0_def
    I0_val = float(I0) if I0 else I0_def
    R0_val = float(R0) if R0 else R0_def
    tmax_val = int(tmax) if tmax else tmax_def

    # Validación de la población total
    poblacion_sumada = S0_val + I0_val + R0_val
    if abs(poblacion_sumada - N_val) > 1e-6:
         # Usar los inputs de S0, I0, R0 y recalcular N
         N_val = poblacion_sumada
    
    # Validación de parámetros
    if tmax_val <= 0 or N_val <= 0:
        fig_err = _fig_error("Error: Población o tiempo máximo deben ser positivos.")
        return fig_err, html.Div("❌ Error: Ajuste los parámetros de población y tiempo.")
    
    if S0_val < 0 or I0_val < 0 or R0_val < 0:
        fig_err = _fig_error("Error: Poblaciones iniciales negativas.")
        return fig_err, html.Div("❌ Error: Las poblaciones iniciales no pueden ser negativas.")


    # --- Simulación del Modelo ---
    t = np.linspace(0, tmax_val, 500)
    y0 = (S0_val, I0_val, R0_val)
    try:
        sol = odeint(sir_rumor, y0, t, args=(b_val, k_val))
    except Exception:
        fig_err = _fig_error("Error en la integración del modelo SIR.", tmax_val)
        return fig_err, html.Div("❌ Error: Problema al resolver las ecuaciones diferenciales. Revise los valores de b y k.")
        
    S, I, R = sol.T

    # --- Cálculo de Indicadores ---
    pico_idx = np.argmax(I)
    dia_pico = t[pico_idx]
    maxI = I[pico_idx]
    
    # Se añade la Tasa de Racionalización/Transmisión (R_0' en algunos modelos de rumor)
    R_ratio = b_val / k_val if k_val != 0 else float('inf')

    # --- Generación de la Gráfica ---
    fig = go.Figure()

    # Trazas: Se mantienen los colores originales (pero con width mejorado)
    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Ignorantes (S)',
        line=dict(color='#458588', width=3) # Color oscuro/grisáceo
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Divulgadores (I)',
        line=dict(color='#fb4934', width=3) # Rojo/Naranja fuerte
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Racionales (R)',
        line=dict(color='#b8bb26', width=3) # Verde/Amarillo
    ))

    # Línea del pico (Destacada)
    fig.add_vline(
        x=dia_pico,
        line=dict(color='#fabd2f', width=2, dash='dot'), # Amarillo fuerte
        annotation_text=f"Pico (día {dia_pico:.1f})",
        annotation_position="top right",
        annotation_font=dict(color='#282828', size=12, family='Arial')
    )

    # Configuración de Layout y Estilo
    fig.update_layout(
        title={
            'text': f"<b>Modelo SIR – Difusión del rumor (b/k = {R_ratio:.3f})</b>",
            'x':0.5, 'y':0.92, 'xanchor': 'center', 'yanchor': 'top',
            'font':dict(size=20, color='#34495e') 
        },
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        template='plotly_white', 
        height=550,
        margin=dict(l=50, r=40, t=90, b=50),
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.05,
            xanchor='center', x=0.5
        )
    )

    # --- Generación de Interpretación Estilizada ---
    interpretacion = html.Div(className="info-details", children=[
        html.P([
            html.Strong("Contexto: "), 
            f"Grupo de {int(N_val)} personas. b (Transmisión) = {b_val:.4f}, k (Racionalización) = {k_val:.4f}."
        ]),
        html.P([
            html.Strong("Ratio b/k: "),
            html.Span(f"{R_ratio:.3f}", className="r0-value"),
            html.Span(" (Alto ratio implica mayor propagación).")
        ]),
        html.Hr(className="info-separator"),
        html.P([
            html.Strong("Pico del rumor: "), 
            f"El máximo número de divulgadores ({int(maxI)} personas) se alcanza alrededor del día {dia_pico:.1f}."
        ]),
        html.P([
            html.Strong("Conclusión: "),
            f"Al finalizar la simulación, {int(R[-1]):,} personas se habrán convertido en racionales, y {int(S[-1]):,} permanecerán ignorantes. La dinámica es consistente con la relación entre b y k."
        ])
    ])

    return fig, interpretacion


# --- 2. Callback de Reinicio ---
@callback(
    [Output('sirN', 'value'),
     Output('sirB', 'value'),
     Output('sirK', 'value'),
     Output('sirS0', 'value'),
     Output('sirI0', 'value'),
     Output('sirR0', 'value'),
     Output('sirTmax', 'value')],
    Input('btnResetSir6', 'n_clicks'),
    prevent_initial_call=True
)
def reiniciar_valores(_: int) -> Tuple[int, float, float, int, int, int, int]:
    """Restaura los valores de entrada a sus estados iniciales."""
    # Valores por defecto del ejercicio
    return 275, 0.004, 0.01, 266, 1, 8, 15

# ============================================================
# 🛠️ FUNCIONES AUXILIARES DE GRÁFICO
# ============================================================

def _fig_error(msg: str, t_max: int = 15) -> go.Figure:
    """Genera una figura de Plotly para mostrar un mensaje de error."""
    fig = go.Figure()
    fig.add_annotation(
        text=msg,
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=20, color="#dc3545")
    )
    fig.update_layout(
        title="",
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
        xaxis=dict(range=[0, t_max]),
        template='plotly_white',
        height=550
    )
    return fig