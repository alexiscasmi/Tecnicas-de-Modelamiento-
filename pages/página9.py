import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import numpy as np
from scipy.optimize import curve_fit
import requests

dash.register_page(__name__, path='/malaria-ajuste', name='SEIR-SEI')

def obtener_datos_malaria_api(pais_codigo):
    """
    Obtiene datos REALES de tu API del Banco Mundial
    """
    url = "https://data360api.worldbank.org/data360/data?DATABASE_ID=WEF_GCIHH&INDICATOR=WEF_GCIHH_MALARIAPC&skip=0"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        años = []
        rankings = []
        
        for item in data['value']:
            if (item.get('REF_AREA') == pais_codigo and 
                item.get('OBS_VALUE') is not None and
                item.get('TIME_PERIOD') is not None and
                item.get('UNIT_MEASURE') == 'RANK'):
                
                año = int(item['TIME_PERIOD'])
                if 2007 <= año <= 2017:
                    ranking = float(item['OBS_VALUE'])
                    años.append(año)
                    rankings.append(ranking)
        
        if años:
            datos_ordenados = sorted(zip(años, rankings))
            años_ordenados = [d[0] for d in datos_ordenados]
            rankings_ordenados = [d[1] for d in datos_ordenados]
            return años_ordenados, rankings_ordenados
        else:
            return None, None
            
    except Exception as e:
        print(f"Error API: {e}")
        return None, None

def transformar_ranking_a_casos(rankings):
    """
    Convierte rankings a números que se parezcan a casos de malaria
    Ranking 1 = muchos casos, Ranking alto = pocos casos
    """
    rankings = np.array(rankings)
    casos_estimados = 100000 / (rankings + 10)
    return casos_estimados * 80

def modelo_ranking_malaria(t, a, b, c, d):
    """
    Modelo para ajustar la evolución de rankings/casos de malaria
    """
    return a * np.exp(-b * t) + c * t + d

def ajuste_minimos_cuadrados(x_data, y_data, modelo, parametros_iniciales):
    try:
        parametros_optimos, pcov = curve_fit(
            modelo, x_data, y_data, 
            p0=parametros_iniciales,
            maxfev=5000
        )
        y_pred = modelo(x_data, *parametros_optimos)
        return parametros_optimos, y_pred, pcov
    except Exception as e:
        raise Exception(f"Error en ajuste: {str(e)}")

paises = [
    {"label": "Argentina", "value": "ARG"},
    {"label": "Brazil", "value": "BRA"},
    {"label": "Cambodia", "value": "KHM"},
    {"label": "Colombia", "value": "COL"},
    {"label": "China", "value": "CHN"},
    {"label": "Ecuador", "value": "ECU"},
    {"label": "El Salvador", "value": "SLV"},
    {"label": "Ghana", "value": "GHA"},
    {"label": "India", "value": "IND"},
    {"label": "Republica Dominicana", "value": "DOM"}
]

layout = html.Div([
    html.H2("Ajuste por Mínimos Cuadrados - Datos Reales de API", 
             style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': '20px'}),
    
    html.Div([
        html.H4("Metodología del Artículo Aplicada a Datos Reales"),
        html.P("• Fuente: API Banco Mundial - Rankings de Malaria"),
        html.P("• Período: 2007-2017"),
        html.P("• Método: Mínimos cuadrados no lineales"),
        html.P("• Transformación: Rankings → Casos estimados")
    ], style={
        'backgroundColor': '#f8f9fa', 
        'padding': '20px', 
        'borderRadius': '10px',
        'marginBottom': '20px'
    }),
    
    html.Div([
        html.Label("Selecciona país:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='selector-pais',
            options=paises,
            value='GHA',
            style={'width': '300px'}
        )
    ], style={'marginBottom': '20px'}),
    
    html.Button("Ejecutar Mínimos Cuadrados con API Real", 
                id="btn-ajuste", 
                style={
                    'backgroundColor': '#2E86AB', 
                    'color': 'white', 
                    'padding': '12px 24px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }),
    
    html.Br(), html.Br(),
    
    dcc.Graph(id="grafica-ajuste"),
    
    html.Div(id="resultados-ajuste", style={'marginTop': '30px'})
])

@callback(
    [Output("grafica-ajuste", "figure"),
     Output("resultados-ajuste", "children")],
    [Input("btn-ajuste", "n_clicks"),
     Input("selector-pais", "value")]
)
def ejecutar_ajuste_api_real(n_clicks, pais_seleccionado):
    if n_clicks is None:
        fig = go.Figure()
        fig.update_layout(
            title="Selecciona un país y presiona el botón",
            xaxis_title="Año",
            yaxis_title="Casos de Malaria (estimados)"
        )
        return fig, ""
    
    try:
        años, rankings = obtener_datos_malaria_api(pais_seleccionado)
        
        if años is None or rankings is None:
            return go.Figure(), html.Div([
                html.H4("Datos no disponibles"),
                html.P(f"No se encontraron datos para {pais_seleccionado} en 2007-2017"),
                html.P("Intenta con otro país como Ghana, Nigeria, Kenya...")
            ], style={'backgroundColor': '#ffebee', 'padding': '15px', 'borderRadius': '10px'})
        
        casos_estimados = transformar_ranking_a_casos(rankings)
        
        t = np.array(años) - min(años)
        y = casos_estimados
        
        parametros_iniciales = [max(y)-min(y), 0.1, 0.1, min(y)]
        
        parametros_optimos, y_pred, covarianza = ajuste_minimos_cuadrados(
            t, y, modelo_ranking_malaria, parametros_iniciales
        )
        
        a_opt, b_opt, c_opt, d_opt = parametros_optimos
        
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_cuadrado = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        t_suave = np.linspace(min(t), max(t), 300)
        y_suave = modelo_ranking_malaria(t_suave, *parametros_optimos)
        años_suave = t_suave + min(años)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=años, y=casos_estimados,
            mode='markers',
            name='data',
            marker=dict(size=8, color='red', symbol='circle'),
            hovertemplate='<b>Año:</b> %{x}<br><b>Casos estimados:</b> %{y:,.0f}<br><b>Ranking real:</b> %{customdata}',
            customdata=rankings
        ))
        
        fig.add_trace(go.Scatter(
            x=años_suave, y=y_suave,
            mode='lines',
            name='bestfit',
            line=dict(color='blue', width=3),
            hovertemplate='<b>Año:</b> %{x:.1f}<br><b>Modelo:</b> %{y:,.0f} casos<extra></extra>'
        ))
        
        nombre_pais = next((p["label"] for p in paises if p["value"] == pais_seleccionado), pais_seleccionado)
        
        fig.update_layout(
            title=dict(
                text=f'<b>Gráfico de la media de los datos - {nombre_pais}</b><br>'
                     f'<sub>Datos reales: Rankings de Malaria {min(años)}-{max(años)} | API Banco Mundial</sub>',
                x=0.5
            ),
            xaxis_title='Año',
            yaxis_title='Casos de Malaria Estimados',
            showlegend=True,
            hovermode='x unified',
            annotations=[
                dict(
                    x=0.02, y=0.98,
                    xref="paper", yref="paper",
                    text="• data<br>— bestfit",
                    showarrow=False,
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            ]
        )
        
        resultados_html = html.Div([
            html.H4(f"Resultados - {nombre_pais}"),
            
            html.Div([
                html.H5("Datos Originales (API):"),
                html.P(f"• Período: {min(años)}-{max(años)}"),
                html.P(f"• Rankings: {rankings}"),
                html.P(f"• Países en ranking: ~140 países")
            ], style={'backgroundColor': '#e3f2fd', 'padding': '15px', 'borderRadius': '5px'}),
            
            html.Div([
                html.H5("Parámetros Estimados por Mínimos Cuadrados:"),
                html.P(f"• a (componente exponencial): {a_opt:.4f}"),
                html.P(f"• b (tasa de cambio): {b_opt:.4f}"),
                html.P(f"• c (tendencia lineal): {c_opt:.4f}"),
                html.P(f"• d (nivel base): {d_opt:.4f}")
            ], style={'backgroundColor': '#e8f5e9', 'padding': '15px', 'borderRadius': '5px', 'marginTop': '10px'}),
            
            html.Div([
                html.H5("Métricas de Ajuste:"),
                html.P(f"• R² (bondad de ajuste): {r_cuadrado:.4f}"),
                html.P(f"• Suma de cuadrados de residuos: {ss_res:.2f}"),
                html.P(f"• Número de puntos: {len(años)}"),
                html.P("• Método: Mínimos cuadrados no lineales")
            ], style={'backgroundColor': '#fff3e0', 'padding': '15px', 'borderRadius': '5px', 'marginTop': '10px'}),
            
            html.Div([
                html.H5("Interpretación:"),
                html.P("• Ranking 1 = mejor posición (menos malaria)"),
                html.P("• Ranking alto = peor posición (más malaria)"),
                html.P("• Transformación: ranking → casos estimados para visualización"),
                html.P("• Modelo ajusta la tendencia temporal de la malaria")
            ], style={'backgroundColor': '#fce4ec', 'padding': '15px', 'borderRadius': '5px', 'marginTop': '10px'})
            
        ])
        
        return fig, resultados_html
        
    except Exception as e:
        fig_error = go.Figure()
        fig_error.add_annotation(text=f"Error: {str(e)}", x=0.5, y=0.5, showarrow=False)
        
        mensaje_error = html.Div([
            html.H4("Error en el análisis"),
            html.P(f"Detalle: {str(e)}"),
            html.P("Posibles soluciones:"),
            html.Ul([
                html.Li("Verifica tu conexión a internet"),
                html.Li("Intenta con otro país"),
                html.Li("La API podría estar temporalmente no disponible")
            ])
        ], style={'backgroundColor': '#ffebee', 'padding': '15px', 'borderRadius': '10px'})
        
        return fig_error, mensaje_error