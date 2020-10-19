import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import webbrowser
from Functions import API_data_extraction as aq

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

summoner = 'Saikki kusuo'
key = 'RGAPI-9724b32a-f354-408c-8cde-8fdcc35e01fa'

summoner_info = aq.get_summoner_info(summoner, key)
accountid = summoner_info['accountId'][0]
match_list = aq.get_matchlist(accountid, key)
match_info = aq.get_match_info(4834424471, key)
players_info = aq.get_players_info(match_info)
timeline = aq.get_match_timeline(4834424471, key)
frames = aq.participant_frames(timeline)
events = aq.get_events(timeline)


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
                    html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
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
                        id="api_key",
                        placeholder="input api key",
                        type='text',
                        value="RGAPI-9724b32a-f354-408c-8cde-8fdcc35e01fa",
                        size="15",
                        style={"width": "100%"}
                    ),

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
                    html.Div(
                        style={"width": "100%", "display": "inline-block", "text-align": "center"},
                        children=[
                            dcc.Dropdown(
                                id="match-list",
                                options=[{'label': f'{match}', 'value': f'{match}'} for match in
                                         list(match_list['gameId'].head(10))],
                            )
                        ]
                    )
                ],
            ),
            html.Div(
                style={"width": "100%",
                       "display": "inline-block",
                       "text-align": "center"},
                children=[
                    dcc.Loading(children=html.Div(id="user_info_container")),
                ]
            ),
            html.Div(
                id="card-2",
                style={"display": "inline-block"},
                children=[
                    html.P("Match Timeline"),
                    daq.Gauge(
                        id="progress-gauge",
                        max=frames['timestamp'].max(),
                        min=frames['timestamp'].min(),
                        units="Min",
                        size=30,
                        value=275,
                        showCurrentValue=True,  # default size 200 pixel
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
                ],
            ),
            html.Div(
                id="utility-card",
                children=[

                    daq.StopButton(id="stop-button", size=160, n_clicks=0)],
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
                            # generate_metric_list_header(),
                            html.Div(
                                id="metric-rows",
                                children=[
                                    # generate_metric_row_helper(stopped_interval, 1),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Stats ranking"),
                    # generate_piechart(),
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
                id="control-chart-live",
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


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        # dcc.Interval(id="interval-component",interval=2 * 1000,  n_intervals=50, disabled=True,),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        # dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)


@app.callback(
    [Output("app-content", "children"),
     # Output("interval-component", "n_intervals")
     ],
    [Input("app-tabs", "value")],
    # [State("n-interval-stage", "data")]
)
def render_tab_content(tab_switch,
                       # interval_component
                       ):
    if tab_switch == "tab1":
        return [html.Div(
            id="set-specs-intro-container",
            className='twelve columns',
            children=html.P("Currently developing."))
        ]
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[build_top_panel(), build_chart_panel()],
                ),
            ],
        ),
        # interval_component
    )


@app.callback(
    Output("user_info_container", "children"),
    [Input("submit-val", "n_clicks")],
    [State("api_key", "value"),
     State("summoner_name", "value")]
)
def update_user_info(n_clicks, input1, input2):
    return dash_table.DataTable(
        columns=[{"name": "apikey", "id": "api_key"}, {"name": "summoner name", "id": "summoner_name"}],
        data=[{}],
        style_table={'overflowX': 'auto'},
        filter_action="native",
        page_size=5,
        style_cell={"background-color": "#242a3b", "color": "#ffffff", "textAlign": "left"},
        style_as_list_view=False,
        style_header={"background-color": "#1f2536", "padding": "0px 5px"},
    )


@app.callback(
    Output("progress-gauge", "value"),
    [Input("gauge-slider", "value")]
)
def update_gauge(value):
    return value


# Running the server
if __name__ == "__main__":
    # launch = webbrowser.open_new_tab('http://127.0.0.1:8050/')
    app.run_server(debug=True, port=8050)
