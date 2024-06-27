import icalendar  # type: ignore[import-untyped]

from icalendar import Calendar
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

load_dotenv()  # take environment variables from .env.

# https://github.com/openai/openai-python

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def _get_ics_content_only(content: str) -> str:
    pattern = re.compile(r"BEGIN:VCALENDAR.*?END:VCALENDAR", re.DOTALL)
    matches = pattern.findall(content)
    return str(matches[0])


def _ask_chatgpt(content: str) -> str:
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "以下の予定内容をicsファイルで返してください\n" + content,
            }
        ],
        model="gpt-4o",
    )

    response = completion.choices[0].message.content

    if response is None:
        raise ValueError("ChatGPT response is None")

    return response


def _get_calender(ics_content: str) -> icalendar.Calendar:
    cal = Calendar.from_ical(ics_content)
    for event in cal.walk("VEVENT"):
        print(event["SUMMARY"])
        print(f"{event.name}")
        print(f"{event["DTSTART"].dt}")
        print(f"{event["DTEND"].dt}")
        print(f"{event["DESCRIPTION"]}")
    return cal


def read(event_content: str) -> icalendar.Calendar:
    response = _ask_chatgpt(event_content)
    ics_content = _get_ics_content_only(response)
    cal = _get_calender(ics_content)
    return cal


def main() -> icalendar.Calendar:
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

    return read(sample_text)


if __name__ == "__main__":
    print(main())
