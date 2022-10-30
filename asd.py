import re
import multiprocessing
import pandas as pd
from time import sleep
from pandas import Series
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Ruch")


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


thread_count = 1


def feature_generation(df, return_dict, procnum):
  sleep(procnum)
  print('df_len', procnum, len(df.index))
  lat = []
  long = []
  succeed = 0
  for ind, row in df.iterrows():
    sleep(thread_count*0.4)
    add = get_address(row)
    location = geolocator.geocode(add)
    try:
      # print(location.latitude, location.longitude)
      if not (location is not None and 43 < location.latitude < 44 and 76 < location.longitude < 77):
        raise Exception
      lat.append(location.latitude)
      long.append(location.longitude)
      succeed = succeed+1
    except:
      lat.append("NA")
      long.append("NA")
    print(f'from {procnum=}: {ind=}')
  print(f'from {procnum=}: {succeed=}')

  df['Latitude'] = lat
  df['Longitude'] = long
  return_dict[procnum] = df


if __name__ == "__main__":
  df = pd.read_csv('krisha_1-502.csv')
  manager = multiprocessing.Manager()
  return_dict = manager.dict()
  jobs = []
  df_len = len(df.index)/100

  for i in range(thread_count):
    from_i = i * int(df_len / thread_count)
    to_i = (i+1) * int(df_len / thread_count) - 1
    subd = df.loc[from_i:to_i]
    p = multiprocessing.Process(target=feature_generation, args=(subd, return_dict, i))
    jobs.append(p)
    p.start()

  for proc in jobs:
    proc.join()

  df_f = pd.concat(return_dict.values())
  df_f.to_csv('df_with_geo.csv')
