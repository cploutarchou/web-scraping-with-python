import json
import time

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import logging
import graypy
import pandas as pd
from mongoengine import StringField, DateTimeField, Document, IntField, errors, connect, ListField
import plotly.graph_objects as go
import plotly.express as px

"""
   Setup the logger
   """
logger = logging.getLogger('Stackoverflow Scraper')
logger.setLevel(logging.INFO)

handler = graypy.GELFTCPHandler('172.21.0.35', 12201)
logger.addHandler(handler)


class Connection:
    def __enter__(self):
        self.conn = connect(
            host="mongodb://admin:admin@172.21.0.20:27017/hexatone?authSource=admin&directConnection=true&ssl=false")
        return self.conn

    def __exit__(self):
        self.conn.close()


client = Connection()


class Posts(Document):
    created_at = DateTimeField(required=True, index=True)
    post_id = IntField(required=True, index=True)
    votes = StringField(required=True, index=True)
    answers = IntField(required=True, index=True)
    views = IntField(required=True, index=True)
    title = StringField(required=True, index=True)
    url = StringField(required=True, index=True)
    user = StringField(required=True, index=True)
    content = StringField(required=True, index=True)
    categories = ListField(required=True, index=True)
    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": [
            "created_at",
            "post_id",
            "votes",
            "answers",
            "views",
            "user",
            "categories"
        ]
    }


def insert_entry(data: dict, ):
    required_fields = ['post_id', 'title', 'user', 'created_at', 'votes', 'answers', 'views', 'url', 'content',
                       'categories']
    res = True
    if all(i.lower() in required_fields for i in data.keys()):
        if check_if_post_exist(int(data['post_id'])) is False:
            try:
                Posts(
                    post_id=data['post_id'], title=data['title'],
                    user=data['user'], created_at=data['created_at'],
                    votes=data['votes'], answers=data['answers'],
                    views=data['views'], url=data['url'], content=data['content'], categories=data['categories']
                ).save()
            except errors.SaveConditionError as e:
                res = None
                logger.error(f"Unable to save entry to db . Error {e.__str__()}")
        else:
            res = False
            logger.info(f"Post id {data['post_id']} already exist to database.")
    else:
        res = None
        logger.info("No Valid data required_fields is missing.")
    return res


def check_if_post_exist(post_id: int = None):
    """

    Get Audio file details.

    Args:
        post_id (str): The file object ID.

    Raises:
        ValidationError:  if file id is not valid or if object id not found in database.

    Returns:
        dict : A dictionary with object data
    """
    res = None
    client.__enter__()
    return_results = False
    if post_id and post_id is not None:
        res = Posts.objects(post_id=post_id)
        if res and len(res) > 0:
            return_results = True
        else:
            return_results = False
    else:
        error = f"post id is not valid.  Value : {post_id}"
        logger.error(error)
    client.__exit__()
    return return_results


def get_all_data():
    data = False
    try:
        client.__enter__()
        q_set = Posts.objects().as_pymongo()
        posts = [user for user in q_set._iter_results()]
        client.__exit__()
        data = posts
        return data
    except errors.LookUpError as e:
        logger.error(f"Something went wrong. Error {e}")
        return data


def posts_perday(weeks_number=1):
    data = get_all_data()

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    df1 = df.groupby(['date']).count()
    print(df1)
    # df['id'] = df.index
    # df.index.name = "id"
    # colors = px.colors.qualitative.Plotly
    #
    # fig = go.Figure()
    # app = Dash('DailyGrowth')
    #
    # trace1 = go.Bar(x=df["id"], y=df['daily new cases'], name='New cases')
    # trace2 = go.Bar(x=df["id"], y=df['daily tests performed'], name='Test performed')
    # trace3 = go.Bar(x=df["id"], y=df['daily deaths'], name='Deaths')
    #
    # app.layout = html.Div(children=[
    #     dcc.Graph(
    #         id='DailyGrowth_graph',
    #         figure={
    #             'data': [trace1, trace2, trace3],
    #             'layout':
    #                 go.Layout(barmode='stack')
    #         },
    #     )
    # ])
