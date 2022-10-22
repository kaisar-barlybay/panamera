import pandas as pd
from parser import Parser
from typing import Generator
from logger import get_script_logger
from visualizer import Visualizer
from preprocessor import Preprocessor
import warnings

import seaborn as sns
logger = get_script_logger('DEBUG')
color = sns.color_palette()
sns.set_style('darkgrid')
warnings.filterwarnings('ignore')


def ignore_warn(*args, **kwargs):
  pass


warnings.warn = ignore_warn
pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))


class Main():
  def __init__(self, resolve_skewness: bool = True) -> None:
    self.parser = Parser()
    self.visualizer = Visualizer()
    self.preprocessor = Preprocessor(self.visualizer)
    self.rsk = resolve_skewness

  def load(self) -> None:
    self.df = pd.read_csv('krisha_1-502.csv')

  def a(self) -> None:
    print(f"Df shape before preprocessing is : {self.df.shape}")
    print(f"df columns: {list(self.df.columns)}")

    print(self.df.describe())
    print(self.df.columns)

  def b(self) -> None:
    print(f"\n\nFinal columns: {list(self.df.columns)}\n\n")
    print(f"Df shape after preprocessing is : {self.df.shape}")

  def grab_parallel(self, thread_count: int):
    from multiprocessing import Pool
    pool = Pool()
    df_len = len(main.df.index)/100

    results = []
    for i in range(thread_count):
      from_i = i * int(df_len / thread_count)
      to_i = (i+1) * int(df_len / thread_count) - 1
      subd = self.df.loc[from_i:to_i]
      print(f'send df of size={len(subd.index)}')
      results.append(pool.apply_async(self.preprocessor.placeFind, [subd]))
    dfs = []
    for result in results:
      dfs.append(result.get())
    df = pd.concat(dfs)
    df.to_csv('df_with_geo.csv')

  def visualize(self) -> None:
    df = self.df

    # Kaisar
    df = self.preprocessor.clean(df)
    df = self.preprocessor.missing_values(df)

    # Shynar
    df = self.preprocessor.set_category_None(df)
    df = self.preprocessor.transliterate(df)
    df.describe(include='all')  # must be run in jupyter notebook in separate cell

    # Arailym
    self.visualizer.corr(df)
    self.visualizer.describe_column(df, 'price')
    self.visualizer.std(df)

    # Olzhas
    scatter_field_names = [
        'general_area',
        'internet',
        'floor',
        'room_count',
        'non_angular',
        'max_floor',
    ]
    self.visualizer.scatters(df)
    for field_name in scatter_field_names:
      self.visualizer.scatter(self.df, from_param=field_name)

    self.df = df

  def describe_post_proc(self) -> None:
    print(self.df.describe())
    self.visualizer.describe_column(self.df, 'price')
    self.visualizer.scatters(self.df)
    self.visualizer.scatter(self.df, 'general_area')
    self.visualizer.scatter(self.df, 'floor')
    self.visualizer.scatter(self.df, 'room_count')
    self.visualizer.std(self.df)
    print([column_name for column_name in list(self.df.columns) if column_name.startswith('district')])


if __name__ == '__main__':
  main = Main()
  job = 'analyze'
  match job:
    case 'find_place':
      main.load()
      main.grab_parallel(10)

    case 'parse':
      # parse
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
          for uri, title, price in main.parser.crawl(from_page, to_page):
            yield uri

        main.parser.parse(from_page, to_page, generator)
    case 'analyze':
      main.visualize()
      # main.analyze()
    case _:
      pass
