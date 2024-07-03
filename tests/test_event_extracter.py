import datetime

import pytz  # type: ignore[import-untyped]
from eventpix.event_extracter import EventExtracter

# import pandas as pd
# import os


class TestEventExtracter:
    # 通常の評価
    # def test_event_extracter(self) -> None:
    #     text = ""
    #     cal = event_extracter.read(text)  # support icalendar library
    #     events = [event for event in cal.walk()]

    #     # xlsxpath = os.environ.get("XLSX_PATH")
    #     # df = pd.read_excel(xlsxpath, sheet_name=[0, "sheet2"], index_col=0)

    #     if len(events) >= 2:
    #         assert events[1].dtstart_datetime == datetime.datetime(2021, 4, 1, 10, 0)
    #         assert events[1].dtend_datetime == datetime.datetime(2021, 4, 1, 10, 0)
    #         assert events[1].summary == ""
    #         assert events[1].description == ""

    def test_ics_content_only(self) -> None:
        content = """以下はお知らせいただいた予定内容をICS形式に変換したものです。ICSファイルはカレンダーイベントを電子的に保存および共有するための標準形式です。このファイルをカレンダーアプリケーションにインポートすることで、予定を簡単に管理できます。

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Calendar//EN
BEGIN:VEVENT
UID:20230530T180000@naist.jp
DTSTAMP:20230530T000000Z
SUMMARY:プロトタイピングA
DESCRIPTION:組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携
DTSTART;TZID=Asia/Tokyo:20230530T180000
DTEND;TZID=Asia/Tokyo:20230530T210000
LOCATION:奈良先端大
END:VEVENT
BEGIN:VEVENT
UID:20230601T103000@mobio.jp
DTSTAMP:20230601T000000Z
SUMMARY:イノベーション創出特論1
DESCRIPTION:GEIOT基礎１ - パネル：先端科学技術事業化の潮流と重要性、概要先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、チームわけ、アイスブレーク
DTSTART;TZID=Asia/Tokyo:20230601T103000
DTEND;TZID=Asia/Tokyo:20230601T175000
LOCATION:MOBIO
END:VEVENT
END:VCALENDAR
```

この内容をテキストエディタにコピーし、拡張子 `.ics` のファイルとして保存してください（例：`schedule.ics`）。その後、保存したファイルをカレンダーアプリケーションにインポートすることで、予定をカレンダーに追加できます。"""
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Calendar//EN
BEGIN:VEVENT
UID:20230530T180000@naist.jp
DTSTAMP:20230530T000000Z
SUMMARY:プロトタイピングA
DESCRIPTION:組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携
DTSTART;TZID=Asia/Tokyo:20230530T180000
DTEND;TZID=Asia/Tokyo:20230530T210000
LOCATION:奈良先端大
END:VEVENT
BEGIN:VEVENT
UID:20230601T103000@mobio.jp
DTSTAMP:20230601T000000Z
SUMMARY:イノベーション創出特論1
DESCRIPTION:GEIOT基礎１ - パネル：先端科学技術事業化の潮流と重要性、概要先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、チームわけ、アイスブレーク
DTSTART;TZID=Asia/Tokyo:20230601T103000
DTEND;TZID=Asia/Tokyo:20230601T175000
LOCATION:MOBIO
END:VEVENT
END:VCALENDAR"""
        assert EventExtracter._get_ics_content_part(content) == ics_content

    def test_get_calender1(self) -> None:
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Calendar//EN
BEGIN:VEVENT
UID:20230530T180000@naist.jp
DTSTAMP:20230530T000000Z
SUMMARY:プロトタイピングA
DESCRIPTION:組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携
DTSTART;TZID=Asia/Tokyo:20230530T180000
DTEND;TZID=Asia/Tokyo:20230530T210000
LOCATION:奈良先端大
END:VEVENT
BEGIN:VEVENT
UID:20230601T103000@mobio.jp
DTSTAMP:20230601T000000Z
SUMMARY:イノベーション創出特論1
DESCRIPTION:GEIOT基礎１ - パネル：先端科学技術事業化の潮流と重要性、概要先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、チームわけ、アイスブレーク
DTSTART;TZID=Asia/Tokyo:20230601T103000
DTEND;TZID=Asia/Tokyo:20230601T175000
LOCATION:MOBIO
END:VEVENT
END:VCALENDAR"""
        print()
        events = EventExtracter.ics2events(ics_content)
        asia = pytz.timezone("Asia/Tokyo")

        print(events[0].summary)

        assert events[0].summary == "プロトタイピングA"

        assert events[0].dtstart_datetime == asia.localize(
            datetime.datetime(2023, 5, 30, 18, 0)
        )
        assert events[0].dtend_datetime == asia.localize(
            datetime.datetime(2023, 5, 30, 21, 0)
        )
        assert (
            events[0].description
            == "組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携"
        )
        assert events[0].location == "奈良先端大"
        assert events[1].summary == "イノベーション創出特論1"
        assert events[1].dtstart_datetime == asia.localize(
            datetime.datetime(2023, 6, 1, 10, 30)
        )
        assert events[1].dtend_datetime == asia.localize(
            datetime.datetime(2023, 6, 1, 17, 50)
        )
        assert (
            events[1].description
            == "GEIOT基礎１ - パネル：先端科学技術事業化の潮流と重要性、概要先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、チームわけ、アイスブレーク"
        )
        assert events[1].location == "MOBIO"

    def test_get_calender2(self) -> None:
        ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Calendar//EN
BEGIN:VEVENT
UID:20230530T180000@naist.jp
DTSTAMP:20230530T000000Z
DESCRIPTION:組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携
DTEND;TZID=Asia/Tokyo:20230530T210000
LOCATION:奈良先端大
END:VEVENT
BEGIN:VEVENT
UID:20230601T103000@mobio.jp
DTSTAMP:20230601T000000Z
SUMMARY:イノベーション創出特論1
DTSTART;TZID=Asia/Tokyo:20230601T103000
LOCATION:MOBIO
END:VEVENT
END:VCALENDAR"""
        events = EventExtracter.ics2events(ics_content)
        asia = pytz.timezone("Asia/Tokyo")

        assert events[0].summary == ""

        assert events[0].dtstart_datetime is None

        assert events[0].dtend_datetime == asia.localize(
            datetime.datetime(2023, 5, 30, 21, 0)
        )
        assert (
            events[0].description
            == "組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携"
        )
        assert events[0].location == "奈良先端大"
        assert events[1].summary == "イノベーション創出特論1"
        assert events[1].dtstart_datetime == asia.localize(
            datetime.datetime(2023, 6, 1, 10, 30)
        )
        assert events[1].dtend_datetime is None

        assert events[1].description == ""
        assert events[1].location == "MOBIO"

    def test_get_calender3(self) -> None:
        ics_content = """何も見つかりませんでした。"""
        events = EventExtracter.ics2events(ics_content)

        assert events == []
    
    def test_add_asia_timezone(self) -> None:
        src = "DTEND:20230530T210000"
        assert EventExtracter.add_asia_timezone(src) == "DTEND;TZID=Asia/Tokyo:20230530T210000"

        src = "DTEND:20230530T210000"
        assert EventExtracter.add_asia_timezone(src) == "DTEND;TZID=Asia/Tokyo:20230530T210000"

        src = "DTEND;TZID=Asia/Tokyo:20230530T210000"
        assert EventExtracter.add_asia_timezone(src) == "DTEND;TZID=Asia/Tokyo:20230530T210000"

        src = "DTSTART:20230601T103000"
        assert EventExtracter.add_asia_timezone(src) == "DTSTART;TZID=Asia/Tokyo:20230601T103000"
