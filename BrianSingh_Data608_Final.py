#Import Packages for use
from dash import Dash, dcc, html, Input, Output
import pandas as pd
from dash import dcc
import plotly.express as px
from dash import dash_table, Input, Output
from urllib.request import urlopen
import json

#Import data and cleanse/tidy
covid_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
                             dtype={"fips": str})
covid_data2 = covid_data

#convert date field to a pandas datetime value in order to group by year for plotting
covid_data2['date'] = pd.to_datetime(covid_data2['date'])
covid_data2['date'] = covid_data2['date'].dt.year

#calculate covid death rate as # of deaths divided by # of cases * 100
covid_data2['death_rate'] = covid_data2['deaths'] / covid_data2['cases'] * 100

#Create app
app4 = Dash(__name__)
app4.layout = html.Div(children=[
    #headers
    html.H1(children='Brian Singh_FinalProject_Data608'),

    html.Div(children='''
        COVID19 Death Rates by County from 2020-2022.
    '''),

    #establish graph for callbacks
    dcc.Graph(
        id='graph'
    ),

    #create slider for years in the data set, with default value set at minimum year and slider marks labeled as the years
    dcc.Slider(
        covid_data2['date'].min(),
        covid_data2['date'].max(),
        step=None,
        id='crossfilter-date-slider',
        value=covid_data2['date'].min(),
        marks={str(date): str(date) for date in covid_data2['date'].unique()}
    )
])

#Callback with slider input
@app4.callback(
    Output('graph', 'figure'),
    Input('crossfilter-date-slider', 'value')
)


def covid_map(date_value):
    #for the year selected, filter covid data for plotting
    filter_date = covid_data2[covid_data2.date == date_value]
    #establish geoson county map for plotting fips data
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    #create choropleth map, plotting death rate, coloring by county (yellow = worse, dark blue = best)
    fig = px.choropleth(filter_date, geojson=counties, locations='fips', color='death_rate',
                         color_continuous_scale="Viridis",
                         range_color=(0, 8),
                         scope="usa", labels={'death_rate': 'Death Rate %'})
    #fig3.update_geos(fitbounds="locations", visible=False)
    #fig3.update_layout()
    # return fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app4.run_server(debug=True)

'''
Resources:
https://plotly.com/python/choropleth-maps/
https://community.sisense.com/t5/knowledge/plotly-choropleth-with-slider-map-charts-over-time/ta-p/9387
https://www.gabegaz.com/handson/charts_with_year_slider/
'''