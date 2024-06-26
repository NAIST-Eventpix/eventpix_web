import icalendar
from datetime import datetime
from icalendar import Calendar, Event, vCalAddress, vText
from openai import OpenAI
import os
# using chatgpt api, get icalernder object
# https://github.com/openai/openai-python

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def read(src_text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )


if __name__ == '__main__':
    read('output.ics')
