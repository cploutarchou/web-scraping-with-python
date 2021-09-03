import json
import pandas as pd
import plotly
import app.models as models
from flask import render_template
import plotly.graph_objects as go
from .main import app
from .common import get_logger
import plotly.express as px

logger = get_logger()


@app.route('/')
def index():
    context = {
        "title": "Web scrapper - Tables",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }
    res = models.get_all_data()

    context['table'] = res

    return render_template('index.html', data=context)


@app.route('/charts', methods=['GET', 'POST'])
def charts():
    top_10_post()
    context = {
        "title": "Web scrapper",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }

    graph_json = week_posts()
    graph_tag = get_popular_tags()
    top_10 = top_10_post()

    return render_template('charts.html', graph_json=graph_json, graph_tag=graph_tag, top_10=top_10, context=context)


@app.errorhandler(code_or_exception=404)
def html_error(e):
    # defining function
    context = {
        "title": "Web scrapper - ERROR 404 ",
        "my_url": "https://christosploutarchou.com",
        "author": "Christos Ploutarchou",
        "copyright": f"© 2021 All rights reserved.",

    }
    return render_template("error.html", error=e, context=context)


def week_posts():
    models.posts_perday()

    df = pd.DataFrame(models.posts_perday()).sort_values(by='date', ascending=True)
    fig = px.line(df, x='date', y="count", labels={
        "date": "Post date",
        "count": "Number of questions",
    })
    week_posts_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return week_posts_json


def get_popular_tags():
    tag = models.most_common()
    df = pd.DataFrame(tag)
    df = df.nlargest(10, 'count')
    fig = px.pie(df, values='count', names='tag', labels={
        "tag": "Category Name",
        "count": "Number of questions",
    })
    get_popular_tags_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return get_popular_tags_json


def top_10_post():
    posts = models.top_10_questions()
    posts_df = pd.DataFrame(posts).sort_values('count', ascending=True)
    fig = go.Figure(go.Bar(
        x=posts_df['count'],
        y=posts_df['title'],
        orientation='h'))

    top_10_post_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return top_10_post_json
