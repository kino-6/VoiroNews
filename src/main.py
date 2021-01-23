#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vManager
import NewsAPIManager
import sys
import codecs
import sys

# global setting
exe_path = "..\\SeikaSay2\\SeikaSay2.exe"
setting_json = "settings.json"

def main():
	# check args
	if len(sys.argv) < 2:
		print("arg1 = Search Word")
		return

	# fetch news
	path = "..\\News\\news.json"
	speak_list = "speak_list.txt"
	news = NewsAPIManager.NewsAPIManager(path)
	news.GetNews(str(sys.argv[1]))
	news.GenerateSpeakText(speak_list)

	# operate voiceroid
	vm = vManager.vManager(exe_path)
	vm.load_args(setting_json)
	vm.main()

main()