# VoiroNews

Read Google News aloud using Voiceroid
A lightweight script that fetches the latest Google News based on a search keyword and reads it aloud via SeikaSay2, a Voiceroid integration tool.

Googleニュースを音声で読み上げるアプリケーションです。
好きなキーワードを指定するだけで、ニュースを取得し、Voiceroidで自動読み上げします。

## Install

1. Install this so great software.
 [SeikaSay2](https://hgotoh.jp/wiki/doku.php/documents/voiceroid/assistantseika/assistantseika-003)

2. Copy or move exe file to this project  
■ root (this project)
├── News/              # Logs or saved news content
├── src/               # Main source files
├── SeikaSay2    <- here!  

3. run setup.bat

```cmd
setup.bat
```

## How to use ?

Run the main script with a search keyword:

```cmd
python main.py [SearchWord]
```

```cmd
# ex.
python main.py PS5
```

## setting

```json
{
    "-cid":2001,  // 琴葉茜
    "-f":"speak_list.txt",
    "-volume":1.00,
    "-speed":0.9,
    "-pitch":1.00,
    "-intonation":1.00,
    "-emotion":"喜び 0.3"
}
```
