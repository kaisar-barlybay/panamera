from typing import TypedDict


class TLoc(TypedDict):
  latitude: float
  longitude: float


class TParams(TypedDict, total=False):
  uri: str
  # title info
  room_count: int | None
  neighborhood: str | None
  street: str | None
  house_number: str | None
  intersection: str | None
  # offer_short descr
  build_year: int | None
  district: str | None
  floor: int | None
  residential_complex: str | None
  max_floor: int | None
  general_area: float | None
  bathroom: str | None
  living_area: float | None
  kitchen_area: float | None
  condition: str | None
  # offer descr
  internet: str | None
  furniture: str | None
  ceiling_height: str | None
  floor_type: str | None
  telephone: str | None
  door: str | None
  balcony: str | None
  parking: str | None
  is_balcony_glazed: bool | None
  bars_on_the_window: bool | None
  security: bool | None
  entry_phone: bool | None
  code_lock: bool | None
  alarm: bool | None
  video_security: bool | None
  video_entry_phone: bool | None
  concierge: bool | None
  # others
  plastic_windows: bool | None
  non_angular: bool | None
  improved: bool | None
  rooms_isolated: bool | None
  studio_kitchen: bool | None
  kitchen_builtin: bool | None
  new_plumbing: bool | None
  pantry: bool | None
  counters: bool | None
  quiet_courtyard: bool | None
  air_conditioning: bool | None
  commercial_convenient: bool | None
  # etc
  installment: bool | None
  mortgage: str | None
  building_type: str | None
  price: int | None
  mortgaged: bool | None
  images_count: int | None
  private_hostel: bool | None
  city: str | None
  text: str | None


class TTitleInfo(TypedDict, total=False):
  room_count: int
  neighborhood: str
  street: str
  house_number: str
  intersection: str


class TOfferDescription(TypedDict, total=False):
  build_year: int | None
  internet: str | None
  furniture: str | None
  ceiling_height: str | None
  floor_type: str | None
  telephone: str | None
  door: str | None
  balcony: str | None
  parking: str | None
  is_balcony_glazed: bool | None
  bars_on_the_window: bool | None
  security: bool | None
  entry_phone: bool | None
  code_lock: bool | None
  alarm: bool | None
  video_security: bool | None
  video_entry_phone: bool | None
  concierge: bool | None


class TOfferShortDescription(TypedDict, total=False):
  building_type: str | None
  district: str | None
  floor: int | None
  residential_complex: str | None
  max_floor: int | None
  general_area: float | None
  bathroom: str | None
  living_area: float | None
  kitchen_area: float | None
  condition: str | None


class TOthers(TypedDict, total=False):
  plastic_windows: bool
  non_angular: bool
  improved: bool
  rooms_isolated: bool
  studio_kitchen: bool
  kitchen_builtin: bool
  new_plumbing: bool
  pantry: bool
  counters: bool
  quiet_courtyard: bool
  air_conditioning: bool
  commercial_convenient: bool


dtypes = {
    'room_count': 'int64',
    'neighborhood': 'str',
    'street': 'str',
    'house_number': 'str',
    'intersection': 'str',
    'district': 'str',
    'floor': 'int64',
    'residential_complex': 'str',
    'max_floor': 'int64',
    'general_area': 'float64',
    'bathroom': 'bool',
    'living_area': 'float64',
    'kitchen_area': 'float64',
    'condition': 'str',
    'internet': 'bool',
    'furniture': 'bool',
    'ceiling_height': 'float64',
    'floor_type': 'str',
    'telephone': 'bool',
    'door': 'str',
    'balcony': 'bool',
    'parking': 'bool',
    'is_balcony_glazed': 'bool',
    'bars_on_the_window': 'bool',
    'security': 'bool',
    'entry_phone': 'bool',
    'code_lock': 'bool',
    'alarm': 'bool',
    'video_security': 'bool',
    'video_entry_phone': 'bool',
    'concierge': 'bool',
    'plastic_windows': 'bool',
    'non_angular': 'bool',
    'improved': 'bool',
    'rooms_isolated': 'bool',
    'studio_kitchen': 'bool',
    'kitchen_builtin': 'bool',
    'new_plumbing': 'bool',
    'pantry': 'bool',
    'counters': 'bool',  # ?
    'quiet_courtyard': 'bool',
    'air_conditioning': 'bool',
    'commercial_convenient': 'bool',
    'installment': 'bool',
    'mortgage': 'bool',
    'building_type': 'str',
    'build_year': 'int64',
    'price': 'int64',
    'mortgaged': 'bool',
    'images_count': 'int64',
    'private_hostel': 'bool',
    'city': 'str',
    'text': 'str',
}
