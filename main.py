from typing import Generator
from logger import get_script_logger
import pandas as pd
import numpy as np

# from dcwav.project.parser import Parser
from parser import Parser


logger = get_script_logger('DEBUG')


if __name__ == '__main__':
  parser = Parser()
  for i in range(46, 51):
    # for i in range(0, 1):
    paramss = []
    # page_factor = 1
    page_factor = 10
    from_page = 1 + i * page_factor
    if i != 50:
      to_page = (i+1) * page_factor
    else:
      to_page = 502
    logger.critical(f'{from_page}-{to_page}')

    def generator() -> Generator[str, None, None]:
      for uri, title, price in parser.crawl(from_page, to_page):
        yield uri

    parser.parse(from_page, to_page, generator)
