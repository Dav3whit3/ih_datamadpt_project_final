import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
from Functions import API_data_extraction as aq
from datetime import date

summoner = 'Saikki kusuo'
key = 'RGAPI-9724b32a-f354-408c-8cde-8fdcc35e01fa'

summoner_info = aq.get_summoner_info(summoner, key)
accountid = summoner_info['accountId'][0]
champions = aq.championsid(key)
queues = aq.get_queuesid(key)
match_list = aq.get_matchlist(accountid, key, champions, queues)
match_info = aq.get_match_info(4884450178, key)
players_info = aq.get_players_info(match_info)
timeline = aq.get_match_timeline(4884450178, key)
frames = aq.participant_frames(timeline, players_info)
events = aq.get_events(timeline, players_info)
golddiff = aq.gold_diff(frames)
players_stats = aq.player_stats_table(frames, champions)


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


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Live game data (In Development)",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Match history data",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        ###### What is this mock app about?
                        This is a dashboard for monitoring real-time process quality along manufacture production line.
                        """

                            )
                        ),
                    ),
                ],
            )
        ),
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
                        id="summoner_name",
                        placeholder="Select summoner name",
                        type='text',
                        value="",
                        size="15",
                        style={"width": "100%", "margin-top": "10px"}
                    ),
                    html.Button('Submit',
                                id='submit-val',
                                style={"text-align": "center",
                                       "margin-bottom": "10px",
                                       "color": "#ffffff",
                                       "margin-top": "10px",
                                       "margin-left": "20%",
                                       "margin-right": "20%"}),

                ],
            ),
            html.Div(
                style={"width": "100%",
                       "display": "inline-block",
                       "text-align": "center"},
                children=[
                    dcc.Loading(children=html.Div(id="user_info_container")),
                    html.Div(
                        style={"width": "100%",
                               "display": "inline-block",
                               "text-align": "center",
                               "margin-top": "30px"},
                        children=[
                            dcc.DatePickerSingle(
                                id='my-date-picker-single',
                                min_date_allowed=match_list['Date2'].min(),
                                max_date_allowed=match_list['Date2'].max(),
                                initial_visible_month=date.today(),
                                clearable=False,
                                day_size=50,
                                placeholder="Select a date",
                                display_format='M-D-Y',
                                date=date.today(),
                                style={
                                    "width":"100%",
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
                                          "margin-top": "10px",
                                          "margin-left": "35%",
                                          "margin-right": "auto",
                                          }
                                   ),
                    dcc.Slider(
                        id="gauge-slider",
                        max=frames['timestamp'].max(),
                        min=frames['timestamp'].min(),
                        # step=None,
                        vertical=False,
                        disabled=False,
                        updatemode='drag'
                    ),
                    daq.Gauge(
                        id="progress-gauge",
                        max=frames['timestamp'].max(),
                        min=frames['timestamp'].min(),
                        units="Min",
                        label="Progress (mins)",
                        color="#27A73E",
                        size=100,
                        value=0,
                        showCurrentValue=True,  # default size 200 pixel

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
                                            "height": 30,
                                        },
                                        "style": {"padding" : "5px"}
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
                            children=["Stats ranking"]
                            ),
                   html.P("Score",
                           style={"text-align": "center"}),
                   html.Div(
                        id="Score",
                        style={"display": "inline-block",
                               "text-align": "center"},
                        children=[
                            daq.LEDDisplay(
                                id='red-team',
                                label="Red Team",
                                value=6,
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
                                value=6,
                                size=50,
                                style={"display": "inline-block",
                                       "margin-bottom": "20px"},
                                color="#2E86C1",
                                backgroundColor="rgba(0,0,0,0)"
                            )
                        ]
                   ),
                   html.P("Towers"),
                   html.Div(
                        id="towers",
                        style={"display": "inline-block",
                               "text-align": "center"},
                        children=[
                            daq.LEDDisplay(
                                id='red-team-towers',
                                label="Red Team",
                                value=6,
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
                                label="Blue Team",
                                value=6,
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
