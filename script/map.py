import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from urllib.request import urlopen
import json
import pyreadr

# Pull in the Presidential data from the paper
def get_data():
    result = pyreadr.read_r('data/dataverse_shareable_presidential_county_returns_1868_2020.Rdata')
    df = result['pres_elections_release']
    df['dem_pct_margin'] = (df['democratic_raw_votes'] - df['republican_raw_votes']) / df['pres_raw_county_vote_totals_two_party']
    return df

def get_margins(df : pd.DataFrame()
                ):
    base_df = df[['state',
                     'election_year',
                     'dem_nominee',
                     'rep_nominee',
                     'democratic_raw_votes',
                     'republican_raw_votes',
                     'raw_county_vote_totals']]
    grouped_df = base_df.groupby(['state', 'election_year', 'dem_nominee', 'rep_nominee']).sum().reset_index()
    grouped_df['dem_share'] = grouped_df['democratic_raw_votes'] / grouped_df['raw_county_vote_totals']
    grouped_df['rep_share'] = grouped_df['republican_raw_votes'] / grouped_df['raw_county_vote_totals']
    melted_df = grouped_df.melt(id_vars=['state','election_year'],value_vars=['dem_nominee','rep_nominee'],value_name='candidate',var_name='party')
    melted_df['vote_share'] = grouped_df.melt(id_vars=['state','election_year'], value_vars=['dem_share','rep_share'],value_name='vote_share')['vote_share']
    melted_df.loc[melted_df['party']=='dem_nominee','candidate_name'] = melted_df.loc[melted_df['party']=='dem_nominee','candidate'].astype(str) + ' (D)'
    melted_df.loc[melted_df['party']=='rep_nominee','candidate_name'] = melted_df.loc[melted_df['party']=='rep_nominee','candidate'].astype(str) + ' (R)'
    melted_df['pct_vote_share'] = round(melted_df['vote_share']*100,2).astype(str) + '%'
    return melted_df

# Pull in geojson information from Plotly master datasets
def get_geojson():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        geo = json.load(response)
    return geo

# Initialize dataframes
parsed_df = get_data()
counties = get_geojson()
state_level_df = get_margins(parsed_df)

# Inputs a list of years and a state abbrev, outputs HTML with the county swings and saves to directory
def create_subplots(years: list,
                    state: int,
                    df: pd.DataFrame = parsed_df,
                    label_df : pd.DataFrame = state_level_df,
                    geography: dict = counties,
                    code: str = 'fips',
                    name: str = 'county_name'
                    ):
    cycles = len(years)
    years.sort()

    # Initialize subplots, these are horizontal, you could adjust rows and columns to make it vertical
    figure = make_subplots(rows=2,
                           cols=cycles,
                           specs=[cycles*[{"type": "choropleth"}],
                                  cycles*[{'type': 'table',
                                           'l': 0.06,
                                           'r': 0.06
                                           }]],
                           subplot_titles=[str(year) for year in years],
                           vertical_spacing=0.01,
                           horizontal_spacing=0,
                           row_heights=[.8,.2]
                           )
    input_df = df.loc[df['state'] == state]

    # Creates each state plot
    for i in range(len(years)):
        figure.add_trace(trace=go.Choropleth(
                         geojson=geography,
                         locations=input_df.loc[input_df['election_year'] == years[i], code],
                         colorscale='RdBu',
                         z=input_df.loc[input_df['election_year'] == years[i], 'dem_pct_margin'],
                         text=input_df.loc[input_df['election_year'] == years[i], name],
                         zmid=0,
                         zmin=-1,
                         zmax=1,
                         showlegend=False
                         ),
                         row=1,
                         col=i+1)

    label_input_df = label_df.loc[label_df['state'] == state]
    for i in range(len(years)):
        figure.add_trace(trace=go.Table(
                         columnwidth=[.8,.2],
                         header=dict(fill_color='white',
                                     line_color='white',
                                     font_size=1,
                                     height=0),
                         cells=dict(values=label_input_df.loc[label_input_df['election_year']==years[i],['candidate_name','pct_vote_share']].transpose().values.tolist(),
                                    fill_color='white',
                                    line_color='white',
                                    font_size=12,
                                    height=20)
                         ),
                         row=2,
                         col=i+1)

    # Focuses the map onto the state in question
    figure.update_geos(fitbounds="locations",
                       visible=False)

    # Rough sizing, this is imperfect still
    figure.update_layout(height=333,
                         width=500*cycles,
                         margin={"r": 0, "t": 50, "l": 0, "b": 0},
                         dragmode=False)
    return figure

# Example years and state
# cyc = [2008,2020]
# st = 'AK'

# Example run
# fig = create_subplots(cyc, st)
#fig.write_html('results/result.html', auto_open = False)
# fig.show()
