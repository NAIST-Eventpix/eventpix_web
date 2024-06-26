import icalendar  # type: ignore[import-untyped]

# from datetime import datetime
# from icalendar import Calendar, Event, vCalAddress, vText
# from openai import OpenAI
# import os
# import pprint
# using chatgpt api, get icalernder object
# https://github.com/openai/openai-python

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )


def read(event_content: str) -> icalendar.Calendar:
    cal = icalendar.Calendar()
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "以下の予定内容をics形式で返してください\n" + event_content,
    #         }
    #     ],
    #     model="gpt-3.5-turbo",
    # )
    # pprint.pprint(chat_completion)
    return cal


if __name__ == "__main__":
    sample_text = """ 	実施場所	時間	科目名	タイトル	詳細
5月30日(木)

奈良先端大

18:00～21:00

プロトタイピングA	組み込みシステム1	Raspberry Pi とLED/センサーを組み合わせた
システムとWebサービスの連携
6月1日
(土)

MOBIO

10:30～17:50

イノベーション創出特論1	GEIOT基礎１	パネル：先端科学技術事業化の潮流と重要性、概要
先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、
チームわけ、アイスブレーク"""

    read(sample_text)
