import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
from Layout import tab1 as t1
from Functions import API_data_extraction as aq


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

key = 'RGAPI-9724b32a-f354-408c-8cde-8fdcc35e01fa'
champions = aq.championsid(key)
queues = aq.get_queuesid(key)

app.layout = html.Div(
    id="big-app-container",
    children=[
        dcc.Store(id="summoner-name"),
        dcc.Store(id="account-id"),
        dcc.Store(id="match-list"),
        dcc.Store(id="game-id"),
        dcc.Store(id="match-info"),
        dcc.Store(id="players-info"),
        dcc.Store(id="timeline"),
        dcc.Store(id="frames"),
        dcc.Store(id="events"),
        dcc.Store(id="golddiff"),
        dcc.Store(id="players_stats_df"),
        t1.build_banner(),
        #dcc.Interval(id="interval-component", interval=2 * 1000,  n_intervals=50, disabled=True,),
        html.Div(
            id="app-container",
            children=[
                html.Div(id="app-content",
                         children=[
                             html.Div(
                                 id="status-container",
                                 children=[
                                     t1.build_quick_stats_panel(),
                                     html.Div(
                                         id="graphs-container",
                                         children=[t1.build_top_panel(), t1.build_chart_panel()],
                                     ),
                                 ],
                             ),
                         ]),
            ],
        ),
        #t1.generate_modal(),
    ],
)

# Store summoner name & acc ID callback --------------------------------------------------------------------------------
@app.callback(
    [Output("summoner-name", "data"),
     Output("account-id", "data")],
    [Input("submit-val", "n_clicks")],
    [State("summoner-name-input", "value")]
)
def store_summoner_name(n_clicks, value):
    summoner_info = aq.get_summoner_info(value, key)
    accid = summoner_info['accountId'][0]

    return value, accid


# Store full match list callback ---------------------------------------------------------------------------------------
@app.callback(
    Output("match-list", "data"),
    [Input("account-id", "data")]
)
def update_match_list(accid):
    match_list = aq.get_matchlist(accid, key, champions, queues)
    match_list = match_list.to_dict(orient='records')

    return match_list


# First-5 match list callback ------------------------------------------------------------------------------------------
@app.callback(
    Output("user_info_container", "children"),
    [Input("match-list", "data"),
     Input("my-date-picker-single", "date")
     ]
)
def update_user_info(matchlist, date):
    df = pd.DataFrame(matchlist)
    df = df[df['Date2'] == date.replace("-", "/")]
    df = df[['Date', 'queue', 'champion', 'role', 'gameId']]

    return dash_table.DataTable(
        id="first-five-match-list",
        columns=[{"name": c, "id": c} for c in df.columns],
        data=df.to_dict('records'),
        style_table={'height': '250px', 'overflowX': 'auto'},
        page_action='none',
        style_data={'color': '#ffffff'},
        style_filter={'color': '#ffffff'},
        row_selectable="single",
        selected_rows=[],
        page_size=5,

        style_cell={"background-color": "#242a3b",
                    "color": "#ffffff",
                    "textAlign": "center",
                    "height": "auto",
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                    },
        style_as_list_view=True,
        style_header={"background-color": "#1f2536",
                      "padding": "0px 5px"},
    )


# Date picker callback
@app.callback(
    [Output('my-date-picker-single', "max_date_allowed"),
     Output('my-date-picker-single', "min_date_allowed")],
    [Input("match-list", "data")]
)
def update_datepicker(matchlist):
    df = pd.DataFrame(matchlist)
    maximum = df['Date2'].max()
    minimum = df['Date2'].min()

    return maximum, minimum


# Store Game ID callback -----------------------------------------------------------------------------------------------
@app.callback(
    [Output('game-id', 'data'),
     Output("gauge-slider", "value")],
    [Input('first-five-match-list', 'data'),
     Input('first-five-match-list', 'selected_rows')])
def update_gameid(data, selected_rows):
    df = pd.DataFrame(data).iloc[selected_rows]
    gameid = df['gameId']

    return gameid, 0


# Store match info -----------------------------------------------------------------------------------------------------
@app.callback(
    Output("match-info", "data"),
    [Input("game-id", "data")]
)
def update_match_info(gameid):
    gameid = gameid[0]
    match_info = aq.get_match_info(gameid, key)

    return match_info


# Store Players info ---------------------------------------------------------------------------------------------------
@app.callback(
    Output("players-info", "data"),
    [Input("match-info", "data")]
)
def update_players_info(matchinfo):
    players_info = aq.get_players_info(matchinfo)
    players_info = players_info.to_dict(orient='records')

    return players_info


# Store match timeline -------------------------------------------------------------------------------------------------
@app.callback(
    Output("timeline", "data"),
    [Input("game-id", "data")]
)
def update_match_timeline(gameid):
    gameid = gameid[0]
    timeline = aq.get_match_timeline(gameid, key)

    return timeline


# Store match frames ---------------------------------------------------------------------------------------------------
@app.callback(
    Output("frames", "data"),
    [Input("timeline", "data"),
     Input("players-info", "data")]
)
def update_match_frames(timeline, players_info):
    players_info = pd.DataFrame(players_info)
    frames = aq.participant_frames(timeline, players_info)
    frames = frames.to_dict(orient='records')

    return frames


# Store match events ---------------------------------------------------------------------------------------------------
@app.callback(
    Output("events", "data"),
    [Input("timeline", "data"),
     Input("players-info", "data")]
)
def update_match_events(timeline, players_info):
    players_info = pd.DataFrame(players_info)
    events = aq.get_events(timeline, players_info)
    events = events.to_dict(orient='records')

    return events


# Store match gold diff table ------------------------------------------------------------------------------------------
@app.callback(
    Output("golddiff", "data"),
    [Input("frames", "data")]
)
def update_golddiff(frames):
    frames = pd.DataFrame(frames)
    golddiff = aq.gold_diff(frames)
    golddiff = golddiff.to_dict(orient='records')

    return golddiff


# Store player stats table ---------------------------------------------------------------------------------------------
@app.callback(
    Output("players_stats_df", "data"),
    [Input("frames", "data")]
)
def update_player_stats_table(frames):
    frames = pd.DataFrame(frames)
    players_stats = aq.player_stats_table(frames, champions)
    players_stats = players_stats.to_dict(orient='records')

    return players_stats


# Update gauge and slider values
@app.callback(
    [Output("gauge-slider", "max"),
     Output("gauge-slider", "min"),
     Output("game-progress", "max"),
     Output("game-progress", "min"),
     #Output("gauge-slider", "marks")
     ],
    [Input("frames", "data")]
)
def update_components_values(frames):
    df = pd.DataFrame(frames)
    maximum = df['timestamp'].max()
    minimum = df['timestamp'].min()
    marks = {value: f"{value}'" for value in df['timestamp'].unique()}

    return maximum, minimum, maximum, minimum, #marks


# Gauge callback--------------------------------------------------------------------------------------------------------
@app.callback(
    Output("game-progress", "value"),
    [Input("gauge-slider", "value")]
)
def update_gauge(value):
    return value


# Gold chart callback --------------------------------------------------------------------------------------------------
@app.callback(
    Output("gold-progress", "figure"),
    [Input("gauge-slider", "value"),
     Input("golddiff", "data")]
)
def update_gold_progress_chart(minute, golddiff):
    df = pd.DataFrame(golddiff)
    df = df[df['timestamp'] <= minute]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['team100golddiff'],
                             fill='tozeroy',
                             name='Blue team',
                             line={
                                 "color": "#2E86C1",
                                  },
                             mode="none"
                             )
                  )
    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['team200golddiff'],
                             fill='tozeroy',
                             name="Red team",
                             line={
                                 "color": "#E74C3C",
                                  },
                             mode="none"
                             )
                  )
    fig["layout"] = dict(
        margin=dict(t=40, r=40, autoexpand=True),
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
        font={"color": "darkgray"},
        showlegend=True,
        autosize=True,
        xaxis={
            "zeroline": False,
            "showgrid": False,
            "tick0": 0,
            "dtick": 1,
            "title": "Time (mins)",
            "showline": True,
            "mirror": True,
            "linecolor": 'black',
            "titlefont": {"color": "darkgray"},
            "autorange": True
        },
        yaxis={
            "title": "Gold",
            "showgrid": False,
            "showline": True,
            "mirror": True,
            "linecolor": 'black',
            "zeroline": True,
            "autorange": True,
            "titlefont": {"color": "darkgray"},

        },
        shapes=[
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 0,
                "y0": 1000,
                "x1": df['timestamp'].max(),
                "y1": 1000,
                "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 0,
                "y0": -1000,
                "x1": df['timestamp'].max(),
                "y1": -1000,
                "line": {"color": "#91dfd2", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 0,
                "y0": 3000,
                "x1": df['timestamp'].max(),
                "y1": 3000,
                "line": {"color": "#f4d44d", "width": 1, "dash": "dot"},
            },
            {
                "type": "line",
                "xref": "x",
                "yref": "y",
                "x0": 0,
                "y0": -3000,
                "x1": df['timestamp'].max(),
                "y1": -3000,
                "line": {"color": "#f4d44d", "width": 1, "dash": "dot"},
            },
        ]
    )

    return fig


# Player stats callback ------------------------------------------------------------------------------------------------
@app.callback(
    Output("player-stats", "figure"),
    [Input("gauge-slider", "value"),
     Input("players_stats_df", "data")]
)
def update_player_stats_table(minute, stats):

    df = pd.DataFrame(stats)
    df = df[df['timestamp'] == minute]
    df['teamId'] = df['teamId'].map({100: "Blue", 200: "Red"})
    df.rename(columns={'summonerName': 'Summoner',
                       'champion': 'Champion',
                       'level': 'Level',
                       'minionsKilled': 'Cs',
                       'totalGold': 'Gold',
                       'teamId': 'Team'
                       }, inplace=True)
    df.drop(['timestamp'], axis=1, inplace=True)
    df.sort_values(by=['Gold'], ascending=False, inplace=True)

    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns.to_list(),
                    align='center',
                    font=dict(color='white', size=18),
                    fill_color="rgba(0,0,0,0)"
                    ),

        cells=dict(values=[df[f'{col}'] for col in df.columns],
                   align='center',
                   font=dict(color='white', size=20),
                   fill_color="rgba(0,0,0,0)",
                   line_color="rgba(0,0,0,0)",
                   height=32,
                   ),
        columnwidth=[3, 2, 1, 1, 1]
                                )
                        ]
                    )
    fig["layout"] = dict(
        margin=dict(t=5, r=5, l=5, b=5, autoexpand=True),
        hovermode="closest",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "darkgray"},
        autosize=True,
                        )

    return fig


# Scores callback ------------------------------------------------------------------------------------------------------
@app.callback([
    Output("red-team", "value"),
    Output("blue-team", "value"),
    Output("red-team-towers", "value"),
    Output("blue-team-towers", "value")],
    [Input("gauge-slider", "value"),
     Input("events", "data")]
)
def update_score(minute, df):
    df = pd.DataFrame(df)
    df_kills = df[(df['timestamp'] <= minute) & (df['type'] == 'CHAMPION_KILL')]
    df_towers = df[(df['timestamp'] <= minute) & (df['type'] == 'BUILDING_KILL')]

    rt_kills = df_kills[df_kills['teamId_y'] == 200].count()['type']
    bt_kills = df_kills[df_kills['teamId_y'] == 100].count()['type']

    rt_towers = df_towers[df_towers['teamId_y'] == 200].count()['type']
    bt_towers = df_towers[df_towers['teamId_y'] == 100].count()['type']

    return rt_kills, bt_kills, rt_towers, bt_towers


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_ui=False) #port=8050)
