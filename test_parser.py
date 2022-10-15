from typing import Any, Generator, cast
import numpy as np
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

  def get_val(self, d: dict, cn: str) -> Any:
    try:
      np.isnan(d.get(cn))
      return None
    except TypeError:
      pass
    v = d.get(cn)
    match v:
      case 'NaN' | 'nan':
        return None
      case _:
        return v

  # Kaisar
  # pytest -v -s test_parser.py::TestViews::test_parse

  def test_parse(self) -> None:
    from_page = 1
    to_page = 1
    threshold = 3
    # cases = {k: v for k, v in test_cases.items() if k == 'https://krisha.kz//a/show/674680782'}
    cases = test_cases

    def generator() -> Generator[str, None, None]:
      i = 0
      for uri, test_case in cases.items():
        if i > threshold:
          break
        yield uri
        i += 1

    self.parser.parse(from_page, to_page, generator)
    df = self.parser.read_csv(from_page, to_page)
    i = 0
    for uri, test_case in cases.items():
      if i > threshold:
        break
      logger.debug(uri)
      test_case = cast(dict[str, dict[str, Any]], test_case)
      sub_df = df.loc[df['uri'] == uri]
      print(sub_df.head())

      if len(sub_df.index) != 1:
        raise Exception('too many / 0 rows found!')
      row = sub_df.iloc[0]

      # true values
      true_vals = {}
      for group_name, group in test_case.items():
        for param_name, true_val in group.items():
          true_vals[param_name] = true_val
      true_vals = self.parser.fill_na(true_vals, self.parser.dtypes)
      # test
      for cn in df.columns:
        if cn not in ['uri', 'text']:
          true_val = self.get_val(true_vals, cn)
          scraped_val = self.get_val(row, cn)
          self.assertEqual(true_val, scraped_val, {
              'column_name': cn,
              'true_val': true_val,
              'scraped_val': scraped_val,
              'row': row.to_dict(),
              'true_vals': true_vals
          })
      i += 1

  # Kaisar
  # pytest -v -s test_parser.py::TestViews::test_crawl

  def test_crawl(self) -> None:
    for title, uri, price in self.parser.crawl(1, 100):
      logger.info((title, uri, price))
      self.assertIsInstance(uri, str)
      self.assertIsInstance(title, str)
      self.assertIsInstance(price, int)

  # Kaisar
  # pytest -v -s test_parser.py::TestViews::test_match_group
  def test_match_group(self) -> None:
    for pattern_name, (pattern, test_cases) in patterns.items():
      for text, answer in test_cases:
        d = self.parser.match_group(pattern, text)
        logger.debug((pattern))
        for param_name, true_value in answer.items():
          logger.debug((param_name, true_value, d, text))
          d_val = d.get(param_name)
          self.assertEqual(str(true_value), d_val, d)

  # pytest -v -s test_parser.py::TestViews::test_regex
  def test_regex(self) -> None:
    import re
    # pattern = r"(?P<general_area>\d+) м²(, жилая — (?P<living_area>\d*\.?\d*)? м²)?"
    pattern = r"(?P<floor_number>\d+) из (?P<max_floor>\d*)"
    match = re.match(pattern, '4 из 10')
    if match is not None:
      val = match.groupdict()
      logger.debug(val)

  # Olzhas
  # pytest -v -s test_parser.py::TestViews::test_scrape
  def test_scrape(self) -> None:
    for uri, test_case in test_cases.items():
      test_case = cast(dict[str, dict[str, Any]], test_case)
      params = self.parser.scrape(uri)
      for section_name, section_data in test_case.items():
        for param_name, test_val in section_data.items():
          scraper_val = params[param_name]
          self.assertEqual(scraper_val, test_val, {param_name: test_val})
          logger.info(f'[OK], {scraper_val} == {test_val}')

  # Olzhas
  # pytest -v -s test_parser.py::TestViews::test_title_info
  def test_title_info(self) -> None:
    for uri, test_case in test_cases.items():
      soup = self.parser.get_soup(uri)
      title_info = self.parser.get_title_info(soup)
      if title_info is None:
        raise Exception
      logger.debug(title_info)
      for param_name, test_val in test_case['title_info'].items():
        scraper_val = title_info[param_name]
        self.assertEqual(scraper_val, test_val, {param_name: test_val, 'title_info': title_info})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # Kaisar
  # pytest -v -s test_parser.py::TestViews::test_offer_short_description
  def test_offer_short_description(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      offer_short_description = self.parser.get_offer_short_description(soup)
      if offer_short_description is None:
        raise Exception
      for param_name, test_val in t['offer_short_description'].items():
        scraper_val = offer_short_description[param_name]
        self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # Shynar
  # pytest -v -s test_parser.py::TestViews::test_offer_description
  def test_offer_description(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      offer_description = self.parser.get_offer_description(soup)
      if offer_description is None:
        raise Exception
      logger.debug(offer_description)
      for param_name, test_val in t['offer_description'].items():
        scraper_val = offer_description[param_name]
        self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # Arailym
  # pytest -v -s test_parser.py::TestViews::test_others
  def test_others(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      others = self.parser.get_others(soup)
      if others is None:
        continue
      for param_name, test_val in t['others'].items():
        scraper_val = others[param_name]
        self.assertEqual(scraper_val, test_val, {param_name: test_val})
        logger.info(f'[OK], {test_val} == {scraper_val}')

  # Kaisar
  # pytest -v -s test_parser.py::TestViews::test_others2
  def test_others2(self) -> None:
    for uri, t in test_cases.items():
      soup = self.parser.get_soup(uri)
      others2 = self.parser.get_others2(soup)
      for param_name, test_val in t['others2'].items():
        scraper_val = others2[param_name]
        self.assertEqual(scraper_val, test_val, {param_name: test_val})

        logger.info(f'[OK], {test_val} == {scraper_val}')
