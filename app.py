import pandas as pd
import numpy as np
import dask.dataframe as dd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import xarray as xr
import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("cerulean")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
# Load the data for deployment table and dictionary for colormaps
df = pd.read_csv("data/glider_deployments.csv")
cm = {"t": "thermal",
      "s": "haline",
      "dens": "dense",
      "chl": "algae"}
# Build different components of the frame work
    # title block
jumbotron = dbc.Jumbotron(
    [
        html.H1("Glider HUB", className="display-3"),
        html.P(
            "By Lu Han (luhan@unc.edu)",
            className="lead",
        ),

        html.P(
            "These glider deployments are part of PEACH field program. "
            "PEACH is short for Processes driving Exchanges At Cape Hatteras, which aims to advance "
            "the fundamental understanding of the processes and dynamics underlying shelf-open ocean "
            "exchanges at convergent, energetically forced coastal margins. "
            "Cape Hatteras, NC, the dividing point between the Middle Atlantic Bight "
            "(MAB) and South Atlantic Bight (SAB) along the US East Coast, is an "
            "active region for shelf-open ocean exchanges due to the confluent western boundary "
            "currents and convergence of the adjacent shelf and slope waters. "
        ),
        # html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ],className="bg-primary text-white"
)

    # images of a glider and a gif of how gliders work
imag = html.Div(children=[
    html.Img(src="https://www.sequoiasci.com/wp-content/uploads/2016/10/Slocum-G2-from-Website.jpg",
             style={"width":'80%'}),
    html.Img(src="http://norgliders.gfi.uib.no/pict/glider4.gif",
             style={"width":'100%'}),
],
)
# imag = dbc.Card(
#     [
#         dbc.CardImg(src="https://www.sequoiasci.com/wp-content/uploads/2016/10/Slocum-G2-from-Website.jpg"),
#         dbc.CardImg(src="http://norgliders.gfi.uib.no/pict/glider4.gif"),
#     ], color="primary", outline=True,style={"height": "100%"}
#
# )

    # deployment table
deployment = html.Div(children=[
    html.H4("Glider Deployment Sheet"),
    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,),
],
)
# deployment = dbc.Card([
#     dbc.CardHeader(html.H4("Glider Deployment Sheet"),className='bg-primary text-white'),
#     dbc.CardBody(dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,),)
# ], color="primary", outline=True,style={"height": "100%"}
# )
    # dropdown for deployments selection
dropdown1 = dcc.Dropdown(
    id="slct_deployment",
    options=[{"label": df["glider"][i] + ' ' + df["Deployment #"][i],
              "value": df["glider"][i] + '_Deployment' + df["Deployment #"][i][-1]}
             for i in range(len(df))],
    multi=False,
    value='Ramses_Deployment1',
    clearable=False,
)
container = dbc.Card(
    [
        dbc.CardHeader(html.H4("Coordinate Transformation")),
        dbc.CardBody(
            dbc.FormGroup([dbc.Label("Select Glider Deployment"), dropdown1])
        )
    ]
)

    # dropdown for parameter selection
dropdown2 = dcc.Dropdown(
    id="slct_parameter",
    options=[{"label": 'Temperature', "value": 't'},
             {"label": 'Salinity', "value": 's'},
             {"label": 'Density', "value": 'dens'},
             {"label": 'Chlorophyll', "value": 'chl'},
             ],
    multi=False,
    value='t',
    clearable=False,
)
choose_param = dbc.Card(
    [
        dbc.CardHeader(html.H4("Water Properties: (T, S, Dens, Chlorophyll)")),
        dbc.CardBody(
            dbc.FormGroup([dbc.Label("Select One Parameter to Show in 3D View"), dropdown2])
        )
    ]
)
    # glider tracks in map view vs transformed coordinate
track = html.Div(children=[
    dbc.Row(
        [dbc.Col(dcc.Graph(id="glider_map"), className='col-6'),
         dbc.Col(dcc.Graph(id="map_tc"), className='col-6')]
    )],
)

track_caption = html.Div(children=[
    html.Figcaption(children=[
        html.H5("Glider Trajectory before and after coordinate transformation"),
        html.P(
            "On the left is the glider trajectory in the original map view. "
            "On the right is the glider trajectory in transformed semi-Lagrangian Coordinate. "
            "In this coordinate, the trajectory shows glider's movement relative to the water rather than the ground. ",
        ),
    ])
])

    # water velocity from glider
vel = html.Div(children=[
    dcc.Graph(id="time_series"),
    ])
vel_caption = html.Div(children=[
    html.Figcaption(children=[
        html.H5(
            "Depth Averaged Water Velocity from Glider"),
        html.P(
            "Under the assumption of homogenous flow, we used the depth averaged water velocity "
            "measured/computed by the glider to estimate the water movement."
        ),
    ]),
])


    # four parameters in the view of time series
ts = html.Div(
    children=
    [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id="ctd",style={"height":'100vh','margin-top':'0'})
                        ]
                    )
                ], className='h-100'
            )
    ],
)
    # choosen parameter in the 3d view (map vs transformed coordinate)
# p3d = html.Div( children=
#     [
#                 dbc.Row(
#                     [
#                         dbc.Col(dcc.Graph(id="3d_map"),),
#                     ],style={"height":'50vh'}
#                 ),
#
#     ],
# )
p3d = html.Div(
    children=
    [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id="3d_map",style={"height":'95vh'})
                        ]
                    )
                ], className='h-100'
            )
    ],
)


aboutme = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H5("A little about me...",),
                html.Br(),
                html.P(
                    "A PhD student at UNC-Chapel Hill. "
                ),
                html.P(
                    "Ten years of education in oceanography and eight years of experience in data analysis."
                ),
                html.P(
                    "Data is the gate to knowledge and analysis is the key."
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True, style={"margin-top":'20','margin-down':'0'}
)


app.layout = html.Div(
    children=[
        jumbotron,

        dbc.Container(
            [dbc.Row([dbc.Col(imag,className='col-4',align="left"),
                      dbc.Col(deployment,className='col-8',align="right"),
                      ],align="center",justify='center',
                     style={'margin-left': 2, 'margin-right': 2}, className="h-95",
                     ),
             ],
            fluid=True, style={"height": "65vh"}
        ),
        # html.Br(),

        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        container, width=12
                    ), align="center", justify='center',
                    style={'margin-left': 2, 'margin-right': 2}),
                dbc.Row(
                    [
                        dbc.Col(track,
                                className='col-7'),
                        dbc.Col(vel,
                                className='col-5'),
                    ], className="h-80", align="center", justify='bottom',
                    style={'margin-left': 2, 'margin-right': 2}
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(track_caption,
                                className='col-7'),
                        dbc.Col(vel_caption,
                                className='col-5'),
                    ], align="center", justify='top',
                    style={'margin-left': 2, 'margin-right': 2}
                ),
            ],
            fluid=True, style={"height": "90vh"}
        ),

        dbc.Container([
# dbc.Row(
#                     dbc.Col(dbc.FormGroup([dbc.Label("Choose a Parameter to show"), dropdown2]))
#                 ),
            dbc.Row(
                    dbc.Col(
                        choose_param, width=12
                    ), align="center", justify='center',
                    style={'margin-left': 2, 'margin-right': 2}),

            dbc.Row(
                [
                    dbc.Col(ts,
                            className='col-7'),
                    dbc.Col(
                        p3d,
                        className='col-5'
                    ),
                ], align="top", justify='center',
                style={'margin-left': 2, 'margin-right': 2}
            ),
            html.Br()
        ],
            fluid=True, style={"height": "130vh"}
        ),

        aboutme

    ]

)


@app.callback(
    [Output(component_id='glider_map', component_property='figure'),
     Output(component_id='map_tc', component_property='figure'),
     Output(component_id='time_series', component_property='figure')],
    [Input(component_id='slct_deployment', component_property='value')]
)
def update_graph(option_slctd):
    current = pd.read_csv("data/" + option_slctd + "_current_tc.csv", parse_dates=['time'])

    fig1 = px.scatter_mapbox(current, lat="lat", lon="lon", hover_name="time",
                             zoom=7, center={"lat": 35.3, "lon": -75.4},
                             )

    fig1.update_layout(
        mapbox_style="white-bg",
        margin=dict(l=20, r=20, t=20, b=20),
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig2 = px.scatter(current,
                      x="xr",
                      y="yr",
                      hover_name="time",
                      hover_data=[])
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20),)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=pd.to_datetime(current['time']), y=current['u'],
                              mode='lines',
                              name='u'))
    fig3.add_trace(go.Scatter(x=pd.to_datetime(current['time']), y=current['v'],
                              mode='lines',
                              name='v'))
    fig3.update_layout(xaxis_title='Time',
                       yaxis_title='Velocity (m/s)',
                       margin=dict(l=20, r=20, t=20, b=20),
                       )

    return fig1, fig2, fig3


@app.callback(
    Output(component_id='3d_map', component_property='figure'),
    [Input(component_id='slct_deployment', component_property='value'),
     Input(component_id='slct_parameter', component_property='value')]
)
def update_map(option_slctd, parameter):
    ctd = pd.read_csv("data/" + option_slctd + "_ctd_tc.csv",
                      skiprows=lambda x: (x != 0) and x % 10)
    fig5 = make_subplots(rows=2, cols=1, specs=[[{'type': 'scatter3d'},],
               [{'type': 'scatter3d'},]])

    fig5.add_trace(
        go.Scatter3d(
            x=ctd['lon'],
            y=ctd['lat'],
            z=-ctd['depth'],
            mode='markers',
            marker=dict(
                size=3,
                color=ctd[parameter],
                colorscale=cm[parameter],
                line_width=None,
                showscale=True
            ),
        ),
        row = 1, col=1
    )
    fig5.update_layout(
        # autosize=False,
        # height=550,
        showlegend=False
    )

    fig5.add_trace(
        go.Scatter3d(
            x=ctd['xr'],
            y=ctd['yr'],
            z=-ctd['depth'],
            mode='markers',
            marker=dict(
                size=3,
                color=ctd[parameter],
                colorscale=cm[parameter],
                line_width=None,
                showscale=True
            ),
        ),
        row = 2, col=1
    )
    fig5.update_layout(
        # autosize=False,
        # height=550,
        margin=dict(l=10, r=20, t=10, b=20),
        showlegend=False
    )
    return fig5


@app.callback(
    Output(component_id='ctd', component_property='figure'),
    [Input(component_id='slct_deployment', component_property='value')]
)
def update_plot(option_slctd):
    ctd = pd.read_csv("data/" + option_slctd + "_ctd_tc.csv", usecols=["time", "t", "s", "dens", "chl", "depth"],
                      parse_dates=['time'], infer_datetime_format=True, skiprows=lambda x: (x != 0) and x % 10)

    chl_range = np.percentile(ctd["chl"][np.isfinite(ctd['chl'])], [5, 95], axis=0)

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.01)
    fig.add_trace(
        go.Scattergl(
            x=ctd["time"],
            y=ctd["depth"],
            mode='markers',
            marker=dict(
                color=ctd['t'],
                colorscale='thermal',
                line_width=None,
                showscale=True,
                colorbar=dict(len=0.25, y=0.88),
            ),
            name="Temperature"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=ctd["time"],
            y=ctd["depth"],
            mode='markers',
            marker=dict(
                color=ctd['s'],
                colorscale='haline',
                line_width=None,
                showscale=True,
                colorbar=dict(len=0.25, y=0.625),
            ),
            name="Salinity"
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=ctd["time"],
            y=ctd["depth"],
            mode='markers',
            marker=dict(
                color=ctd['dens'],
                colorscale='dense',
                line_width=None,
                showscale=True,
                colorbar=dict(len=0.25, y=0.37),
            ),
            name="Density"
        ),
        row=3, col=1
    )
    fig.add_trace(
        go.Scattergl(
            x=ctd["time"],
            y=ctd["depth"],
            mode='markers',
            marker=dict(
                color=ctd['chl'],
                colorscale='algae',
                line_width=None,
                cmin=chl_range[0],
                cmax=chl_range[-1],
                showscale=True,
                colorbar=dict(len=0.25, y=0.115),
            ),
            name="Chlorophyll"
        ),
        row=4, col=1
    )
    fig.update_layout(
        # title='Parameters as time series',
        # autosize=False,
        # height=1200,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    fig.update_yaxes(autorange="reversed")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
