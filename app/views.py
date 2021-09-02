import json
import subprocess
import flask
import pandas as pd
import plotly
import app.models as models
import plotly.express as px
from flask import render_template, request

from .main import app
from .common import get_logger

logger = get_logger()


@app.route('/update_data', methods=['POST'])
def update_data():
    if request.method == 'POST' and request.form.get('update_data', None) is not False:
        print("test 12")
        result = subprocess.check_output("python scraper.py", shell=True)
        print(result)


@app.route('/')
def index():
    context = {
        "title": "Hexatone - Tables",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }
    res = models.get_all_data()

    context['table'] = res

    return render_template('index.html', data=context)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    context = {
        "title": "Hexatone",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }
    graphJSON = week_posts()

    return render_template('charts.html', graphJSON=graphJSON, context=context)


@app.errorhandler(code_or_exception=404)
def html_error(e):
    # defining function
    context = {
        "title": "Hexatone - ERROR 404 ",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }
    return render_template("error.html", error=e, context=context)


def week_posts():
    models.posts_perday()
    import plotly.express as px
    df = pd.DataFrame(models.posts_perday()).sort_values(by='date', ascending=True)
    fig = px.line(df, x='date', y="count", labels={
        "date": "Post date",
        "count": "Number of questions",
    })
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
