# -*- coding: utf-8 -*-
import news_classes
from datetime import datetime
import os
import sys
import click_log_processor
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import cloudAMQPClient

# Don't modify this value unless you know what you are doing.
NUM_OF_CLASSES = len(news_classes.classes)
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

SLEEP_TIME_IN_SECONDS = 1

LOG_CLICKS_TASK_QUEUE_URL = "amqp://avqwoxul:DnLJdgb71xYI_2bNIC5myl9-6NF-Hsop@hornet.rmq.cloudamqp.com/avqwoxul"
LOG_CLICKS_TASK_QUEUE_NAME = 'preference'

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

cloudAMQP_client = cloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def test_basic():
    db = mongodb_client.get_db()
    db[PREFERENCE_MODEL_TABLE_NAME].delete_many({'userId': 'test_user'})

    msg= {'userId':'test_user',
          'newsId': 'test_news',
          'timestamp': str(datetime.utcnow())}

    click_log_processor.handle_message(msg)

    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':'test_user'})

    assert model is not None
    assert len(model['preference']) == NUM_OF_CLASSES

    print "test_basic passed"

if __name__ == "__main__":
    test_basic()
