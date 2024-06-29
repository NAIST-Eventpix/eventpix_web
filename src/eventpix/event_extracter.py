import re
from pathlib import Path

import icalendar  # type: ignore[import-untyped]
from dotenv import load_dotenv
from icalendar import Calendar
from openai import OpenAI

openai_enabled = False

load_dotenv(override=True)  # take environment variables from .env.


def read(event_content_path: Path) -> icalendar.Calendar:
    event_content = event_content_path.read_text(encoding="utf8")
    response = _ask_chatgpt(event_content)
    ics_content = _get_ics_content_only(response)
    cal = get_calender(ics_content)
    return cal


def get_calender(ics_content: str) -> icalendar.Calendar:
    return Calendar.from_ical(ics_content)


# https://github.com/openai/openai-python
def _ask_chatgpt(content: str) -> str:
    if not openai_enabled:
        client = OpenAI()
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


def _get_ics_content_only(content: str) -> str:
    pattern = re.compile(r"BEGIN:VCALENDAR.*?END:VCALENDAR", re.DOTALL)
    matches = pattern.findall(content)
    return str(matches[0])
