import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests
import plotly.express as px
import pandas as pd
import urllib.parse

dash.register_page(
    __name__,
    path="/clima-global",
    name="Clima Global"
)

# ============================================================
# 1. FUNCIÓN PARA OBTENER LAT/LON DE UNA CIUDAD (GEOCODING)
# ============================================================
def geocode(ciudad):

    ciudad_encoded = urllib.parse.quote(ciudad)

    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={ciudad_encoded}&format=json&limit=1"
    )

    headers = {
        "User-Agent": "ClimaDashApp/1.0 (contacto: ejemplo@gmail.com)"
    }

    r = requests.get(url, headers=headers)

    try:
        data = r.json()
    except Exception:
        return None

    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "name": data[0]["display_name"],
    }


# ============================================================
# 2. FUNCIÓN PARA OBTENER CLIMA
# ============================================================
def obtener_clima(lat, lon):
    url_meteo = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&hourly=temperature_2m"
    )

    r = requests.get(url_meteo)
    data = r.json()

    if "hourly" not in data:
        return None

    horas = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "Hora": pd.to_datetime(horas),
        "Temperatura (°C)": temps,
    })

    return df


# ============================================================
# 3. LAYOUT
# ============================================================
layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody([
                html.H2(
                    "🌍 Clima Global por Ciudad",
                    className="text-center mb-4",
                    style={"fontWeight": "bold", "color": "#00a8e8"},
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                id="ciudad-input",
                                placeholder="Escribe una ciudad (ej: Lima, Madrid, Tokyo)",
                                type="text",
                                className="shadow-sm",
                                style={
                                    "height": "50px",
                                    "borderRadius": "12px",
                                    "border": "3px solid #00a8e8",
                                    "fontSize": "17px"
                                },
                            ),
                            md=8
                        ),

                        dbc.Col(
                            dbc.Button(
                                "🔍 Buscar Clima",
                                id="btn-buscar",
                                className="w-100 shadow",
                                style={
                                    "height": "50px",
                                    "borderRadius": "12px",
                                    "backgroundColor": "#00b4d8",
                                    "border": "none",
                                    "fontWeight": "bold",
                                    "color": "white",
                                    "fontSize": "16px"
                                },
                                n_clicks=0
                            ),
                            md=4
                        ),
                    ],
                    className="mb-4"
                ),

                html.Div(
                    id="info-ciudad",
                    className="mt-3",
                    style={"fontSize": "17px"}
                ),
            ]),
            className="shadow-lg p-4",
            style={"borderRadius": "18px", "backgroundColor": "#ffffff"}
        ),

        dbc.Card(
            dbc.CardBody([
                html.H4(
                    "📈 Variación Horaria de Temperatura",
                    className="text-center mb-3",
                    style={"color": "#0077b6"}
                ),

                dcc.Loading(
                    dcc.Graph(id="grafico-temp", figure={}),
                    type="circle",
                    color="#00a8e8"
                )
            ]),
            className="shadow-lg mt-4",
            style={"borderRadius": "18px", "backgroundColor": "#ffffff"}
        ),
    ],
    fluid=True,
    className="mt-4"
)


# ============================================================
# 4. CALLBACK
# ============================================================
@dash.callback(
    Output("info-ciudad", "children"),
    Output("grafico-temp", "figure"),
    Input("btn-buscar", "n_clicks"),
    State("ciudad-input", "value"),
)
def actualizar_clima(n_clicks, ciudad_input):
    if not n_clicks or not ciudad_input:
        return "", {}

    geo = geocode(ciudad_input)

    if geo is None:
        return dbc.Alert("❌ No se encontró la ciudad. Intenta otra.", color="danger"), {}

    lat = geo["lat"]
    lon = geo["lon"]
    name = geo["name"]

    df = obtener_clima(lat, lon)

    if df is None:
        return dbc.Alert("⚠ No se pudo obtener información del clima.", color="warning"), {}

    fig = px.line(
        df,
        x="Hora",
        y="Temperatura (°C)",
        title=f"Temperatura por Hora — {ciudad_input.capitalize()}",
    )
    fig.update_layout(template="simple_white")

    info = dbc.Alert(
        [
            html.H5("📌 Ciudad encontrada:"),
            html.P(name),
            html.P(f"Latitud: {lat:.4f} | Longitud: {lon:.4f}"),
        ],
        color="info"
    )

    return info, fig
