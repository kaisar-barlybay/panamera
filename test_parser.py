from parser import Parser
from unittest import TestCase
from test_data import test_cases
from logger import get_script_logger
logger = get_script_logger('DEBUG')


# pytest -v -s test_parser.py
class TestViews(TestCase):
  def __init__(self, methodName: str = ...) -> None:  # type: ignore
    super().__init__(methodName)
    self.parser = Parser()  # type: ignore

  # pytest -v -s test_parser.py::TestViews::test_crawl
  def test_crawl(self) -> None:
    for title, uri, price in self.parser.crawl(1, 100):
      logger.info((title, uri, price))
      self.assertIsInstance(uri, str)
      self.assertIsInstance(title, str)
      self.assertIsInstance(price, int)

  # pytest -v -s test_parser.py::TestViews::test_regex
  def test_regex(self) -> None:
    import re
    pattern = r"(?P<general_area>\d+) м²(, жилая — (?P<living_area>\d*\.?\d*)? м²)?"
    match = re.match(pattern, '148 м², жилая — 88.9 м², кухня — 24.7 м²')
    if match is not None:
      val = match.groupdict()
      logger.debug(val)

  # pytest -v -s test_parser.py::TestViews::test_scrape
  def test_scrape(self) -> None:
    for uri, feat in test_cases.items():
      params = self.parser.scrape(uri)
      logger.debug(params)
      for param_name, test_case in feat.items():
        value = test_case[0]
        assert_type = test_case[1]
        match assert_type:
          case 'equal':
            self.assertEqual(params[param_name], value, {param_name: value})
          case 'in':
            self.assertIn(params[param_name], value, {param_name: value})
