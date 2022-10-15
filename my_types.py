from typing import Any, Union, TypedDict


class TLoc(TypedDict):
  latitude: float
  longitude: float


# class TTitleInfo(TypedDict, total=False):
TTitleInfo = TypedDict('TTitleInfo', {
    'room_count': int,
    'floor': int,
    'max_floor': int,
    'street': str,
    'house_number': str,
    'general_area': float,
    'intersection': str,
    'microdistrict': str,
})

title_info_dtypes = {
    'room_count': 'Int64',
    'floor': 'Int64',
    'max_floor': 'Int64',
    'street': 'str',
    'house_number': 'str',
    'general_area': 'Float64',
    'intersection': 'str',
    'microdistrict': 'str',
}


# class TOfferShortDescription(TypedDict, total=False):
TOfferShortDescription = TypedDict('TOfferShortDescription', {
    'building_type': str,
    'floor': int,
    'max_floor': int,
    'general_area': float,
    'kitchen_area': float,
    'living_area': float,
    'condition': str,
    'build_year': int,
    'residential_complex': str,
    'city': str,
    'district': str,
})

offer_short_description_dtypes = {
    'building_type': 'str',
    'floor': 'Int64',
    'max_floor': 'Int64',
    'general_area': 'Float64',
    'kitchen_area': 'Float64',
    'living_area': 'Float64',
    'condition': 'str',
    'build_year': 'Int64',
    'residential_complex': 'str',
    'city': 'str',
    'district': 'str',
}


# class TOfferDescription(TypedDict, total=False):
TypedOfferDescription = TypedDict('TypedOfferDescription', {
    'telephone': str,  # Телефон: есть возможность подключения
    'internet': str,
    'balcony': str,
    'is_balcony_glazed': bool,
    'door': str,
    'bathroom': str,
    'parking': str,
    'furniture': str,
    'floor_type': str,
    'former_hostel': bool,  # бывшее общежитие
    'ceiling_height': float,
    # security,
    'bars_on_the_window': bool,  # решетки на окнах
    'security': bool,  # охрана
    'entry_phone': bool,  # домофон
    'code_lock': bool,  # кодовый замок
    'alarm': bool,  # сигнализация
    'video_security': bool,  # видеонаблюдение
    'video_entry_phone': bool,  # видеодомофон
    'concierge': bool,  # консьерж
    'exchange_possible': bool,  # Возможен обмен
})

offer_description_dtypes = {
    'telephone': 'str',
    'internet': 'str',
    'balcony': 'str',
    'is_balcony_glazed': 'bool',
    'door': 'str',
    'bathroom': 'str',
    'parking': 'str',
    'furniture': 'str',
    'floor_type': 'str',
    'former_hostel': 'bool',
    'ceiling_height': 'Float64',
    # security
    'bars_on_the_window': 'bool',
    'security': 'bool',
    'entry_phone': 'bool',
    'code_lock': 'bool',
    'alarm': 'bool',
    'video_security': 'bool',
    'video_entry_phone': 'bool',
    'concierge': 'bool',
    'exchange_possible': 'bool',
}


TOthers = TypedDict('TOthers', {
    'plastic_windows': bool,
    'non_angular': bool,
    'improved': bool,
    'rooms_isolated': bool,
    'studio_kitchen': bool,
    'kitchen_builtin': bool,
    'new_plumbing': bool,
    'pantry': bool,
    'counters': bool,
    'quiet_courtyard': bool,
    'air_conditioning': bool,
    'commercial_convenient': bool,
})

others_dtypes = {
    'plastic_windows': 'bool',
    'non_angular': 'bool',
    'improved': 'bool',
    'rooms_isolated': 'bool',
    'studio_kitchen': 'bool',
    'kitchen_builtin': 'bool',
    'new_plumbing': 'bool',
    'pantry': 'bool',
    'counters': 'bool',
    'quiet_courtyard': 'bool',
    'air_conditioning': 'bool',
    'commercial_convenient': 'bool',
}


# class TOthers2(TypedDict, total=False):
TOthers2 = TypedDict('TOthers2', {
    'price': int,
    'mortgaged': bool,
    'images_count': int,
    'private_hostel': bool,
    'text': str,
}
)

others2_dtypes = {
    'price': 'Int64',
    'mortgaged': 'bool',
    'images_count': 'Int64',
    'private_hostel': 'bool',
    'text': 'str',
}


URI = TypedDict('URI', {
    'uri': str,
})

TParams = Union[URI, TTitleInfo, TypedOfferDescription, TypedOfferDescription, TOthers, TOthers2]

dtypes = {'uri': 'str'} | title_info_dtypes | offer_short_description_dtypes | offer_description_dtypes | others_dtypes | others2_dtypes


class TTestcase(TypedDict, total=False):
  title_info: TTitleInfo
  offer_short_description: TOfferShortDescription
  offer_description: TypedOfferDescription
  others: TOthers
  others2: TOthers2
