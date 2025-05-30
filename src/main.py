import argparse
import json
import os
from NewsAPIManager import NewsAPIManager
from voiceroid_controller import VoiceroidController


def read_shift_jis_txt(file_path):
    """
    Shift-JIS エンコーディングで保存されたテキストファイルを読み込む関数。

    Args:
        file_path (str): 読み込むファイルのパス

    Returns:
        str: ファイルから読み取ったテキスト
    """
    try:
        with open(file_path, "r", encoding="shift_jis") as f:
            text = f.read()
        return text
    except UnicodeDecodeError as e:
        print(f"⚠️ デコードエラー: {e}")
        return ""
    except FileNotFoundError as e:
        print(f"⚠️ ファイルが見つかりません: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(description="キーワードでニュース取得しVOICEROID2で読み上げ")
    parser.add_argument("keyword", type=str, help="ニュース検索キーワード")
    args = parser.parse_args()

    # ニュース取得
    news_json_path = "..\\News\\news.json"
    manager = NewsAPIManager(news_json_path)
    news_file = manager.get_news(args.keyword)

    # ニュース本文抽出
    print(f"{news_file=}")
    text = read_shift_jis_txt(news_file)
    print(f"{text=}")

    # 読み上げ
    vc = VoiceroidController()
    vc.speak(text)


if __name__ == "__main__":
    main()
