import re

import icalendar  # type: ignore[import-untyped]

# from openai import OpenAI
# import os
from dotenv import load_dotenv
from icalendar import Calendar

load_dotenv()  # take environment variables from .env.

# https://github.com/openai/openai-python

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )


# def read(event_content: str) -> icalendar.Calendar:
#     response = _ask_chatgpt(event_content)
#     ics_content = _get_ics_content_only(response)
#     cal = _get_calender(ics_content)
#     return cal


# def _ask_chatgpt(content: str) -> str:
#     completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "以下の予定内容をicsファイルで返してください\n" + content,
#             }
#         ],
#         model="gpt-4o",
#     )

#     response = completion.choices[0].message.content

#     if response is None:
#         raise ValueError("ChatGPT response is None")

#     return response


def _get_ics_content_only(content: str) -> str:
    pattern = re.compile(r"BEGIN:VCALENDAR.*?END:VCALENDAR", re.DOTALL)
    matches = pattern.findall(content)
    return str(matches[0])


def _get_calender(ics_content: str) -> icalendar.Calendar:
    cal = Calendar.from_ical(ics_content)
    for event in cal.walk("VEVENT"):
        print(event["SUMMARY"])
        print(f"{event.name}")
        print(f"{event["DTSTART"].dt}")
        print(f"{event["DTEND"].dt}")
        print(f"{event["DESCRIPTION"]}")
    return cal