import pandas as pd
import time
import re
import logging
import requests
from requests import Response
from typing import Generator, Literal, Any
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim  # type: ignore
from pandas import DataFrame, Series
from my_types import TOfferDescription, TOfferShortDescription, TOthers, TOthers2, TParams, TTitleInfo, dtypes
from test_data import patterns
import urllib3
from my_types import TLoc
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


def geoGrab(address: str) -> TLoc | None:

  print(f"{address=}")
  geolocator = Nominatim(user_agent='user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36')
  location = geolocator.geocode(address)
  if location is not None:
    loc: TLoc = {
        'latitude': location.latitude,
        'longitude': location.longitude
    }
    return loc
  else:
    return None


def get_address(row: Series) -> str:
  city = row['city']
  ditrict = row['district']
  house_number = row['house_number']
  intersection = row['intersection']
  street = row['street']
  add = [
      f"{city}",
      f", {ditrict} район" if type(ditrict) != float else '',
      (f", {street}" if type(street) != float else ''),
      f" {house_number}" if type(house_number) != float else '',
      f" - {intersection}" if type(intersection) != float else '',
  ]
  # print(city, ditrict, house_number, intersection, street,)
  res = ''.join(add)
  res = re.sub(r'(\, (мкр|Мкр|Мкрн))?', '', res)
  return res


def placeFind(df: DataFrame) -> None:
  rows_list = []
  for ind, row in df.iterrows():
    address = get_address(row)

    coords = geoGrab(address)
    if coords is not None and 43 < coords['latitude'] < 44 and 76 < coords['longitude'] < 77:
      rows_list.append([address, coords['latitude'], coords['longitude']])
      print(f"{coords=}\n")
    else:
      rows_list.append([address, None, None])
  df2 = pd.DataFrame(rows_list, columns=['address', 'lat', 'long'])
  df3 = df.join(df2)
  df3.to_csv('df3.csv')


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

  def crawl(self, from_page: int, to_page: int) -> Generator[tuple[str, str, int], None, None]:
    for i in range(from_page, to_page + 1):
      'https://krisha.kz/prodazha/kvartiry/almaty/?das[_sys.hasphoto]=1&das[flat.priv_dorm]=2&das[house.year][from]=1970&das[who]=1&page=2'
      url = f'https://krisha.kz/prodazha/kvartiry/almaty/?page={i}'
      soup = self.get_soup(url)
      main_info_selector = 'div.a-card__main-info'
      main_infos = soup.select(main_info_selector)
      a_selector = 'div.a-card__header-left > a'
      price_selector = 'div.a-card__price'

      for main_info in main_infos:
        a_tag = main_info.select_one(a_selector)
        price_div = main_info.select_one(price_selector)
        if a_tag is not None and price_div is not None:
          price = price_div.getText().replace(r'от', '').replace(r'〒', '').replace(u'\xa0', '').strip()
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

  def get_mortgaged(self, soup: BeautifulSoup) -> bool:
    selector = 'div.offer__parameters-mortgaged'
    tag = soup.select_one(selector)
    if tag is not None:
      return True
    else:
      return False

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
    return None

  # Shynar

  def get_title_info(self, soup: BeautifulSoup) -> TTitleInfo | None:
    title_info: TTitleInfo = {}
    selector = 'div.offer__advert-title > h1'
    value = soup.select_one(selector)
    if value is None:
      return None
    # 3-комнатная квартира, 90 м², 4/10 этаж, Кенесары хана 54/39
    text = value.getText().strip()
    logger.debug(f'[{repr(text)}]')
    group = self.match_group(patterns['title_info'][0], text)

    title_info['room_count'] = self.unpack(group, 'room_count', 'int')
    title_info['floor'] = self.unpack(group, 'floor', 'int')
    title_info['max_floor'] = self.unpack(group, 'max_floor', 'int')
    title_info['street'] = self.unpack(group, 'street', 'str')
    title_info['house_number'] = self.unpack(group, 'house_number', 'str')
    title_info['general_area'] = self.unpack(group, 'general_area', 'float')
    title_info['intersection'] = self.unpack(group, 'intersection', 'str')
    title_info['microdistrict'] = self.unpack(group, 'microdistrict', 'str')
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
        case 'пластиковые окна':
          others['plastic_windows'] = True
        case 'неугловая':
          others['non_angular'] = True
        case 'улучшенная':
          others['improved'] = True
        case 'комнаты изолированы':
          others['rooms_isolated'] = True
        case 'кухня-студия':
          others['studio_kitchen'] = True
        case 'встроенная кухня':
          others['kitchen_builtin'] = True
        case 'новая сантехника':
          others['new_plumbing'] = True
        case 'кладовка':
          others['pantry'] = True
        case 'счётчики':
          others['counters'] = True
        case 'тихий двор':
          others['quiet_courtyard'] = True
        case 'кондиционер':
          others['air_conditioning'] = True
        case 'удобно под коммерцию':
          others['commercial_convenient'] = True
        case _:
          pass
    return others

  def get_private_hostel(self, soup: BeautifulSoup) -> bool:
    for i in range(1, 10):
      selector1 = f'div.offer__parameters > dl:nth-child({i})'
      selector2 = f'div.offer__parameters > dl:nth-child({i}) > dd'
      match = soup.select_one(selector1)
      if match is None:
        continue
      text = match.getText().strip()
      match2 = re.match(r'В прив. общежитии\.*', text)
      if match2 is None:
        match3 = soup.select_one(selector2)
        if match3 is None:
          return False
    return False

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
        r"((?P<building_year>\d+) г.п.)?"
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
    logger.debug((pattern, text))
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
        case 'Тип дома':
          offer_short_description['building_type'] = val
        case 'Этаж':
          # offer_short_description['floor'] = int(val)
          match = re.match(r"(?P<floor>\d+) из (?P<max_floor>\d*)", val)
          if match is not None:
            d = match.groupdict()
            offer_short_description['floor'] = int(d['floor'])
            offer_short_description['max_floor'] = int(d['max_floor'])
        case 'Площадь, м²':
          group = self.match_group(patterns['general_area'][0], val)
          offer_short_description['general_area'] = self.unpack(group, 'general_area', 'float')
          offer_short_description['living_area'] = self.unpack(group, 'living_area', 'float')
          offer_short_description['kitchen_area'] = self.unpack(group, 'kitchen_area', 'float')
        case 'Состояние':
          offer_short_description['condition'] = val
        case 'Санузел':
          offer_short_description['bathroom'] = val
        case 'Год постройки':
          offer_short_description['build_year'] = int(val)
        case 'Жилой комплекс':
          offer_short_description['residential_complex'] = val
        case 'Город':
          group = self.match_group(patterns['city'][0], val)
          offer_short_description['city'] = self.unpack(group, 'city', 'str')
          offer_short_description['district'] = self.unpack(group, 'district', 'str')
        case _:
          logger.debug(f'{key} - {val}')

    return offer_short_description

  # Olzhas
  def get_offer_description(self, soup: BeautifulSoup) -> TOfferDescription | None:
    patterns: dict[str, dict[Literal['title_pattern'], str]] = {
        'telephone': {'title_pattern': r'Телефон', },
        'internet': {'title_pattern': r'Интернет', },
        'balcony': {'title_pattern': r'Балкон$', },
        'bathroom': {'title_pattern': r'Санузел$', },
        'is_balcony_glazed': {'title_pattern': r'Балкон остеклён', },
        'door': {'title_pattern': r'Дверь', },
        'parking': {'title_pattern': r'Парковка', },
        'furniture': {'title_pattern': r'Квартира меблирована', },
        'floor_type': {'title_pattern': r'Пол$', },
        'former_hostel': {'title_pattern': r'Бывшее общежитие', },
        'ceiling_height': {'title_pattern': r'Потолки', },
        'security': {'title_pattern': r'Безопасность', },
        'exchange_possible': {'title_pattern': r'Возможен обмен', },
        # 'internet': {'title_pattern': r'Санузел', },
    }
    offer_description = {
        'telephone': None,
        'internet': None,
        'balcony': None,
        'door': None,
        'parking': None,
        'is_balcony_glazed': None,
        'furniture': None,
        'floor_type': None,
        'ceiling_height': None,
        'bars_on_the_window': None,
        'security': None,
        'entry_phone': None,
        'code_lock': None,
        'alarm': None,
        'video_security': None,
        'video_entry_phone': None,
        'concierge': None,
    }
    for i in range(1, 20):
      selector1 = f"div.offer__description > div.offer__parameters > dl:nth-child({i}) > dt"
      selector2 = f"div.offer__description > div.offer__parameters > dl:nth-child({i}) > dd"
      for param, params in patterns.items():
        try:
          title = soup.select_one(selector1).getText().strip()
          title_match = re.match(params['title_pattern'], title)
          if title_match:
            value = soup.select_one(selector2).getText().strip()
            match param:
              case 'telephone':
                offer_description['telephone'] = value
              case 'internet':
                offer_description['internet'] = value
              case 'balcony':
                offer_description['balcony'] = value
              case 'is_balcony_glazed':
                offer_description['is_balcony_glazed'] = value == 'да'
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
                offer_description['former_hostel'] = value == 'да'
              case 'ceiling_height':
                val = re.match(r'(?P<ceiling_height>\d+\.?\d*) м', value)
                offer_description['ceiling_height'] = float(val['ceiling_height'])
              case 'exchange_possible':
                offer_description['exchange_possible'] = value
              case 'security':
                vals = value.split(', ')
                for val in vals:
                  match val:
                    case 'решетки на окнах':
                      offer_description['bars_on_the_window'] = True
                    case 'охрана':
                      offer_description['security'] = True
                    case 'домофон':
                      offer_description['entry_phone'] = True
                    case 'кодовый замок':
                      offer_description['code_lock'] = True
                    case 'сигнализация':
                      offer_description['alarm'] = True
                    case 'видеонаблюдение':
                      offer_description['video_security'] = True
                    case 'видеодомофон':
                      offer_description['video_entry_phone'] = True
                    case 'консьерж':
                      offer_description['concierge'] = True
                    case _:
                      pass
              case _:
                pass
        except AttributeError as e:
          continue
    # 45 м², кухня — 6 м²

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
    return 'Алматы'

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

  def enrich(self, d1: dict, d2: dict | None) -> dict:
    if d2 is not None:
      for k, v in d2.items():
        if k not in d1:
          d1[k] = v
    return d1

  def scrape(self, uri: str) -> dict[str, float | int | str | None]:
    logger.info(f"Scraping uri: {uri}")
    soup = self.get_soup(uri)
    # logger.debug(soup)
    params: TParams = {
        'uri': uri,
    }

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
    return others2
