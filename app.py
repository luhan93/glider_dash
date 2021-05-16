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
# app = dash.Dash(__name__)
# ====================================================================


df = pd.read_csv("data/glider_deployments.csv")
cm = {"t": "thermal",
      "s": "haline",
      "dens": "dense",
      "chl": "algae"}
jumbotron = dbc.Jumbotron(
    [
        html.H1("Glider Data Visualization", className="display-3"),
        html.P(
            "These glider deployments are part of PEACH field program.",
            className="lead",
        ),

        html.P(
            "Processes driving Exchanges At Cape Hatteras (PEACH)"
        ),
        # html.P(dbc.Button("Learn more", color="primary"), className="lead"),
    ],className="bg-primary text-white"
)
dropdown1 = dcc.Dropdown(
    id="slct_deployment",
    options=[{"label": df["glider"][i] + ' ' + df["Deployment #"][i],
              "value": df["glider"][i] + '_Deployment' + df["Deployment #"][i][-1]}
             for i in range(len(df))],
    multi=False,
    value='Ramses_Deployment1',
    clearable=False,
)

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


imag = dbc.Card(
    [
        dbc.CardImg(src="http://norgliders.gfi.uib.no/pict/glider4.gif"),
        dbc.CardImg(src="https://www.sequoiasci.com/wp-content/uploads/2016/10/Slocum-G2-from-Website.jpg"),
    ],
    color="primary", outline=True

)

# deployment = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
deployment = dbc.Card([
    dbc.CardHeader(html.H4("Glider Deployment Sheet"),className='bg-primary text-white'),
    dbc.CardBody(dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,),)
], color="primary", outline=True
)
track = dbc.Card(
    [
        dbc.CardHeader(
            html.H4("Glider Trajectory before and after coordinate transformation")
        ),
        dbc.CardBody(
            [
                html.P(
                    "On the left is the glider trajectory in the original map view. "
                    "On the right is the glider trajectory in transformed semi-Lagrangian Coordinate. "
                    "In this coordinate, the trajectory shows glider's movement relative to the water rather than the ground. ",

                ),
                dbc.Row(
                    [dbc.Col(dcc.Graph(id="glider_map"), width=6),
                     dbc.Col(dcc.Graph(id="map_tc"), width=6)]
                )
            ]
        )],
    color="primary", outline=True)
vel = dbc.Card(
    [
        dbc.CardHeader(
            html.H4(
                "Depth Averaged Water Velocity from Glider")
        ),
        dbc.CardBody(
            [
                html.P(
                    "Under the assumption of homogenous flow, we used the depth averaged water velocity "
                    "measured/computed by the glider to estimate the water movement."
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="time_series")
                            ],
                        )
                    ]
                )
            ]
        )
    ], color="primary", outline=True)

ts = dbc.Card(
    [
        dbc.CardHeader(
            html.H4(
                "Parameters Time Series")
        ),
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(id="ctd")
                        ]
                    )
                ]
            )
        )
    ], color="primary", outline=True
)
p3d = dbc.Card(
    [
        dbc.CardHeader(
            html.H4(
                "Show in 3D")
        ),
        dbc.CardBody(
            [
                dbc.Row(
                    dbc.Col(dbc.FormGroup([dbc.Label("Choose a Parameter to show"), dropdown2]))
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="3d_map")),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id="3d_tc"))
                    ]
                )
            ]
        )
    ], color="primary", outline=True
)
container = dbc.Card(
    [
        dbc.CardHeader(html.H4("Coordinate Transformation")),
        dbc.CardBody(
            dbc.FormGroup([dbc.Label("Select Glider Deployment"), dropdown1])
            # [
            #     dbc.Row(
            #         dbc.Col(dbc.FormGroup([dbc.Label("Select Glider Deployment"), dropdown1]))
            #     ),
            #
            #
            #     # dbc.Row(
            #     #     dbc.Col(dbc.FormGroup([dbc.Label("Choose a Parameter to show"), dropdown2]))
            #     # ),
            #     # dbc.Row(
            #     #     [
            #     #         dbc.Col(dcc.Graph(id="3d_map")),
            #     #     ]
            #     # ),
            #     # dbc.Row(
            #     #     [
            #     #         dbc.Col(dcc.Graph(id="3d_tc"))
            #     #     ]
            #     # )
            # ]
        )
    ]
)

app.layout = html.Div(
    children=[
        jumbotron,
        html.Div(className='row',
                 children=[
                     dbc.Container(
                         [dbc.Row([dbc.Col(imag,width=4), dbc.Col(deployment,width=8)],align="center",justify='center',
                                  style={'margin-left': 2, 'margin-right': 2} ),
                          html.Br(),
                          dbc.Row(
                              dbc.Col(
                                  container, width=12
                              ),align="center",justify='center',
                              style={'margin-left': 2, 'margin-right': 2} ),
                          html.Br(),
                          dbc.Row(
                              [
                                  dbc.Col(track,
                                          width=7),
                                  dbc.Col(
                                      vel,
                                      width = 5
                                  ),
                              ], className="h-30", align="center", justify='center',
                              style={'margin-left': 2, 'margin-right': 2}
                          ),
                          html.Br(),
                          dbc.Row(
                              [
                                  dbc.Col(ts,
                                          width=7),
                                  dbc.Col(
                                      p3d,
                                      width = 5
                                  ),
                              ], className="h-30", align="center", justify='center',
                              style={'margin-left': 2, 'margin-right': 2}
                          ),
                          # dbc.Row(
                          #     [
                          #         dbc.Col(ts,
                          #                 width=5),
                          #         dbc.Col(
                          #             vel,
                          #             width = 7
                          #         ),
                          #     ], className="h-30", align="center", justify='center',
                          #     style={'margin-left': 2, 'margin-right': 2}
                          # ),

                          ],
                         fluid=True,
                     ),

                     # dbc.Container(
                     #     # [
                     #         dbc.Row(
                     #             dbc.Col(
                     #                 container, width=11
                     #             ),align="center",justify='center',
                     #             style={'margin-left': 2,} ),
                     #     # ],
                     #     # dbc.Row([dbc.Col(imag,width=4), dbc.Col(deployment,width=8)],align="center",justify='center',
                     #     #         style={'margin-left': 2,'margin-right': 2}),
                     #     fluid=True,
                     # ),

                     # html.Div(
                     #          children=[
                     #
                     #              # dbc.Row(html.H6("Glider deployment sheet")),
                     #              # html.Div(className='row',
                     #              #         children=[
                     #              #            html.Div(className="six columns", style={'margin-left': 0},
                     #              #                      children=[
                     #              #                           deployment
                     #              #                      ]),
                     #              #             html.Div(className="three columns offset by six columns div-for-chart",
                     #              #                      children=[
                     #              #                           html.Img(src='https://www.whoi.edu/wp-content/uploads/2019/01/slocum_en_42909.jpg')
                     #              #                      ]),
                     #              #         ]),
                     #
                     #              dbc.Row(
                     #                  [
                     #                      dcc.Graph(id="time_series")
                     #                  ]
                     #              ),
                     #              # dbc.Row(
                     #              #     [
                     #              #         dcc.Graph(id="ctd")
                     #              #     ]
                     #              # )
                     #          ])
                 ])
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
    # fig.update_layout(mapbox_style="carto-positron")
    fig1.update_layout(
        mapbox_style="white-bg",
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
    # fig2.update_layout()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=pd.to_datetime(current['time']), y=current['u'],
                              mode='lines',
                              name='u'))
    fig3.add_trace(go.Scatter(x=pd.to_datetime(current['time']), y=current['v'],
                              mode='lines',
                              name='v'))
    fig3.update_layout(xaxis_title='Time',
                       yaxis_title='Velocity (m/s)',
                       height=475,)

    return fig1, fig2, fig3


@app.callback(
    [Output(component_id='3d_map', component_property='figure'),
     Output(component_id='3d_tc', component_property='figure')],
    [Input(component_id='slct_deployment', component_property='value'),
     Input(component_id='slct_parameter', component_property='value')]
)
def update_map(option_slctd, parameter):
    ctd = pd.read_csv("data/" + option_slctd + "_ctd_tc.csv",
                      skiprows=lambda x: (x != 0) and x % 10)
    fig5 = go.Figure()
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
        )
    )
    fig5.update_layout(
        autosize=False,
        height=550,
        showlegend=False
    )

    fig6 = go.Figure()
    fig6.add_trace(
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
        )
    )
    fig6.update_layout(
        autosize=False,
        height=550,
        showlegend=False
    )
    return fig5, fig6


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
        autosize=False,
        height=1200,
        showlegend=False
    )
    fig.update_yaxes(autorange="reversed")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
