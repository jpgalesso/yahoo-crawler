import unittest
from crawler.parser import YahooParser


class TestYahooParser(unittest.TestCase):

    def setUp(self):
        self.parser = YahooParser()

        with open("sample.html", "r", encoding="utf-8") as file:
            self.sample_html = file.read()

    def test_parse_returns_list(self):
        result = self.parser.parse(self.sample_html)
        self.assertIsInstance(result, list)

    def test_parse_extracts_correct_data(self):
        result = self.parser.parse(self.sample_html)

        self.assertEqual(result[0]["symbol"], "AMX.BA")
        self.assertEqual(result[0]["name"], "América Móvil")
        self.assertEqual(result[0]["price"], "2089.00")

    def test_parse_number_of_items(self):
        result = self.parser.parse(self.sample_html)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
