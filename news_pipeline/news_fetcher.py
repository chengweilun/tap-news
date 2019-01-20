# -*- coding: utf-8 -*-
import os
import sys
from newspaper import Article

# from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scrapers
from cloudAMQP_client import cloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://suldldjl:LabjGQ3Dh-fG3k6C0TFZ1xJ_OhJcE7TL@shark.rmq.cloudamqp.com/suldldjl"
DEDUPE_NEWS_TASK_QUEUE_NAME = "dedupe"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://avqwoxul:DnLJdgb71xYI_2bNIC5myl9-6NF-Hsop@hornet.rmq.cloudamqp.com/avqwoxul"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = cloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = cloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is broken')
        return

    task = msg
    
    article = Article(task['url'])
    article.download()
    article.parse()

    # if task['source'] == 'cnn':
    #     text = cnn_news_scrapers.extract_news(task['url'])
    # else:
    #     print task['source']

    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)