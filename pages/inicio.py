import dash
from dash import html

dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div([
    html.Div([
        # Columna izquierda — Sobre mí
        html.Div([
            html.H2("Sobre mí", className="titulo-sobremi"),
            html.P("""
                Hola, soy Alexis Aarón Castillo Milián, estudiante de Computación Científica en la
                Universidad Nacional Mayor de San Marcos. Me encuentro en formación en las áreas de
                programación, matemáticas aplicadas y resolución de problemas.
            """, className="texto-sobremi"),

            html.P("""
                Me apasiona aprender y aplicar mis conocimientos en desarrollo de software, análisis
                de datos, inteligencia artificial y simulación científica, buscando siempre conectar
                la teoría con la práctica.
            """, className="texto-sobremi"),

            html.P("""
                Actualmente estoy enfocado en fortalecer mis habilidades en programación, modelado
                matemático y trabajo en proyectos prácticos, que me permitan aplicar lo aprendido,
                desarrollar soluciones reales y seguir creciendo como profesional.
            """, className="texto-sobremi"),

            html.P("""
                En mi tiempo libre disfruto de mis hobbies como escuchar música, practicar deporte,
                explorar nuevas tecnologías y aprender sobre ciencia y computación.
            """, className="texto-sobremi")
        ], className="columna izquierda"),

        # Columna derecha — Imagen
        html.Div([
            html.Img(
                src='/assets/images/hobbie.jpg',  
                className="imagen-hobbies"
            )
        ], className="columna derecha")

    ], className="contenedor-inicio")
])
