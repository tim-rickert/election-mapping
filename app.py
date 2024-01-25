from dash import Dash, html, dcc, Input, Output, callback
from script.map import get_data, get_margins, get_geojson, create_subplots

app = Dash(__name__)

states = {"Alabama": "AL",
          "Alaska": "AK",
          "Arizona": "AZ",
          "Arkansas": "AR",
          "California": "CA",
          "Colorado": "CO",
          "Connecticut": "CT",
          "Delaware": "DE",
          "Florida": "FL",
          "Georgia": "GA",
          "Hawaii": "HI",
          "Idaho": "ID",
          "Illinois": "IL",
          "Indiana": "IN",
          "Iowa": "IA",
          "Kansas": "KS",
          "Kentucky": "KY",
          "Louisiana": "LA",
          "Maine": "ME",
          "Maryland": "MD",
          "Massachusetts": "MA",
          "Michigan": "MI",
          "Minnesota": "MN",
          "Mississippi": "MS",
          "Missouri": "MO",
          "Montana": "MT",
          "Nebraska": "NE",
          "Nevada": "NV",
          "New Hampshire": "NH",
          "New Jersey": "NJ",
          "New Mexico": "NM",
          "New York": "NY",
          "North Carolina": "NC",
          "North Dakota": "ND",
          "Ohio": "OH",
          "Oklahoma": "OK",
          "Oregon": "OR",
          "Pennsylvania": "PA",
          "Rhode Island": "RI",
          "South Carolina": "SC",
          "South Dakota": "SD",
          "Tennessee": "TN",
          "Texas": "TX",
          "Utah": "UT",
          "Vermont": "VT",
          "Virginia": "VA",
          "Washington": "WA",
          "West Virginia": "WV",
          "Wisconsin": "WI",
          "Wyoming": "WY",
          "District of Columbia": "DC"}

years = list(range(1868,2021,4))

# Initialize dataframes
parsed_df = get_data()
counties = get_geojson()
state_level_df = get_margins(parsed_df)

app.layout = html.Div(children=[
    html.Label('State:'),
    dcc.Dropdown(list(states.keys()),id='state'),
    html.Br(),
    html.Label('Cycle:'),
    dcc.Dropdown(years,multi=True,id='cycles'),
    html.Br(),
    dcc.Graph(id='election-maps')
    ])

@callback(
    Output('election-maps', 'figure'),
    Input('cycles', 'value'),
    Input('state', 'value'))
def graph_states(cycles, state):
    fig = create_subplots(cycles, states[state])
    return fig

if __name__ == '__main__':
    app.run(debug=True)