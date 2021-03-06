# -*- coding: utf-8 -*-
import json
import os
import sys
import pickle # convert dictionary or json into string that redis can process
from datetime import datetime
from bson.json_util import dumps
import redis

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client # pylint: disable=import-error, wrong-import-position
# import news_recommendation_service_client

from cloudAMQP_client import cloudAMQPClient

CLOUDAMQP_URL = "amqp://avqwoxul:DnLJdgb71xYI_2bNIC5myl9-6NF-Hsop@hornet.rmq.cloudamqp.com/avqwoxul"

TEST_QUEUE_NAME = 'test'

REDIS_HOST = "localhost"
REDIS_PORT = 6379

CLICK_LOGS_TABLE_NAME = "user_click_log"

NEWS_TABLE_NAME = "news"

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 100
USER_NEWS_TIME_OUT_IN_SECONDS = 60

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

amqp_client = cloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)
def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return json.loads(dumps(news))

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        total_news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digests = total_news_digests[begin_index:end_index]
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        # total_news = list(db[NEWS_TABLE_NAME])
        total_news_digests = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index: end_index]
        print sliced_news

     # Get preference for the user
    # preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    # topPreference = None
    #
    # if preference is not None and len(preference) > 0:
    #     topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth.
        del news['text']
        # if news['class'] == topPreference:
        #     news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}
    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    amqp_client.sendMessage(message)
