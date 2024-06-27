import pytz  # type: ignore[import-untyped]
from eventpix import event_extracter
import datetime

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
    #         assert events[1]["DTSTART"].dt == datetime.datetime(2021, 4, 1, 10, 0)
    #         assert events[1]["DTEND"].dt == datetime.datetime(2021, 4, 1, 10, 0)
    #         assert events[1]["SUMMARY"] == ""
    #         assert events[1]["DESCRIPTION"] == ""

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
        assert event_extracter._get_ics_content_only(content) == ics_content

    def test_get_calender(self) -> None:
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
        cal = event_extracter._get_calender(ics_content)
        events = [event for event in cal.walk("VEVENT")]
        asia = pytz.timezone("Asia/Tokyo")

        print(events[0]["SUMMARY"])

        assert events[0]["SUMMARY"] == "プロトタイピングA"

        assert events[0]["DTSTART"].dt == asia.localize(
            datetime.datetime(2023, 5, 30, 18, 0)
        )
        assert events[0]["DTEND"].dt == asia.localize(
            datetime.datetime(2023, 5, 30, 21, 0)
        )
        assert (
            events[0]["DESCRIPTION"]
            == "組み込みシステム1 - Raspberry Pi とLED/センサーを組み合わせたシステムとWebサービスの連携"
        )
        assert events[0]["LOCATION"] == "奈良先端大"
        assert events[1]["SUMMARY"] == "イノベーション創出特論1"
        assert events[1]["DTSTART"].dt == asia.localize(
            datetime.datetime(2023, 6, 1, 10, 30)
        )
        assert events[1]["DTEND"].dt == asia.localize(
            datetime.datetime(2023, 6, 1, 17, 50)
        )
        assert (
            events[1]["DESCRIPTION"]
            == "GEIOT基礎１ - パネル：先端科学技術事業化の潮流と重要性、概要先端科学技術ベンチャーの現在、ビジネスモデルキャンバス、チームわけ、アイスブレーク"
        )
        assert events[1]["LOCATION"] == "MOBIO"
