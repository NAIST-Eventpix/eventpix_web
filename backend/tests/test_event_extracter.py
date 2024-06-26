from eventpix import event_extracter
import datetime
# import pandas as pd
# import os


class TestEventExtracter:
    # 通常の評価
    def test_event_extracter(self) -> None:
        text = ""
        cal = event_extracter.read(text)  # support icalendar library
        events = [event for event in cal.walk()]

        # xlsxpath = os.environ.get("XLSX_PATH")
        # df = pd.read_excel(xlsxpath, sheet_name=[0, "sheet2"], index_col=0)

        if len(events) >= 2:
            assert events[1]["DTSTART"].dt == datetime.datetime(2021, 4, 1, 10, 0)
            assert events[1]["DTEND"].dt == datetime.datetime(2021, 4, 1, 10, 0)
            assert events[1]["SUMMARY"] == ""
            assert events[1]["DESCRIPTION"] == ""
