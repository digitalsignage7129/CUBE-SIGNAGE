import requests
import json
import os
import re

# 正しい通信先URL（末尾に不要な文字が入らないように注意してください）
URL = "https://www2.edam.ne.jp/Public/00574/Sokutei/WBGT?LoID=2452"

def main():
    try:
        # 相手方サーバーからデータを取得
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        
        # 【注意】相手方がHTMLを返す場合、ソース内のJavaScriptオブジェクトや
        # 該当のJSONレスポンス文字列を正規表現などで抽出する必要があります。
        # ここでは、前回のレスポンス形式がそのままテキストとして取得できた場合のパース例です。
        
        # 簡易的に、レスポンスの中に [ { "Time": ... } ] の形が含まれていると仮定して抽出
        # ※もし相手方が純粋なJSONを返しているなら `data = response.json()` だけでOKです。
        match = re.search(r'\[\s*\{\s*"Time".*?\}\s*\]', response.text, re.DOTALL)
        
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
        else:
            # 抽出に失敗した場合は、直近の受信データの構造に合わせて調整してください
            print("JSONデータの抽出に失敗しました。ソース構造を確認してください。")
            return

        # 同一リポジトリ内に「data.json」として書き出し
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("データの更新に成功しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
