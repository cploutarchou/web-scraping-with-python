import datetime
import logging
from operator import itemgetter

import graypy
from mongoengine import StringField, DateTimeField, Document, IntField, errors, connect, ListField

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
            host="mongodb://admin:admin@172.21.0.20:27017/webscrapper?authSource=admin&directConnection=true&ssl=false")
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
        posts = [post for post in q_set._iter_results()]
        data = posts
        client.__exit__()
        return data
    except errors.LookUpError as e:
        logger.error(f"Something went wrong. Error {e}")
        return data


def posts_perday():
    client.__enter__()
    pipeline = [
        {"$group":
             {"_id":
                  {"day": {"$dayOfMonth": "$created_at"},
                   "month": {"$month": "$created_at"},
                   "year": {"$year": "$created_at"}
                   },
              "count": {"$sum": 1},
              "date": {'$first': "$created_at"}
              }
         }, {
            "$project":
                {
                    "date":
                        {
                            "$dateToString": {"format": "%Y-%m-%d", "date": "$date"}
                        },
                    "count": 1,
                    "_id": 0
                }
        }
    ]
    data = Posts.objects().aggregate(pipeline=pipeline)
    final_data = []
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    for i in data:
        date_time_obj = datetime.datetime.strptime(i['date'], '%Y-%m-%d').date()
        if date_time_obj > week_ago:
            final_data.append({'date': i['date'], 'count': i['count']})
    client.__exit__()
    return final_data


def most_common():
    client.__enter__()
    pipeline = [
        {"$unwind": "$categories"},
        {"$group": {"_id": "$categories", "count": {"$sum": 1}}},
        {
            "$group": {
                "_id": "null",
                "counts": {
                    "$push": {
                        "k": "$_id",
                        "v": "$count"
                    }
                }
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {"$arrayToObject": "$counts"}
            }
        }
    ]
    final_data = []
    data = Posts.objects().aggregate(pipeline=pipeline)
    for i in data:
        for key, val in i.items():
            final_data.append({"tag": key, "count": val})
    client.__exit__()
    return final_data


def top_10_questions():
    client.__enter__()
    pipeline = [{"$sort": {"views": -1}}, {"$limit": 10}]
    final_data = []
    data = Posts.objects().aggregate(pipeline=pipeline)
    for v in data:
        final_data.append({'title': v['title'], 'count': v['views']})
    return final_data
