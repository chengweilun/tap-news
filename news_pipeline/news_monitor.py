# -*- coding: utf-8 -*-
import datetime
import os
import redis
import hashlib
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import news_api_client
from cloudAMQP_client import cloudAMQPClient

SLEEP_TIME_IN_SECONDS = 10

REDIS_HOST = 'localhost'
REDOS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600*24

SCRAPE_NEWS_TASKS_QUEUE_URL = "amqp://avqwoxul:DnLJdgb71xYI_2bNIC5myl9-6NF-Hsop@hornet.rmq.cloudamqp.com/avqwoxul"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

NEWS_SOURCES = [
	'cnn'
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redis_client = redis.StrictRedis(REDIS_HOST,REDOS_PORT)
cloudAMQP_client = cloudAMQPClient(SCRAPE_NEWS_TASKS_QUEUE_URL,SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
	news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)

	num_of_new_news = 0

	for news  in news_list:
		news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

		if redis_client.get(news_digest) is None:
			num_of_new_news = num_of_new_news + 1
			news['digest'] = news_digest

			if news['publishedAt'] is None:
				news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

			redis_client.set(news_digest, 1)
			redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
			cloudAMQP_client.sendMessage(news)
	print "Fetched %d new news" % num_of_new_news
	cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)