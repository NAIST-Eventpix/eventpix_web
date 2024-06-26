import unittest
import ocr
import datetime
import pandas as pd


class TestOCR(unittest.TestCase):
    def test_ocr(self):
        content = ocr.open('sample.jpg')
        content.save_json('output.json')


if __name__ == "__main__":
    unittest.main()
