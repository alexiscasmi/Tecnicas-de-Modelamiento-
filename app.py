import dash
from dash import html, dcc

# Crear app con soporte para pages
app = dash.Dash(__name__, use_pages=True)

# Orden deseado de las páginas
orden_paginas = ['/', '/pagina1', '/pagina2']

# Obtener las páginas registradas
paginas_registradas = dash.page_registry.values()

# Ordenar las páginas según el orden deseado
paginas_ordenadas = sorted(
    paginas_registradas,
    key=lambda page: orden_paginas.index(page['path']) if page['path'] in orden_paginas else len(orden_paginas)
)

# Layout principal
app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className='app-header'),

    # Menú de navegación ordenado
    html.Div([
        html.Div([
            dcc.Link(
                f"{page['name']}", 
                href=page["relative_path"], 
                className='nav-link'
            )
            for page in paginas_ordenadas
        ], className='nav-links')
    ], className='navigation'),

    # Contenedor de páginas
    dash.page_container
], className='app-container')

if __name__ == '__main__':
    app.run(debug=True)
