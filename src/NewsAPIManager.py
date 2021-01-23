#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import pandas
import pickle

from datetime import datetime
from pytz import timezone

from bs4 import BeautifulSoup

import feedparser
import pprint
import urllib
import re
import os

class NewsAPIManager():
	def __init__(self, path):
		self.news_data_path = path
		self.news_data = {}
		self.keyword = list()


	def ScrapingRSS(self, url):
		url = url
		d = feedparser.parse(url)
		news = dict()
		for i, entry in enumerate(d.entries, 1):
			tmp = {
				# "no": i,
				"title": entry.title,
				# "summary": entry.summary,
				"link": entry.link,
				"published": entry.published,
			}
			news[i] = tmp

		# pprint.pprint(news)
		return news


	def GenerateTimeStamp(self):
		utc_now = datetime.now(timezone('UTC'))
		jst_now = utc_now.astimezone(timezone('Asia/Tokyo'))
		ts = jst_now.strftime("%Y%m%d_%H%M%S")
		return ts


	def GetNews(self, keyword):
		self.keyword = keyword
		s = keyword
		s_quote = urllib.parse.quote(s)
		url = "https://news.google.com/news/rss/search/section/q/" + s_quote + "/" + s_quote + "?ned=jp&amp;hl=ja&amp;gl=JP"
		
		self.news_data = self.ScrapingRSS(url)

		dir_name  = os.path.dirname(self.news_data_path) + "\\"
		file_name = os.path.splitext(os.path.basename(self.news_data_path))[0]

		file_path = dir_name + keyword + "_" + file_name + "_" + self.GenerateTimeStamp() + ".json"
		with open(file_path, 'w', encoding='UTF-8', errors='ignore') as f:
			json.dump(self.news_data, f, ensure_ascii=False, indent=4)

		return file_path


	def GenerateSpeakText(self, speak_list):
		cnt = 1

		with open(speak_list, 'w', encoding='UTF-8') as f:
			# speak start
			f.write("じゃあ、" + self.keyword + "についてのヘッドラインを読み上げるで\n")
			f.write("えーっと、全部で" + str(len(self.news_data)) + "個あるみたいやな\n")

			# value is dict
			for myvalue in self.news_data.values():
				speak = str(myvalue["title"])
				speak = speak.replace("!", "")	# 変な間ができるので削除

				if cnt % 5 == 0:
					f.write("これが" + str(cnt) + "番目のヘッドラインやで\n")
				cnt += 1

				f.write(speak + "\n")

			f.write("終わりやで、お疲れさん！\n")


	def LoadNews(self):
		pass
