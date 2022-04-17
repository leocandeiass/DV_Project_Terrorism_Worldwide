import pandas as pd
import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_excel("data.xlsx")
df["Number Killed"].fillna(0, inplace = True)
df.dropna(inplace=True)
df = df[df['Number Killed']!=0]
df["Total Affected"] = df["Number Killed"] + df["Number Wounded"]

country_options = []
for country in df['Country'].unique():
    country_options.append({'label':str(country),'value':country})

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Terror Attacks'),

    html.Br(),

    html.H2("Global View of Terrorist Attack from 2010 to 2017"),

    dcc.Graph(id='fig'),

    html.Br(),

    html.Br(),

    dcc.Graph(id='fig3'),

    html.H2("Filtered View of Terrorist Attack from 2010 to 2017"),

    dcc.Dropdown(id ="country_picker",options=country_options,value=["Afghanistan","Pakistan"], multi = True),

    dcc.Graph(id='world_graph'),

    html.Br(),

    dcc.Graph(id='line_graph'),

    html.Br(),

    dcc.Graph(id='fig_tree'),

    html.Br(),

])

@app.callback(
    [Output('world_graph', 'figure'),
    Output('line_graph', 'figure'),
    Output('fig_tree', 'figure'),
    Output('fig', 'figure'),
    Output('fig3', 'figure')],
     Input('country_picker', 'value')
)

def update_graph(country_picker):

    filtered_df = df[df["Country"].isin(country_picker)]
    fig_world = px.scatter_geo(filtered_df, lat = "latitude", lon="longitude", color="success",
                     hover_name="city", size="Number Killed",
                     animation_frame="Year",
                     projection="miller")
    
    fig_world.update_layout(
    margin=dict(l=20, r=20, t=20, b=20))
    
    fig_world.update_geos(fitbounds="locations", showcountries = True, showsubunits = True)
    
    fig_bar = px.histogram(df[df["Country"].isin(country_picker)], x="Month", y="Number Killed",
                     color="Country", text_auto=True, animation_frame="Year",
                     barmode="group", height=500)
    
    fig_bar.update_layout(yaxis_range=[0,300], margin=dict(l=20, r=20, t=20, b=20))

    fig_tree = px.treemap(df[df["Country"].isin(country_picker)], path=[px.Constant('world'), 'Country', 'Terrorist Gang Name'], values='Total Affected',
                  color='Number Killed')

    fig = px.scatter_mapbox(df, lat = "latitude", lon="longitude", hover_name="city",hover_data=["Country", "Number Killed"], title= "Global Terrorism",
                            color_discrete_sequence=["fuchsia"], zoom = 1, animation_frame="Year")
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig3 = px.ecdf(df, x="Year", y="Total Affected", color="Region",  ecdfnorm=None, orientation="v")



    return fig_world, fig_bar, fig_tree, fig, fig3



if __name__ == '__main__':
    app.run_server(debug=True)
