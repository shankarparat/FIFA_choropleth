import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Data setup
data = {
    "Year": [
        1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978,
        1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022
    ],
    "Winner": [
        "Uruguay", "Italy", "Italy", "Uruguay", "West Germany", "Brazil", "Brazil", "England",
        "Brazil", "West Germany", "Argentina", "Italy", "Argentina", "West Germany", "Brazil",
        "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"
    ],
    "Runner-Up": [
        "Argentina", "Czechoslovakia", "Hungary", "Brazil", "Hungary", "Sweden", "Czechoslovakia", "West Germany",
        "Italy", "Netherlands", "Netherlands", "West Germany", "West Germany", "Argentina", "Italy",
        "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"
    ]
}

df = pd.DataFrame(data)
df.replace({"West Germany": "Germany"}, inplace=True)

winnercount = df["Winner"].value_counts().reset_index()
winnercount.columns = ["Winner", "Count"]

# Dash app
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={"textAlign": "center"}),

    html.Div([
        html.H2("World Cup Wins by Country (Choropleth Map)"),
        dcc.Graph(id='choropleth-map')
    ], style={"marginBottom": 50}),

    html.Div([
        html.Label("Select a country to view number of wins:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": c, "value": c} for c in sorted(winnercount["Winner"].unique())],
            value="Brazil"
        ),
        html.Div(id='country-output', style={"marginTop": 10})
    ], style={"marginBottom": 50}),

    html.Div([
        html.Label("Select a World Cup year to view winner and runner-up:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(y), 'value': y} for y in sorted(df['Year'])],
            value=2022
        ),
        html.Div(id='year-output', style={"marginTop": 10})
    ])
])

# Choropleth callback
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_choropleth():
    fig = px.choropleth(
        winnercount,
        locations="Winner",
        locationmode="country names",
        color="Count",
        color_continuous_scale="Blues",
        title="Countries that have won the FIFA World Cup"
    )
    return fig

# Country wins callback
@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    wins = winnercount[winnercount['Winner'] == selected_country]['Count'].values[0]
    return f"{selected_country} has won the FIFA World Cup {wins} time(s)."

# Year result callback
@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    row = df[df['Year'] == selected_year].iloc[0]
    return f"In {selected_year}, the winner was {row['Winner']} and the runner-up was {row['Runner-Up']}."

# Final server run for Render
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
