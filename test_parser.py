from parser import Parser
from unittest import TestCase
from test_data import test_cases, patterns
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

  # pytest -v -s test_parser.py::TestViews::test_match_group
  def test_match_group(self) -> None:
    for pattern_name, (pattern, test_cases) in patterns.items():
      for text, answer in test_cases:
        d = self.parser.match_group(pattern, text)
        for param_name, true_value in answer.items():
          logger.debug((param_name, true_value, d, text))
          self.assertEqual(true_value, d[param_name], d)

  # pytest -v -s test_parser.py::TestViews::test_regex
  def test_regex(self) -> None:
    import re
    # pattern = r"(?P<general_area>\d+) м²(, жилая — (?P<living_area>\d*\.?\d*)? м²)?"
    pattern = r"(?P<floor_number>\d+) из (?P<max_floor>\d*)"
    match = re.match(pattern, '4 из 10')
    if match is not None:
      val = match.groupdict()
      logger.debug(val)

  # pytest -v -s test_parser.py::TestViews::test_scrape
  def test_scrape(self) -> None:
    for uri, feat in test_cases.items():
      params = self.parser.scrape(uri)
      logger.debug(params)
      for param_name, (value, assert_type) in feat.items():
        match assert_type:
          case 'equal':
            logger.debug((param_name, value))
            self.assertEqual(params[param_name], value, {param_name: value})
          case 'in':
            self.assertIn(params[param_name], value, {param_name: value})
