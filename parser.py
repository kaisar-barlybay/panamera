import pandas as pd
import time
import re
import logging
import requests
from requests import Response
from typing import Callable, Generator, Literal, Any
from bs4 import BeautifulSoup

from pandas import DataFrame, Series
from my_types import TypedOfferDescription, TOfferShortDescription, TOthers, TOthers2, TParams, TTitleInfo, dtypes, title_info_dtypes, offer_description_dtypes, offer_short_description_dtypes, others2_dtypes, others_dtypes
from test_data import patterns
import urllib3
from my_types import TLoc
import numpy as np
logger = logging.getLogger('default')


def fetch(url: str, method: str = 'GET', params: dict = {}, data: dict = {}, stream: bool = False) -> Response:
  # SSLError - dh key too small
  # requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  config: dict = {
      "method": method,
      "url": url,
      "params": params,
      "data": data,
      "stream": stream,
  }

  r = requests.request(**config, verify=False)

  r.encoding = r.apparent_encoding

  return r


class Parser:
  def __init__(self, use_webdriver: bool = False) -> None:
    self.use_webdriver = use_webdriver
    # if use_webdriver:
    #   chrome_driver_path = 'C:\\chromedriver.exe'
    #   firefox_binary_path = 'C:\\Users\\barlybay.kaisar\\Desktop\\Tor Browser\\Browser\\firefox.exe'
    #   firefox_profile_path = 'C:\\Users\\barlybay.kaisar\\Desktop\\Tor Browser\\Browser\\TorBrowser\Data\\Browser\\profile.default'
    #   geckodriver_path = 'C:\\geckodriver.exe'
    #   self.webdriver = Webdriver('tordriver', chrome_driver_path, firefox_binary_path, firefox_profile_path, geckodriver_path, True)
    self.dtypes = dtypes

  def read_csv(self, path: str) -> DataFrame:
    df = pd.read_csv(path)
    # df = df.fillna(value=np.nan)
    df.set_index('uri')
    df = self.format_df(df)
    df.replace(to_replace=['None'], value=np.nan, inplace=True)
    df.replace(to_replace=['True'], value=True, inplace=True)
    df.replace(to_replace=['False'], value=False, inplace=True)
    return df

  def format_df(self, df: DataFrame) -> DataFrame:
    for column_name, dtype in self.dtypes.items():
      logger.debug(f"{column_name}: {df[column_name].dtypes} - {dtype}")
      match dtype:
        case 'Int64':
          df[column_name] = np.floor(pd.to_numeric(df[column_name], errors='coerce')).astype(dtype)
        case _:
          df[column_name] = df[column_name].astype(dtype)
    return df

  def format_df_name(self, from_page: int, to_page: int) -> str:
    return f"krisha_{from_page}-{to_page}.csv"

  def parse(self, from_page: int, to_page: int, generator: Generator[str, None, None]) -> None:
    paramss = []
    for uri in generator():
      params = self.scrape(uri)
      paramss.append(params)

    df = pd.DataFrame(paramss, columns=list(self.dtypes.keys()))
    df.set_index('uri')
    df = self.format_df(df)
    df = df.fillna(value=np.nan)
    df.to_csv(self.format_df_name(from_page, to_page), encoding='utf-8', index=False, na_rep=np.nan)
    print(df.head)

  def crawl(self, from_page: int, to_page: int) -> Generator[tuple[str, str, int], None, None]:
    for i in range(from_page, to_page + 1):
      # 'https://krisha.kz/prodazha/kvartiry/almaty/?das[_sys.hasphoto]=1&das[flat.priv_dorm]=2&das[house.year][from]=1970&das[who]=1&page=2'
      url = f'https://krisha.kz/prodazha/kvartiry/almaty/?das[_sys.hasphoto]=1&das[flat.priv_dorm]=2&das[house.year][from]=1970&das[who]=1&page={i}'
      soup = self.get_soup(url)
      main_info_selector = 'div.a-card__main-info'
      main_infos = soup.select(main_info_selector)
      a_selector = 'div.a-card__header-left > a'
      price_selector = 'div.a-card__price'

      for main_info in main_infos:
        a_tag = main_info.select_one(a_selector)
        price_div = main_info.select_one(price_selector)
        if a_tag is not None and price_div is not None:
          price = price_div.getText().replace(r'????', '').replace(r'???', '').replace(u'\xa0', '').strip()
          uri = f"https://krisha.kz/{a_tag['href']}"
          title = a_tag.getText().strip()
          yield uri, title, int(price)

  def get_soup(self, url: str) -> BeautifulSoup:
    logger.debug(f'Fetching url: {url}')
    # we need this step, because site bans due often requests
    time.sleep(1)
    resp = fetch(url)
    return BeautifulSoup(resp.text, 'html.parser')

  def get_price(self, soup: BeautifulSoup) -> int | None:
    selector = 'div.offer__price'
    mortgage_selector = 'div.offer__sidebar-header > p'
    tag = soup.select_one(selector)
    if tag is not None:
      text = tag.getText()
      return int(''.join(re.findall(r'\d+', text)))
    else:
      tag = soup.select_one(mortgage_selector)
      if tag is not None:
        text = tag.getText()
        return int(''.join(re.findall(r'\d+', text)))
      else:
        return None

  def get_mortgaged(self, soup: BeautifulSoup) -> Literal[True, None]:
    selector = 'div.offer__parameters-mortgaged'
    tag = soup.select_one(selector)
    if tag is not None:
      return True
    else:
      return None

  def unpack(self, d: dict, name: str, t: Literal['str', 'float', 'int']) -> Any:
    d_str = d.get(name)
    if d_str is not None:
      match t:
        case 'int':
          return int(d_str)
        case 'float':
          return float(d_str)
        case _:
          return d_str
    return np.nan

  def fill_na(self, d: dict, types: dict[str, Literal['bool', 'Float64', 'Int64', 'str']], for_pandas: bool = True) -> dict:
    for param_name, t in types.items():
      if param_name not in d:
        match t:
          case 'bool':
            d[param_name] = False
          case 'Float64' | 'Int64':
            d[param_name] = np.nan if for_pandas is True else None
          case 'str':
            d[param_name] = np.nan if for_pandas is True else None
    logger.info(d)
    return d

  # Shynar
  def get_title_info(self, soup: BeautifulSoup) -> TTitleInfo | None:
    title_info: TTitleInfo = {}
    selector = 'div.offer__advert-title > h1'
    value = soup.select_one(selector)
    if value is None:
      return None
    # 3-?????????????????? ????????????????, 90 ????, 4/10 ????????, ???????????????? ???????? 54/39
    text = value.getText().strip()
    # logger.debug(f'[{repr(text)}]')
    group = self.match_group(patterns['title_info'][0], text)

    title_info['room_count'] = self.unpack(group, 'room_count', 'int')
    title_info['floor'] = self.unpack(group, 'floor', 'int')
    title_info['max_floor'] = self.unpack(group, 'max_floor', 'int')
    title_info['street'] = self.unpack(group, 'street', 'str')
    title_info['house_number'] = self.unpack(group, 'house_number', 'str')
    title_info['general_area'] = self.unpack(group, 'general_area', 'float')
    title_info['intersection'] = self.unpack(group, 'intersection', 'str')
    title_info['microdistrict'] = self.unpack(group, 'microdistrict', 'str')
    title_info = self.fill_na(title_info, title_info_dtypes)
    return title_info

  # Kaisar
  def get_others(self, soup: BeautifulSoup) -> TOthers | None:
    others: TOthers = {}
    selector = 'div.offer__description > div.text > div.a-options-text.a-text-white-spaces'
    value = soup.select_one(selector)
    if value is None:
      logger.error("No others section")
      return None
    text = value.getText().strip()
    vals = text.split(', ')
    for val in vals:
      val = re.sub(r'\.', '', val)
      match val.lower():
        case '?????????????????????? ????????':
          others['plastic_windows'] = True
        case '??????????????????':
          others['non_angular'] = True
        case '????????????????????':
          others['improved'] = True
        case '?????????????? ??????????????????????':
          others['rooms_isolated'] = True
        case '??????????-????????????':
          others['studio_kitchen'] = True
        case '???????????????????? ??????????':
          others['kitchen_builtin'] = True
        case '?????????? ????????????????????':
          others['new_plumbing'] = True
        case '????????????????':
          others['pantry'] = True
        case '????????????????':
          others['counters'] = True
        case '?????????? ????????':
          others['quiet_courtyard'] = True
        case '??????????????????????':
          others['air_conditioning'] = True
        case '???????????? ?????? ??????????????????':
          others['commercial_convenient'] = True
        case _:
          pass
    others = self.fill_na(others, others_dtypes)
    return others

  def get_private_hostel(self, soup: BeautifulSoup) -> Literal[True, None]:
    for i in range(1, 10):
      selector1 = f'div.offer__parameters > dl:nth-child({i})'
      selector2 = f'div.offer__parameters > dl:nth-child({i}) > dd'
      match = soup.select_one(selector1)
      if match is None:
        continue
      text = match.getText().strip()
      match2 = re.match(r'?? ????????. ??????????????????\.*', text)
      if match2 is None:
        match3 = soup.select_one(selector2)
        if match3 is None:
          return None
    return None

  def get_building_type__building_year(self, soup: BeautifulSoup) -> tuple[str | None, int | None]:
    selector = 'div:nth-child(2) > div.offer__advert-short-info'
    tag = soup.select_one(selector)
    if tag is None:
      return None, None
    text = tag.getText().strip()
    logger.debug(text)
    pattern = (
        r"(?P<building_type>\w+)?"
        r"(, )?"
        r"((?P<building_year>\d+) ??.??.)?"
    )
    match = re.match(pattern, text)
    if match is None:
      return None, None
    val = match.groupdict()
    building_type = val.get('building_type', None)
    build_year = int(val['building_year']) if val['building_year'] is not None else None
    return building_type, build_year

  def parseFloat(self, d: dict, key: str) -> float | None:
    val = d.get(key)
    if isinstance(val, str):
      return float(val)
    else:
      return None

  def parseInt(self, d: dict, key: str) -> int | None:
    val = d.get(key)
    if isinstance(val, str):
      return int(val)
    else:
      return None

  def denonify(self, d: dict) -> dict:
    for k in list(d.keys()):
      if d[k] == None or d[k] == [] or d[k] == {} or d[k] == '':
        del d[k]
    return d

  def match_group(self, pattern: str, text: str) -> dict:
    match = re.match(pattern, text)
    if match is not None:
      return self.denonify(match.groupdict())
    else:
      return {}

  # Arailym
  def get_offer_short_description(self, soup: BeautifulSoup) -> TOfferShortDescription | None:
    offer_short_description: TOfferShortDescription = {}
    block_selector = 'div.offer__info-item'
    key_selector = 'div.offer__info-title'
    val_selector = 'div.offer__advert-short-info'
    blocks = soup.select(block_selector)
    for block in blocks:
      key_tag = block.select_one(key_selector)
      val_tag = block.select_one(val_selector)
      # logger.debug((key_tag, val_tag))
      if key_tag is None or val_tag is None:
        continue

      key = key_tag.getText().strip()
      val = val_tag.getText().strip()

      match key:
        case '?????? ????????':
          offer_short_description['building_type'] = val
        case '????????':
          # offer_short_description['floor'] = int(val)
          match = re.match(r"(?P<floor>\d+) ???? (?P<max_floor>\d*)", val)
          if match is not None:
            d = match.groupdict()
            offer_short_description['floor'] = int(d['floor'])
            offer_short_description['max_floor'] = int(d['max_floor'])
        case '??????????????, ????':
          group = self.match_group(patterns['general_area'][0], val)
          offer_short_description['general_area'] = self.unpack(group, 'general_area', 'float')
          offer_short_description['living_area'] = self.unpack(group, 'living_area', 'float')
          offer_short_description['kitchen_area'] = self.unpack(group, 'kitchen_area', 'float')
        case '??????????????????':
          offer_short_description['condition'] = val
        case '??????????????':
          offer_short_description['bathroom'] = val
        case '?????? ??????????????????':
          offer_short_description['build_year'] = int(val)
        case '?????????? ????????????????':
          offer_short_description['residential_complex'] = val
        case '??????????':
          group = self.match_group(patterns['city'][0], val)
          offer_short_description['city'] = self.unpack(group, 'city', 'str')
          offer_short_description['district'] = self.unpack(group, 'district', 'str')
        case _:
          logger.debug(f'{key} - {val}')

    offer_short_description = self.fill_na(offer_short_description, offer_short_description_dtypes)
    return offer_short_description

  # Olzhas
  def get_offer_description(self, soup: BeautifulSoup) -> TypedOfferDescription | None:
    patterns: dict[str, str] = {
        'telephone': r'??????????????',
        'internet': r'????????????????',
        'balcony': r'????????????$',
        'bathroom': r'??????????????$',
        'is_balcony_glazed': r'???????????? ????????????????',
        'door': r'??????????',
        'parking': r'????????????????',
        'furniture': r'???????????????? ??????????????????????',
        'floor_type': r'??????$',
        'former_hostel': r'???????????? ??????????????????',
        'ceiling_height': r'??????????????',
        'security': r'????????????????????????',
        'exchange_possible': r'???????????????? ??????????',
    }
    offer_description: TypedOfferDescription = {}
    for i in range(1, 20):
      selector1 = f"div.offer__description > div.offer__parameters > dl:nth-child({i}) > dt"
      selector2 = f"div.offer__description > div.offer__parameters > dl:nth-child({i}) > dd"
      for param_name, pattern in patterns.items():
        try:
          title = soup.select_one(selector1).getText().strip()
          title_match = re.match(pattern, title)
          if title_match:
            value = soup.select_one(selector2).getText().strip()
            match param_name:
              case 'telephone':
                offer_description['telephone'] = value
              case 'internet':
                offer_description['internet'] = value
              case 'balcony':
                offer_description['balcony'] = value
              case 'is_balcony_glazed':
                offer_description['is_balcony_glazed'] = value == '????'
              case 'door':
                offer_description['door'] = value
              case 'bathroom':
                offer_description['bathroom'] = value
              case 'parking':
                offer_description['parking'] = value
              case 'furniture':
                offer_description['furniture'] = value
              case 'floor_type':
                offer_description['floor_type'] = value
              case 'former_hostel':
                offer_description['former_hostel'] = value == '????'
              case 'ceiling_height':
                val = re.match(r'(?P<ceiling_height>\d+\.?\d*) ??', value)
                offer_description['ceiling_height'] = float(val['ceiling_height'])
              case 'exchange_possible':
                offer_description['exchange_possible'] = value == '???????????????? ??????????'
              case 'security':
                vals = value.split(', ')
                for val in vals:
                  match val:
                    case '?????????????? ???? ??????????':
                      offer_description['bars_on_the_window'] = True
                    case '????????????':
                      offer_description['security'] = True
                    case '??????????????':
                      offer_description['entry_phone'] = True
                    case '?????????????? ??????????':
                      offer_description['code_lock'] = True
                    case '????????????????????????':
                      offer_description['alarm'] = True
                    case '??????????????????????????????':
                      offer_description['video_security'] = True
                    case '????????????????????????':
                      offer_description['video_entry_phone'] = True
                    case '????????????????':
                      offer_description['concierge'] = True
                    case _:
                      pass
              case _:
                pass
        except AttributeError as e:
          continue

    offer_description = self.fill_na(offer_description, offer_description_dtypes)
    return offer_description

  def get_installment_mortgage(self, soup: BeautifulSoup) -> tuple[bool, bool]:

    mortgage_selector = 'span.credit-badge.credit-badge--hypothec-full'
    installment_selector = 'span.credit-badge.credit-badge--installment'
    try:
      value = soup.select_one(mortgage_selector).getText().strip()
      mortgage = True
    except AttributeError as e:
      mortgage = False
    try:
      value = soup.select_one(installment_selector).getText().strip()
      installment = True
    except AttributeError as e:
      installment = False
    return installment, mortgage

  def get_city(self, soup: BeautifulSoup) -> str:
    return '????????????'

  def get_text(self, soup: BeautifulSoup) -> str:
    selector = r'div.offer__description > div.text'
    try:
      return soup.select_one(selector).getText().strip()
    except AttributeError as e:
      return None

  def get_images_count(self, soup: BeautifulSoup) -> int:
    selector = 'div.gallery__container > ul > li'
    image_lis = soup.select(selector)
    return len(image_lis)

  def enrich(self, destination: dict, source: dict | None) -> dict:
    if source is not None:
      for key, value in source.items():
        if key not in destination:
          destination[key] = value
    return destination

  def scrape(self, uri: str) -> TParams:
    logger.info(f"Scraping uri: {uri}")
    soup = self.get_soup(uri)
    # logger.debug(soup)
    params: TParams = {}
    params['uri'] = uri

    title_info = self.get_title_info(soup)
    self.enrich(params, title_info)

    offer_short_description = self.get_offer_short_description(soup)
    self.enrich(params, offer_short_description)

    offer_description = self.get_offer_description(soup)
    self.enrich(params, offer_description)

    others = self.get_others(soup)
    self.enrich(params, others)

    others2 = self.get_others2(soup)
    self.enrich(params, others2)
    return params

  # Shynar
  def get_others2(self, soup) -> TOthers2:
    others2 = {}
    others2['price'] = self.get_price(soup)
    others2['mortgaged'] = self.get_mortgaged(soup)
    others2['images_count'] = self.get_images_count(soup)
    others2['private_hostel'] = self.get_private_hostel(soup)
    others2['text'] = self.get_text(soup)
    others2 = self.fill_na(others2, others2_dtypes)
    return others2
