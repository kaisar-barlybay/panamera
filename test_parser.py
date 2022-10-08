from typing import Any, cast
from my_types import TTestcase
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
    for uri, test_case in test_cases.items():
      params = self.parser.scrape(uri)
      logger.debug(params)
      for param_name, (test_val, assert_type) in test_case.items():
        scraper_val = params[param_name]
        match assert_type:
          case 'equal':
            logger.debug((param_name, test_val))
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # pytest -v -s test_parser.py::TestViews::test_title_info
  def test_title_info(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      title_info = self.parser.get_title_info(soup)
      if title_info is None:
        raise Exception
      logger.debug(title_info)
      for param_name, (test_val, assert_type) in t['title_info'].items():
        test_val, assert_type = cast(tuple[Any, str], (test_val, assert_type))
        scraper_val = title_info[param_name]
        match assert_type:
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
          case 'equal':
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # pytest -v -s test_parser.py::TestViews::test_offer_short_description
  def test_offer_short_description(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      offer_short_description = self.parser.get_offer_short_description(soup)
      if offer_short_description is None:
        raise Exception
      for param_name, (test_val, assert_type) in t['offer_short_description'].items():
        test_val, assert_type = cast(tuple[Any, str], (test_val, assert_type))
        scraper_val = offer_short_description[param_name]
        match assert_type:
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
          case 'equal':
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # pytest -v -s test_parser.py::TestViews::test_offer_description
  def test_offer_description(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      offer_description = self.parser.get_offer_description(soup)
      if offer_description is None:
        raise Exception
      logger.debug(offer_description)
      for param_name, (test_val, assert_type) in t['offer_description'].items():
        test_val, assert_type = cast(tuple[Any, str], (test_val, assert_type))
        scraper_val = offer_description[param_name]
        match assert_type:
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
          case 'equal':
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # pytest -v -s test_parser.py::TestViews::test_others
  def test_others(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      others = self.parser.get_others(soup)
      if others is None:
        raise Exception
      for param_name, (test_val, assert_type) in t['others'].items():
        test_val, assert_type = cast(tuple[Any, str], (test_val, assert_type))
        scraper_val = others[param_name]
        match assert_type:
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
          case 'equal':
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # pytest -v -s test_parser.py::TestViews::test_others2
  def test_others2(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      others2 = self.parser.get_others2(soup)
      if others2 is None:
        raise Exception
      for param_name, (test_val, assert_type) in t['others2'].items():
        test_val, assert_type = cast(tuple[Any, str], (test_val, assert_type))
        scraper_val = others2[param_name]
        match assert_type:
          case 'in':
            self.assertIn(scraper_val, test_val, {param_name: test_val})
          case 'equal':
            self.assertEqual(scraper_val, test_val, {param_name: test_val})
            logger.info('success')
        logger.info(f'[OK], {test_val} == {scraper_val}')
