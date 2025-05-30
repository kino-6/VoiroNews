import os
import json
import urllib.parse
import feedparser
from datetime import datetime
from pytz import timezone


class NewsAPIManager:
    def __init__(self, save_path):
        self.news_data_path = save_path
        self.news_data = {}
        self.keyword = ""

    def scraping_rss(self, url):
        d = feedparser.parse(url)
        news = dict()
        for i, entry in enumerate(d.entries, 1):
            news[i] = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
            }
        return news

    def generate_timestamp(self):
        jst_now = datetime.now(timezone("Asia/Tokyo"))
        return jst_now.strftime("%Y%m%d_%H%M%S")

    def get_news(self, keyword):
        self.keyword = keyword
        s_quote = urllib.parse.quote(keyword)
        url = (
            f"https://news.google.com/news/rss/search/section/q/{s_quote}/{s_quote}"
            "?ned=jp&hl=ja&gl=JP"
        )

        self.news_data = self.scraping_rss(url)

        save_dir = os.path.dirname(self.news_data_path)
        os.makedirs(save_dir, exist_ok=True)
        file_base = os.path.splitext(os.path.basename(self.news_data_path))[0]
        timestamp = self.generate_timestamp()

        # JSON保存
        json_path = os.path.join(save_dir, f"{keyword}_{file_base}_{timestamp}.json")
        with open(json_path, "w", encoding="utf-8", errors="ignore") as f:
            json.dump(self.news_data, f, ensure_ascii=False, indent=4)

        # テキスト保存（speak_list）
        speak_lines = self.generate_speak_text()
        txt_path = os.path.join(save_dir, f"{keyword}_{file_base}_{timestamp}_speak_list.txt")
        with open(txt_path, "w", encoding="shift_jis", errors="ignore") as f:
            for line in speak_lines:
                f.write(line + "\n")

        return txt_path  # speak_list.txt を返す

    def generate_speak_text(self):
        lines = [
            f"じゃあ、{self.keyword}についてのヘッドラインを読み上げるで",
            f"えーっと、全部で{len(self.news_data)}個あるみたいやな",
        ]
        for i, v in enumerate(self.news_data.values(), 1):
            title = v["title"].replace("!", "")
            if i % 5 == 0:
                lines.append(f"これが{i}番目のヘッドラインやで")
            lines.append(title)
        lines.append("終わりやで、お疲れさん！")
        return lines
