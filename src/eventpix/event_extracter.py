import re
import warnings
from pathlib import Path

from dotenv import load_dotenv
from icalendar import Calendar  # type: ignore[import-untyped]
from openai import OpenAI

from eventpix.event import Event

load_dotenv(override=True)  # take environment variables from .env.


class EventExtracter:
    def __init__(self, event_content_path: Path):
        event_content = event_content_path.read_text(encoding="utf8")
        self.response = self._ask_chatgpt(event_content)
        self.ics_content = self._get_ics_content_part(self.response)

    @property
    def events(self) -> list[Event]:
        return self.ics2events(self.ics_content)

    @staticmethod
    def ics2events(ics_src: str | Path) -> list[Event]:
        if isinstance(ics_src, str):
            ics_content = ics_src
        elif isinstance(ics_src, Path):
            ics_content = ics_src.read_text(encoding="utf8")
        else:
            raise ValueError("ics_src is not str or Path")

        result: list[Event] = []

        ics_content = EventExtracter.add_asia_timezone(ics_content)

        try:
            caldendar = Calendar.from_ical(ics_content)
        except ValueError:
            warnings.warn("Failed to parse ics_content")
            return result

        for component in caldendar.walk("VEVENT"):
            event = Event(
                component.get("DTSTART"),
                component.get("DTEND"),
                component.get("SUMMARY"),
                component.get("DESCRIPTION"),
                component.get("LOCATION"),
            )
            result.append(event)
        return result

    @staticmethod
    def _ask_chatgpt(content: str) -> str:
        # https://github.com/openai/openai-python
        client = OpenAI()
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "以下の予定内容をicsファイルで返してください\n"
                    + content,
                }
            ],
            model="gpt-4o",
        )

        response = completion.choices[0].message.content

        if response is None:
            raise ValueError("ChatGPT response is None")

        return response

    @staticmethod
    def _get_ics_content_part(content: str) -> str:
        pattern = re.compile(r"BEGIN:VCALENDAR.*?END:VCALENDAR", re.DOTALL)
        matches = pattern.findall(content)
        return str(matches[0])

    @staticmethod
    def add_asia_timezone(src: str) -> str:
        tmp = src
        tmp = tmp.replace("DTSTART:", "DTSTART;TZID=Asia/Tokyo:")
        tmp = tmp.replace("DTEND:", "DTEND;TZID=Asia/Tokyo:")
        dst = tmp
        return dst
