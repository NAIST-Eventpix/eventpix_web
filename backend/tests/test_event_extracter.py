from src.eventpix import event_extracter
import unittest
import datetime
# import pandas as pd
# import os


class TestEventExtracter(unittest.TestCase):
    def test_extract_event(self):
        text = ""
        cal = event_extracter.read(text)  # support icalendar library
        events = [event for event in cal.walk()]

        # xlsxpath = os.environ.get("XLSX_PATH")
        # df = pd.read_excel(xlsxpath, sheet_name=[0, "sheet2"], index_col=0)

        self.assertEqual(events[1]["DTSTART"].dt, datetime.datetime(2021, 4, 1, 10, 0))
        self.assertEqual(events[1]["DTEND"].dt, datetime.datetime(2021, 4, 1, 10, 0))
        self.assertEqual(events[1]["SUMMARY"], "")
        self.assertEqual(events[1]["DESCRIPTION"], "")


if __name__ == "__main__":
    unittest.main()
