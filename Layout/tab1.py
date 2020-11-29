import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
from datetime import date


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("League of Legends Dashboard"),
                    html.H6("In-game data analysis"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", ),
                ],
            ),
        ],
    )


def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        style={"padding-top": "0"},
        className="row",
        children=[
            html.Div(
                id="card-1",
                style={"display": "inline-block",
                       "text-align": "center",
                       "margin-bottom": "10px"},
                children=[
                    html.P("User info"),

                    dcc.Input(
                        id="summoner-name-input",
                        placeholder="Select summoner name",
                        type='text',
                        value="",
                        size="15",
                        style={"width": "100%", "margin-top": "10px"}
                    ),
                    html.Button('Search player',
                                id='submit-val',
                                style={"text-align": "center",
                                       "margin-bottom": "10px",
                                       "color": "#ffffff",
                                       "margin-top": "30px",
                                       "margin-left": "20%",
                                       "margin-right": "20%"}),

                ],
            ),
            html.Div(
                style={"width": "100%",
                       "display": "inline-block",
                       "text-align": "center"},
                children=[
                    html.P("Pick one of the recent games"),
                    dcc.Loading(children=html.Div(id="user_info_container")),
                    html.Div(
                        style={"width": "100%",
                               "display": "inline-block",
                               "text-align": "center",
                               "margin-top": "30px"},
                        children=[
                            html.P("or searh games by date"),
                            dcc.DatePickerSingle(
                                id='my-date-picker-single',
                                initial_visible_month=date.today(),
                                clearable=False,
                                day_size=50,
                                placeholder="Select a date",
                                display_format='Y/M/D',
                                date=date.today(),
                                style={
                                    "width": "100%",
                                }
                            ),
                        ]
                    )
                    ,
                ]
            ),
            html.Div(
                id="card-2",
                style={"display": "inline-block",
                       "text-align": "center",
                       "margin-bottom": "10px",
                       "margin-top": "25px"},
                children=[
                    html.P("Match Timeline"),
                    daq.StopButton(id="stop-button",
                                   size=160,
                                   n_clicks=0,
                                   style={"text-align": "center",
                                          "margin-bottom": "20px",
                                          "color": "#ffffff",
                                          "margin-top": "0px",
                                          "margin-left": "30%",
                                          "margin-right": "auto",
                                          }
                                   ),
                    dcc.Slider(
                        id="gauge-slider",
                        vertical=False,
                        disabled=False,
                        updatemode='drag',
                        step=1,

                    ),
                    daq.GraduatedBar(
                        id='game-progress',
                        label="Game progress",
                        value=0,
                        min=0,
                        max=10,
                        color={
                            "gradient": True,
                            "ranges": {
                                "green": [0, 100],
                            }
                        }
                    ),
                ],
            ),
        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def build_top_panel():
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Players stats"),
                    html.Div(
                        id="metric-div",
                        children=[
                            dcc.Graph(
                                id="player-stats",
                                figure=go.Figure(
                                    {
                                        "layout": {
                                            "paper_bgcolor": "rgba(0,0,0,0)",
                                            "plot_bgcolor": "rgba(0,0,0,0)",
                                            "xaxis": {
                                                'showgrid': False,
                                                "zeroline": False,
                                            },
                                            "yaxis": {
                                                'showgrid': False,
                                                "zeroline": False,
                                            }
                                        },
                                        "style": {"padding": "5px"}
                                    }
                                ),
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="stats-ranking",
                className="four columns",
                style={"display": "inline",
                       "text-align": "center"},
                children=[
                   html.Div(className="section-banner",
                            children=["Game progress"]
                            ),
                   html.P("Score",
                           style={"text-align": "center",
                                  "font-size": "50px"}),
                   html.Div(
                        id="Score",
                        style={"display": "inline-block",
                               "text-align": "center"},
                        children=[
                            daq.LEDDisplay(
                                id='red-team',
                                label="Red Team",
                                value=0,
                                size=50,
                                style={"display": "inline-block",
                                       "paper_bgcolor": "rgba(0,0,0,0)",
                                       "plot_bgcolor": "rgba(0,0,0,0)",
                                       "margin-right": "20px"},
                                color="#E74C3C",
                                backgroundColor="rgba(0,0,0,0)"
                            ),
                            daq.LEDDisplay(
                                id='blue-team',
                                label="Blue Team",
                                value=0,
                                size=50,
                                style={"display": "inline-block",
                                       "margin-bottom": "20px"},
                                color="#2E86C1",
                                backgroundColor="rgba(0,0,0,0)"
                            )
                        ]
                   ),
                   html.P("Towers",
                          style={"font-size": "20px"}
                          ),
                   html.Div(
                        id="towers",
                        style={"display": "inline-block",
                               "text-align": "center"},
                        children=[
                            daq.LEDDisplay(
                                id='red-team-towers',
                                value=0,
                                size=20,
                                style={"display": "inline-block",
                                       "paper_bgcolor": "rgba(0,0,0,0)",
                                       "plot_bgcolor": "rgba(0,0,0,0)",
                                       "margin-right": "20px"},
                                color="white",
                                backgroundColor="rgba(0,0,0,0)"
                            ),
                            daq.LEDDisplay(
                                id='blue-team-towers',
                                value=0,
                                size=20,
                                style={"display": "inline-block"},
                                color="white",
                                backgroundColor="rgba(0,0,0,0)"
                            )
                        ]
                   ),
                ],
            ),
        ],
    )


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Gold progress"),
            dcc.Graph(
                id="gold-progress",
                figure=go.Figure(
                    {
                        "data": [
                            {
                                "x": [],
                                "y": [],
                                "mode": "lines+markers",
                                "name": 'Hola',
                            }
                        ],
                        "layout": {
                            "paper_bgcolor": "rgba(0,0,0,0)",
                            "plot_bgcolor": "rgba(0,0,0,0)",
                            "xaxis": dict(
                                showline=False, showgrid=False, zeroline=False
                            ),
                            "yaxis": dict(
                                showgrid=False, showline=False, zeroline=False
                            ),
                            "autosize": True,
                        },
                    }
                ),
            ),
        ],
    )
