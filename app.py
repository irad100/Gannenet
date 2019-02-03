from threading import Thread

from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.figure_factory as ff
import plotly.plotly as plty
from dash.dependencies import Input, Output

from gannenet import Gannenet
import sys
from subprocess import check_output, call
import atexit
import argparse

df = []
thread_started = False
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]

app = dash.Dash('working-status-app', external_stylesheets=external_css)
server = app.server

app.layout = html.Div([
    html.Div([
        html.H2("Gannenet: Live Working Status"),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png")], className='banner'),
    html.Div([
        html.H3(id='live-update-text', className='Title'),
        html.Div([dcc.Graph(id='live-update-graph')]),
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)]),
], style={'padding': '0px 10px 15px 10px',
          'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
          'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'})


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    global thread_started
    global g
    if not g.isAlive() and not thread_started:
        thread_started = True
        g.start()
        print("Main Thread Started")
    elapsed_str = g.to_string()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span(elapsed_str, style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    start_working, end_working = g.get_working_session_times()

    work_status_bool = g.get_work_status()

    start_working_str = start_working.strftime("%Y-%m-%d %H:%M:%S")
    end_working_str = end_working.strftime("%Y-%m-%d %H:%M:%S")

    now_status = datetime.now()
    now_status_str = now_status.strftime("%Y-%m-%d %H:%M:%S")

    if work_status_bool:
        df.append(dict(Task="WorkStatus", Start=start_working_str,
                       Finish=now_status_str, Resource="Working"))
        df.append(dict(Task="WorkStatus", Start=end_working_str,
                       Finish=start_working_str, Resource="NotWorking"))
    else:
        df.append(dict(Task="WorkStatus", Start=start_working_str,
                       Finish=end_working_str, Resource="Working"))
        df.append(dict(Task="WorkStatus", Start=end_working_str,
                       Finish=now_status_str, Resource="NotWorking"))

    colors = dict(Working='rgb(100, 221, 23)',
                  NotWorking='rgb(213, 0, 0)')

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='',
                          show_colorbar=True, bar_width=0.1, showgrid_x=False, showgrid_y=False, group_tasks=True)

    fig['layout']['height'] = 450

    now_status = datetime.now()
    now_status_str = now_status.strftime("%Y-%m-%d %H:%M:%S")

    fig['layout']['yaxis'] = dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        fixedrange=False,
        showticklabels=False
    )
    fig['layout']['xaxis'] = dict(
        showgrid=False,
        showline=False,
        fixedrange=False,
        showticklabels=True,
        zeroline=False
    )

    fig['layout']['margin'] = {
        't': 10, 'l': 80, 'r': 50
    }
    fig['layout']['legend'] = {'x': 400, 'y': 600, 'xanchor': 'right'}

    fig['layout']['xaxis']['rangeselector'] = dict(
        buttons=[{'count': 7, 'label': '1w', 'step': 'day', 'stepmode': 'backward'},
                 {'count': 24, 'label': '1d', 'step': 'hour', 'stepmode': 'backward'},
                 {'count': 5, 'label': '5h', 'step': 'hour', 'stepmode': 'backward'},
                 {'count': 60, 'label': '1h',
                     'step': 'minute', 'stepmode': 'backward'},
                 {'count': 5, 'label': '5m', 'step': 'minute', 'stepmode': 'backward'}],
    )
    return fig


def __exit_handler(g):
    print("\n\n\n---     You pressed Ctrl+C!      ---")
    print("---   Have a Nice Day! Goodbye   ---")

    #fig = update_graph_live(1)
    #plty.plot(fig, filename='daily-schedule', fileopt='extend')

    g.stop()

if __name__ == "__main__":
    g = Gannenet()
    atexit.register(__exit_handler, g)
    app.run_server(debug=True)
