# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 21:08:07 2023

@author: aleja
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import nlp

# Estilo oscuro de dash dbc
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Estilos personalizados
styles = {
    "big_star": {
        "fontSize": "2rem",    # Aumenta el tamaño de las estrellas
        "animation": "spin 5s linear infinite"   # Añade una animación de giro
    }
}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Web Scraper TF-IDF", style=styles["big_star"]),
            dbc.Input(id="input-domain", type="text", placeholder="Introduce un dominio (e.g., https://ejemplo.com)"),
            dbc.RadioItems(
                id="input-language",
                options=[
                    {"label": "Spanish", "value": "spanish"}
                ],
                value="spanish",
                inline=True
            ),
            html.Br(),
            dbc.Button("Analizar", id="submit-button", color="primary", n_clicks = 0),
            html.Br(), 
            html.Div(children= "Espera a que cargue", id='mensaje_espera',style = {"display":"none"}),
            html.Br(),
            html.Div(id="output-container")
        ], width=6)
    ], justify="center")  # Centrar el contenido
])

@app.callback(
    Output("output-container", "children"),
    Output("mensaje_espera", "style"),
    Input("submit-button", "n_clicks"),
    [
        dash.dependencies.State("input-domain", "value"),
        dash.dependencies.State("input-language", "value")
    ]
)
def update_output(n_clicks, domain, language):
    if n_clicks and n_clicks > 0:
        urls = nlp.find_internal_links(domain, domain)
        print('Estas son las urls:', urls)
        tfidf_sorting = nlp.compute_tfidf_for_urls(urls, language)
        top_words_tf_idf = nlp.get_top_n_words(tfidf_sorting)
    #    top_words = []
    #    for words in top_words_tf_idf:
    #        top_words.append(nlp.get_most_similar_words(words))

        children = []
        for url, words in zip(urls, top_words_tf_idf):
            children.append(html.H5(url))
            children.append(html.P(", ".join(words)))
            children.append(html.Hr())

        return children, {}
    return "Introduce un dominio y pulsa 'Analizar'", {"display":"none"}

if __name__ == "__main__":
    app.run_server(debug=False)
