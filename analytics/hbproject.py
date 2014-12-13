#!/usr/bin/env python
# -*- coding: utf-8 -*-
# post count
# posts (view_count, comment_count, like_count, publish_time)
# text 

import nltk
import jieba
import json
from pprint import pprint
# for every country get its posts count 


def get_country(data):
	country = {}
	# decoded_data = json.loads(data)
	for record in data:
		country_name = record['country_name']
		country.setdefault(country_name, 0)
		for i in record['posts']:
			view_count = i['view_count']
			comment_count = i['comment_count']
			like_count = i['like_count']
			score = score_of_count(view_count, comment_count, like_count)
			country[country_name] += score
			country[country_name] += score_of_text(i['text'])
			print country[country_name]
	return country

def score_of_count(view_count, comment_count, like_count):
	return (float(comment_count) + float(like_count))  / view_count 

def score_of_text(text):
	from snownlp import SnowNLP
	doc = list(jieba.cut(text))

	s = SnowNLP(text)

	return s.sentiments
	

if __name__ == '__main__':
	data = [{'country_name': '中国','posts_count': 3.0, 'posts':[{'view_count':20000,'comment_count':100,'like_count':100,'publish_time':20131208,'text':'是健康的减肥卡拉斯京地方'}]},
	{'country_name': '日本','posts_count': 3.0, 'posts':[{'view_count':30000,'comment_count':180,'like_count':1000,'publish_time':20131208,'text':'粉色的肌肤立刻睡觉地方'}]}]
	result = get_country(data)
	for i in result.keys():
		print i + '\'s score: ' + str(result[i])
