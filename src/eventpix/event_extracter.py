import os
import re
from pathlib import Path

import icalendar  # type: ignore[import-untyped]
from dotenv import load_dotenv
from icalendar import Calendar
from openai import OpenAI

load_dotenv(override=True)  # take environment variables from .env.

# https://github.com/openai/openai-python

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def read(event_content_path: Path) -> icalendar.Calendar:
    event_content = event_content_path.read_text(encoding="utf8")
    response = _ask_chatgpt(event_content)
    ics_content = _get_ics_content_only(response)
    cal = get_calender(ics_content)
    return cal


def get_calender(ics_content: str) -> icalendar.Calendar:
    return Calendar.from_ical(ics_content)


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


def _get_ics_content_only(content: str) -> str:
    pattern = re.compile(r"BEGIN:VCALENDAR.*?END:VCALENDAR", re.DOTALL)
    matches = pattern.findall(content)
    return str(matches[0])


if __name__ == "__main__":
    sample_dir = Path(__file__).parent / "sample"
    sample_text = (sample_dir / "sample_image.txt").read_text(encoding="utf8")
    cal = read(sample_text)
    for event in cal.walk("VEVENT"):
        print(event["SUMMARY"])
        print(f"{event.name}")
        print(f"{event['DTSTART'].dt}")
        print(f"{event['DTEND'].dt}")
        print(f"{event['DESCRIPTION']}")
