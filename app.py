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


app.layout = html.Div(
    id="big-app-container",
    children=[
        t1.build_banner(),
        # dcc.Interval(id="interval-component",interval=2 * 1000,  n_intervals=50, disabled=True,),
        html.Div(
            id="app-container",
            children=[
                t1.build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        # dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
        t1.generate_modal(),
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
                t1.build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[t1.build_top_panel(), t1.build_chart_panel()],
                ),
            ],
        ),
        # interval_component
    )


@app.callback(
    Output("user_info_container", "children"),
    [Input("submit-val", "n_clicks")],
    [State("summoner_name", "value")]
)
def update_user_info(n_clicks, input1):
    df = t1.match_list.copy()
    df = df.head(5)[['Date', 'role', 'champion']]

    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_data={'color': '#ffffff'},
        style_filter={'color': '#ffffff'},
        row_selectable="single",
        page_size=5,
        style_cell={"background-color": "#242a3b",
                    "color": "#ffffff",
                    "textAlign": "center"},
        style_as_list_view=True,
        style_header={"background-color": "#1f2536",
                      "padding": "0px 5px"},
    )


@app.callback(
    Output("progress-gauge", "value"),
    [Input("gauge-slider", "value")]
)
def update_gauge(value):
    return value


@app.callback(
    Output("gold-progress", "figure"),
    [Input("gauge-slider", "value")]
)
def update_gold_progress_chart(value):
    df = t1.golddiff.copy()
    df = df[df['timestamp'] <= value]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['team100golddiff'],
                             fill='tozeroy',
                             name='Blue team',
                             line_color='#2E86C1',
                             #mode='none'
                             )
                  )

    fig.add_trace(go.Scatter(x=df['timestamp'],
                             y=df['team200golddiff'],
                             fill='tozeroy',
                             name="Red team",
                             line_color='#E74C3C',
                             #mode='none'
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
            "showgrid": True,
            "nticks": 5,
            "title": "Time (mins)",
            "showline": False,
            "titlefont": {"color": "darkgray"},
            "autorange": True
        },
        yaxis={
            "title": "Gold",
            "showgrid": False,
            "showline": False,
            "zeroline": True,
            "autorange": True,
            "titlefont": {"color": "darkgray"},
        })

    return fig


@app.callback(
    Output("player-stats", "figure"),
    [Input("gauge-slider", "value")]
)
def update_player_stats_table(minute):
    df = t1.players_stats
    df = df[df['timestamp'] == minute]
    df.rename(columns={'summonerName': 'Summoner',
                       'champion': 'Champion',
                       'level': 'Level',
                       'minionsKilled': 'Cs',
                       'totalGold': 'Gold'
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
                   height= 30,
                    ),
        columnwidth=[3,2,1,1,1]
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


# Running the server
if __name__ == "__main__":
    # launch = webbrowser.open_new_tab('http://127.0.0.1:8050/')
    app.run_server(debug=True, port=8050)
