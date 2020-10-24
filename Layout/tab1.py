import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
from Functions import API_data_extraction as aq


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
events = aq.get_events(timeline)
golddiff = aq.gold_diff(frames)


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
                        placeholder="input summoner name",
                        type='text',
                        value="Saikki kusuo",
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
                            dcc.Dropdown(
                                id="match-list",
                                placeholder="Select a match",
                                options=[{'label': f'{match}', 'value': f'{match}'} for match in
                                         list(match_list['gameId'].head(10))],
                            )
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
                                          "margin-bottom": "10px",
                                          "color": "#ffffff",
                                          "margin-top": "10px",
                                          "margin-left": "35%",
                                          "margin-right": "auto"}
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
                        color={"gradient": True, "ranges":{"green":[0,10],"yellow":[10,20],"red":[20,40]}},
                        size=30,
                        value=5,
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
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Players stats"),
                    html.Div(
                        id="metric-div",
                        children=[
                            #generate_metric_list_header(),
                            dcc.Loading(children=html.Div(id="player-stats"))
                            #html.Div(
                            #    id="metric-rows",
                            #   children=[
                                    # generate_metric_row_helper(stopped_interval, 1),
                            #    ],
                            #),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="stats-ranking",
                className="four columns",
                style={"display": "block"},
                children=[
                   html.Div(className="section-banner",
                            children=["Stats ranking",
                                      ]
                            ),
                   dcc.Dropdown(
                        # style={"width": "40%"}
                    )
                ],
            ),
        ],
    )


def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        #className="twelve columns",
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


def generate_metric_list_header():
    return generate_metric_row(
        "metric_header",
        {"height": "3rem", "margin": "1rem 0", "textAlign": "center"},
        {"id": "m_header_1", "children": html.Div("Player")},
        {"id": "m_header_2", "children": html.Div("Champion")},
        {"id": "m_header_3", "children": html.Div("Level")},
        {"id": "m_header_4", "children": html.Div("Cs")},
        {"id": "m_header_5", "children": html.Div("Gold")},
        {"id": "m_header_6", "children": "Pass/Fail"},
    )


def generate_metric_row(id, style, col1, col2, col3, col4, col5, col6):
    if style is None:
        style = {"height": "8rem", "width": "100%"}

    return html.Div(
        id=id,
        className="row metric-row",
        style=style,
        children=[
            html.Div(
                id=col1["id"],
                className="one column",
                style={"margin-right": "2.5rem", "minWidth": "50px"},
                children=col1["children"],
            ),
            html.Div(
                id=col2["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col2["children"],
            ),
            html.Div(
                id=col3["id"],
                style={"textAlign": "center"},
                className="one column",
                children=col3["children"],
            ),
            html.Div(
                id=col4["id"],
                style={"height": "100%"},
                className="three columns",
                children=col4["children"],
            ),
            html.Div(
                id=col5["id"],
                style={"display": "flex", "justifyContent": "center"},
                className="one column",
                children=col5["children"],
            ),
            html.Div(
                id=col6["id"],
                style={"height": "100%"},
                className="four columns",
                children=col6["children"],
            ),
        ],
    )