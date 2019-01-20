import requests
import json

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '524460d037b44f929b578257ae8d9288'
ARTICLES_API = 'articles'
DEFAULT_SOURCES = ['cnn']
SORT_BY_TOP = 'top'


def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
	return end_point+ api_name


def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
	articles = []
	for source in sources:
		payload = {'apiKey': NEWS_API_KEY,
				   'source': source,
				   'sortBy': sortBy}
		response = requests.get(buildUrl(), params = payload)
		res_json = json.loads(response.content)
		# res_json = response.json()

		#extract info
		if ((res_json is not None) and (res_json['status'] == 'ok') and (res_json['source'] is not None)):
			
			# add source for every articles
			for news in res_json['articles']:
				news['source'] = res_json['source']

			articles.extend(res_json['articles'])
	return articles