import json
import subprocess
import os
import flask
import pandas as pd
import plotly
import app.models as models
import plotly.express as px
from flask import render_template, request, session, url_for, send_from_directory, flash
from mongoengine.errors import ValidationError, SaveConditionError
from .main import app
from .common import get_logger

logger = get_logger()


@app.route('/update_data', methods=['POST'])
def update_data():
    if request.method == 'POST' and request.form.get('update_data', None) is not False:
        print("test 12")
        result = subprocess.check_output("python scraper.py", shell=True)
        print(result)


@app.route('/find/<_id>', methods=['GET'])
def find(_id=None):
    try:
        data = models.get_upload_details(_id)
    except Exception as e:
        return flask.Response(status=404, response=json.dumps(str(e)))
    return flask.Response(status=200, response=json.dumps(data))


@app.route('/file/<_id>', methods=['GET'])
def get_file(_id):
    try:
        data = models.get_file(_id)
    except Exception as e:
        return flask.Response(status=404, response=json.dumps(str(e)))
    return flask.Response(status=200, response=json.dumps(data))


@app.route('/top_10', methods=['GET'])
def top_10():
    return models.get_top_10()


@app.route('/avg', methods=['GET'])
def avg():
    return models.get_average_file_size()


@app.route('/last_7_days_upload', methods=['GET'])
def last_7_days_upload():
    return models.last_7_days_upload()


@app.route('/')
def index():
    context = {
        "title": "AudioServer",
        "my_url": "https://christosploutarchou.com",
        "copyright": f"© 2021 All rights reserved.",

    }
    res = models.get_all_data()

    context['table'] = res

    return render_template('index.html', data=context)


@app.route('/tables')
def tables():
    models.posts_perday()
    context = {
        "title": "AudioServer",
        "my_url": "https://christosploutarchou.com",
        "copyright": f"© 2021 All rights reserved.",

    }
    res = models.get_all_data()

    context['table'] = res

    return render_template('index.html', data=context)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    context = {
        "title": "AudioServer",
        "my_url": "https://christosploutarchou.com",
        "copyright": f"© 2021 All rights reserved.",

    }
    res = models.get_all_data()

    context['table'] = res

    return render_template('charts.html', data=context)


@app.route("/stats")
def stats():
    available_objects = models.Files.objects().count()
    if available_objects > 0:
        context = {"top_10": models.get_top_10(),
                   "title": "AudioServer",
                   "average_file_size": avg()['AverageValue'],
                   "total_files": available_objects,
                   "total_size": models.convert_size(models.Files.objects.sum('file_size')),
                   "nodata": False
                   }
        data = last_7_days_upload()
        df = pd.DataFrame(data['data'])
        fig = px.bar(df, x='date', y='items', barmode='stack',
                     hover_data=['date', 'items'], color='date',
                     labels={'pop': 'population of Canada'}, height=350)

        fig.update_layout(barmode='stack')
        fig.update_xaxes(categoryorder='category ascending')
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        header = "Weekly Uploads"
        description = """
    
            """
        return render_template('stats.html', data=context, graphJSON=graph_json, header=header, description=description)
    else:
        return render_template('stats.html', data={"nodata": True, "title": "AudioServer", })


@app.errorhandler(code_or_exception=404)
def html_error(e):
    # defining function
    return render_template("error.html", error=e)


def week_posts():
    df = get_daily_data()
    df['id'] = df.index
    df.index.name = "id"
    colors = px.colors.qualitative.Plotly

    fig = go.Figure()
    app = DjangoDash('DailyGrowth')
    register = template.Library()
    trace1 = go.Bar(x=df["id"], y=df['daily new cases'], name='New cases')
    trace2 = go.Bar(x=df["id"], y=df['daily tests performed'], name='Test performed')
    trace3 = go.Bar(x=df["id"], y=df['daily deaths'], name='Deaths')

    app.layout = html.Div(children=[
        dcc.Graph(
            id='DailyGrowth_graph',
            figure={
                'data': [trace1, trace2, trace3],
                'layout':
                    go.Layout(barmode='stack')
            },
        )
    ])