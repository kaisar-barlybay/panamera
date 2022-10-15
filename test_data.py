from my_types import TTestcase
building_types = ['монолитный', 'кирпичный', 'панельный', 'иное']


# Arailym
test_cases: dict[str, TTestcase] = {
    'https://krisha.kz//a/show/674680782': {
        'title_info': {
            'room_count': 3,
            'floor': 4,
            'general_area': 90,
            'max_floor': 10,
            'street': 'Кенесары хана',
            'house_number': '54/39',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 4,
            'max_floor': 10,
            'city': 'Алматы',
            'district': 'Наурызбайский',
            'general_area': 90,
            'condition': 'хорошее',
            'residential_complex': 'Хан Тенгри',
            'build_year': 2013,
        },
        'offer_description': {
            'bathroom': 'раздельный',
            'balcony': 'несколько балконов или лоджий',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'оптика',
            'parking': 'паркинг',
            'furniture': 'полностью',
            'floor_type': 'ламинат',
            'ceiling_height': 2.9,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'plastic_windows': True,
            'quiet_courtyard': True,
            'non_angular': True,
            'improved': True,
            'rooms_isolated': True,
            'kitchen_builtin': True,
            'new_plumbing': True,
            'counters': True,
        },
        'others2': {
            'images_count': 22,
            'price': 66900000,
        },
    },
    'https://krisha.kz/a/show/679286505': {
        'title_info': {
            'room_count': 1,
            'general_area': 35,
            'floor': 1,
            'max_floor': 5,
            'street': 'Мынбаева',
            'house_number': '47А',
            'intersection': 'Ауэзова',
        },
        'offer_short_description': {
            'building_type': 'панельный',
            'floor': 1,
            'max_floor': 5,
            'general_area': 35,
            'kitchen_area': 6,
            'condition': 'хорошее',
            'build_year': 1981,
            'city': 'Алматы',
            'district': 'Бостандыкский',
            'bathroom': 'совмещенный',
        },
        'offer_description': {
            'balcony': 'балкон',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'оптика',
            'parking': 'рядом охраняемая стоянка',
            'floor_type': 'линолеум',
            'ceiling_height': 2.6,
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'plastic_windows': True,
            'commercial_convenient': True,
            'kitchen_builtin': True,
            'new_plumbing': True,
            'counters': True,
            'quiet_courtyard': True,
        },
        'others2': {
            'price': 27700000,
        },
    },
    'https://krisha.kz/a/show/27290921': {
        'title_info': {
            'room_count': 3,
            'general_area': 90,
            'floor': 4,
            'max_floor': 9,
            'microdistrict': '№12',
            'street': '12-й мкр',
            'house_number': '22/2',
            'intersection': 'Шаляпина',
        },
        'offer_short_description': {
            'floor': 4,
            'max_floor': 9,
            'general_area': 90,
            'bathroom': '2 с/у и более',
            'build_year': 2017,
            'residential_complex': 'Park House',
            'city': 'Алматы',
            'district': 'Ауэзовский',
        },
        'offer_description': {
            'door': 'бронированная',
            'telephone': 'отдельный',
            'internet': 'через TV кабель',
            'furniture': 'полностью',
            'floor_type': 'паркет',
            'ceiling_height': 3,
            'security': True,
            'entry_phone': True,
            'alarm': True,
            'video_security': True,
            'video_entry_phone': True,
            'concierge': True,
        },
        'others': {
            'plastic_windows': True,
            'non_angular': True,
            'improved': True,
            'kitchen_builtin': True,
            'new_plumbing': True,
            'quiet_courtyard': True,
            'air_conditioning': True,
        },
        'others2': {
            'price': 59500000,
            'images_count': 36,
        },
    },
    'https://krisha.kz/a/show/676253177': {
        'title_info': {
            'room_count': 2,
            'general_area': 51.8,
            'floor': 4,
            'max_floor': 5,
            'microdistrict': 'Кулагер',
            'street': 'Мукатая Беспакова',
            # 'house_number': None,
            'intersection': 'Омарова',
        },
        'offer_short_description': {
            'floor': 4,
            'max_floor': 5,
            'general_area': 51.8,
            'living_area': 49.7,
            'kitchen_area': 9,
            'bathroom': 'раздельный',
            'build_year': 1988,
            'condition': 'хорошее',
            'city': 'Алматы',
            'district': 'Жетысуский',
        },
        'offer_description': {
            'telephone': 'отдельный',
            'internet': 'оптика',
            'balcony': 'балкон и лоджия',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            'furniture': 'частично',
            'floor_type': 'линолеум',
            'former_hostel': False,
            'ceiling_height': 2.7,
            'entry_phone': True,
            'video_security': True,
        },
        'others': {
            'plastic_windows': True,
            'rooms_isolated': True,
            'counters': True,
            'quiet_courtyard': True,
        },
        'others2': {
            'price': 35000000,
            'images_count': 17,
        },
    },



    # Arailym
    'https://krisha.kz/a/show/678978706': {  # 1
        'title_info': {
            'room_count': 4,
            'floor': 4,
            'general_area': 109,
            'max_floor': 10,
            'street': 'Кенесары хана',
            'house_number': '54/38',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 4,
            'max_floor': 10,
            'city': 'Алматы',
            'district': 'Наурызбайский',
            'general_area': 109,
            'condition': 'хорошее',
            'residential_complex': 'Хан Тенгри',
            'build_year': 2013,
        },
        'offer_description': {
            'bathroom': '2 с/у и более',
            'balcony': 'балкон и лоджия',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'ADSL',
            'floor_type': 'паркет',
            'ceiling_height': 2.8,
            'security': True,
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 109,
        },
        'others2': {
            'images_count': 29,
        },
    },
    'https://krisha.kz/a/show/678631102': {  # 2
        'title_info': {
            'room_count': 3,
            'floor': 2,
            'general_area': 159.4,
            'max_floor': 6,
            'street': 'Жамбыла',
            'house_number': '75',
        },
        'offer_short_description': {
            'building_type': 'панельный',
            'floor': 2,
            'max_floor': 6,
            'city': 'Алматы',
            'district': 'Алмалинский',
            'general_area': 159.4,
            'build_year': 2002,
        },
        'offer_description': {

            'is_balcony_glazed': True,
            'door': 'металлическая',
            'parking': 'паркинг',
            'floor_type': 'паркет',
            'ceiling_height': 3,
            'former_hostel': False,
            'exchange_possible': 'Возможен обмен',
        },
        'others': {
            'living_area': 159.4,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 15,
        },
    },
    'https://krisha.kz/a/show/678217538': {  # 3
        'title_info': {
            'room_count': 3,
            'floor': 2,
            'general_area': 119.4,
            'max_floor': 3,
            'street': 'Искендерова',
            'house_number': '23',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 2,
            'max_floor': 3,
            'city': 'Алматы',
            'district': 'Бостандыкский',
            'general_area': 119.4,
            'condition': 'хорошее',
            'residential_complex': 'Ideal Residence',
            'build_year': 2018,
        },
        'offer_description': {
            'bathroom': '2 с/у и более',
            # 'balcony': 'балкон',
            # 'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'оптика',
            'parking': 'паркинг',
            'furniture': 'полностью',
            'floor_type': 'ламинат',
            'ceiling_height': 3,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 119.4,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 23,
        },
    },
    'https://krisha.kz/a/show/679446203': {  # 4
        'title_info': {
            'room_count': 2,
            'floor': 2,
            'general_area': 40,
            'max_floor': 2,
            'street': 'Суюнбая',
            'house_number': '292',
        },
        'offer_short_description': {
            'building_type': 'кирпичный',
            'floor': 2,
            'max_floor': 2,
            'city': 'Алматы',
            'district': 'Турксибский',
            'general_area': 40,
            'condition': 'хорошее',
            'build_year': 1970,
        },
        'offer_description': {
            'internet': 'проводной',
            'parking': 'гараж',
            'floor_type': 'линолеум',
            'security': True,
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 40,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 25,
        },
    },


    # Shynar
    'https://krisha.kz/a/show/677715354': {  # 1
        'title_info': {
            'room_count': 2,
            'floor': 2,
            'general_area': 53,
            'max_floor': 5,
            'street': 'Халиуллина',
            'house_number': '196/1',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 2,
            'max_floor': 5,
            'city': 'Алматы',
            'district': 'Медеуский',
            'general_area': 53,
            'condition': 'хорошее',
            'residential_complex': 'Medeu City',
            'build_year': 2021,
        },
        'offer_description': {
            'bathroom': 'совмещенный',
            # 'balcony': 'несколько балконов или лоджий',
            # 'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'ADSL',
            'parking': 'паркинг',
            # 'furniture': 'полностью',
            'floor_type': 'ламинат',
            'ceiling_height': 2.8,
            # bools
            'security': True,
            # 'entry_phone': True,
            # 'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 53,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 15,
        },
    },
    'https://krisha.kz/a/show/674202944': {  # 2
        'title_info': {
            'room_count': 6,
            'floor': 13,
            'general_area': 188,
            'max_floor': 13,
            'street': 'Сейфуллина',
            'house_number': '499/131',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 13,
            'max_floor': 13,
            'city': 'Алматы',
            'district': 'Алмалинский',
            'general_area': 188,
            'condition': 'хорошее',
            'residential_complex': 'Бақытты өмір (Бакытты омир)',
            'build_year': 2017,
        },
        'offer_description': {
            # 'bathroom': 'совмещенный',
            'balcony': 'балкон',
            'is_balcony_glazed': True,
            'door': 'бронированная',
            'internet': 'оптика',
            'parking': 'рядом охраняемая стоянка',
            # 'furniture': 'полностью',
            'floor_type': 'паркет',
            'ceiling_height': 3.35,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 188,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 28,
        },
    },
    'https://krisha.kz/a/show/675689940': {  # 3
        'title_info': {
            'room_count': 5,
            'floor': 1,
            'general_area': 225,
            'max_floor': 9,
            'street': 'Аскарова Асанбая',
            'house_number': '21',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 1,
            'max_floor': 9,
            'city': 'Алматы',
            'district': 'Бостандыкский',
            'general_area': 225,
            # 'condition': 'хорошее',
            'residential_complex': 'Аль-Фараби',
            'build_year': 2015,
        },
        'offer_description': {
            # 'bathroom': 'совмещенный',
            'balcony': 'балкон',
            # 'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'ADSL',
            # 'parking': 'паркинг',
            # 'furniture': 'полностью',
            # 'floor_type': 'ламинат',
            'ceiling_height': 3,
            # bools
            'security': True,
            'entry_phone': True,
            # 'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Возможен обмен',
        },
        'others': {
            'living_area': 225,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 53,
        },
    },
    'https://krisha.kz/a/show/677954631': {  # 4
        'title_info': {
            'room_count': 2,
            'floor': 4,
            'general_area': 45.9,
            'max_floor': 4,
            'street': 'Жубанова',
            'house_number': '196/1',
        },
        'offer_short_description': {
            'building_type': 'панельный',
            'floor': 4,
            'max_floor': 4,
            'city': 'Алматы',
            'district': 'Ауэзовский',
            'general_area': 45.9,
            'condition': 'хорошее',
            # 'residential_complex': 'Medeu City',
            'build_year': 1971,
        },
        'offer_description': {
            'bathroom': 'раздельный',
            'balcony': 'балкон',
            'is_balcony_glazed': True,
            'parking': 'рядом охраняемая стоянка',
            # bools
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 45.9,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 14,
        },
    },
    # from page = 41
    'https://krisha.kz/a/show/675785580': {
        'title_info': {
            'room_count': 3,
            'floor': 2,
            'general_area': 70.5,
            'max_floor': 8,
            'street': 'Райымбека',
            'house_number': '508',
        },
        'offer_short_description': {
            'building_type': 'панельный',
            'floor': 2,
            'max_floor': 8,
            'city': 'Алматы',
            'district': 'Ауэзовский',
            'general_area': 70.5,
            'condition': 'хорошее',
            # 'residential_complex': None,
            'build_year': 1976,
        },
        'offer_description': {
            'bathroom': 'раздельный',
            'balcony': 'лоджия',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            # 'internet': None,
            'parking': 'паркинг',
            'furniture': 'частично',
            'floor_type': 'ламинат',
            'ceiling_height': 2.85,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            # 'exchange_possible': None,
        },
        'others': {
            'living_area': 70.5,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 10,
        }
    },
    # from page = 44
    'https://krisha.kz/a/show/677290787': {
        'title_info': {
            'room_count': 2,
            'floor': 9,
            'general_area': 52,
            'max_floor': 9,
            'street': 'Богенбай Батыра',
            'house_number': '23/3',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 9,
            'max_floor': 9,
            'city': 'Алматы',
            'district': 'Медеуский',
            'general_area': 52,
            # 'condition': None,
            'residential_complex': 'На Богенбай Батыра',
            'build_year': 2021,
        },
        'offer_description': {
            'bathroom': 'совмещенный',
            'balcony': 'несколько балконов или лоджий',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            # 'internet': None,
            'parking': 'паркинг',
            # 'furniture': None,
            # 'floor_type': None,
            'ceiling_height': 2.7,
            # bools
            # 'security': None,
            # 'entry_phone': None,
            # 'video_security': None,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 52,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 6,
        },



    },
    # from page = 50
    'https://krisha.kz/a/show/677577731': {
        'title_info': {
            'room_count': 3,
            'floor': 2,
            'general_area': 71.1,
            'max_floor': 9,
            'street': 'Алмалинский',
            'house_number': '167',
        },
        'offer_short_description': {
            'building_type': 'панельный',
            'floor': 2,
            'max_floor': 9,
            'city': 'Алматы',
            'district': 'Алмалинский',
            'general_area': 71.1,
            'condition': 'хорошее',
            # 'residential_complex': None,
            'build_year': 1988,
        },
        'offer_description': {
            'bathroom': 'раздельный',
            'balcony': 'лоджия',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            'internet': 'оптика',
            # 'parking': None,
            # 'furniture': None,
            'floor_type': 'ламинат',
            'ceiling_height': 2.8,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 71.1,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 22,
        },
    },
    # from page = 60
    'https://krisha.kz/a/show/679428912': {
        'title_info': {
            'room_count': 1,
            'floor': 4,
            'general_area': 40,
            'max_floor': 13,
            'street': 'Есенова',
            'house_number': '160/3',
        },
        'offer_short_description': {
            'building_type': 'монолитный',
            'floor': 4,
            'max_floor': 13,
            'city': 'Алматы',
            'district': 'Жетысуский',
            'general_area': 40,
            # 'condition': None,
            'residential_complex': 'Jetisu Park',
            'build_year': 2022,
        },
        'offer_description': {
            'bathroom': 'совмещенный',
            'balcony': 'балкон и лоджия',
            'is_balcony_glazed': True,
            'door': 'металлическая',
            # 'internet': None,
            'parking': 'паркинг',
            # 'furniture': None,
            # 'floor_type': None,
            'ceiling_height': 2.8,
            # bools
            'security': True,
            'entry_phone': True,
            'video_security': True,
            # oths
            'former_hostel': False,
            'exchange_possible': 'Не интересует',
        },
        'others': {
            'living_area': 40,
        },
        'others2': {
            # 'mortgaged': False,
            # 'mortgage': False,
            # 'installment': False,
            # 'private_hostel': False,
            'images_count': 3,
        },
    }
}

pats = {
    'street': r'(?P<street>[а-яА-Я0-9]{1,}(-й мкр)?(\s[а-яА-Я]+){0,})',
    'house_number': r' (?P<house_number>(\d)+(\/?\w*)*[а-яА-Я]*)',
    'microdistrict': r'мкр (?P<microdistrict>[а-яА-Я№0-9]{1,})',
    'intersection': r' — (?P<intersection>[а-яА-Я]{1,}(\s[а-яА-Я]+){0,})',
}

# Kaisar
patterns: dict[str, tuple[str, list[tuple[str, dict]]]] = {
    'city': (r"(?P<city>.+), (?P<district>.+) р-н", [
        ('Алматы, Наурызбайский р-н', {
            'city': 'Алматы',
            'district': 'Наурызбайский',
        })
    ]),
    'general_area': ((
        r"(?P<general_area>(\.?\d+)+) м²"
        r"(, жилая — (?P<living_area>(\.?\d+)+) м²)?"
        r"(, Площадь кухни — (?P<kitchen_area>(\.?\d+)+) м²)?"
    ), [
        ('159.4 м², Площадь кухни — 22 м²', {
            'general_area': '159.4',
            'kitchen_area': '22',
        }),
        ('51.8 м², жилая — 49.7 м², Площадь кухни — 9 м²', {
            'general_area': '51.8',
            'living_area': '49.7',
            'kitchen_area': '9',
        }),
    ]),
    'street': (pats['street'], [
        ('Кенесары хана', {
            'street': 'Кенесары хана'
        }),
        ('Мынбаева', {
            'street': 'Мынбаева'
        }),
        ('Мынбаева 47А', {
            'street': 'Мынбаева'
        }),
        ('12-й мкр 22/2', {
            'street': '12-й мкр'
        }),
    ]),
    'house_number': (pats['house_number'], [
        (' 54/39', {
            'house_number': '54/39'
        }),
        (' 47А', {
            'house_number': '47А'
        }),
    ]),
    'intersection': (pats['intersection'], [
        (' — Ауэзова', {
            'intersection': 'Ауэзова'
        }),
        (' — Кенесары хана', {
            'intersection': 'Кенесары хана'
        }),
        (' — Омарова', {
            'intersection': 'Омарова'
        }),
    ]),
    'microdistrict': (pats['microdistrict'], [
        ('мкр №12', {
            'microdistrict': '№12'
        }),
        ('мкр Кулагер', {
            'microdistrict': 'Кулагер'
        }),
        # (' — Кенесары хана', {
        #     'intersection': 'Кенесары хана'
        # }),
    ]),
    'title_info': ((
        r'(?P<room_count>\d+)-комнатная квартира' +
        r'(, (?P<general_area>\d+\.?\d+) м²)' +
        r'(, (?P<floor>\d+)/(?P<max_floor>\d+) этаж)?' +
        r'(, ' +
        pats['microdistrict'] +
        r')?' +
        r'(, ' +
        pats['street'] +
        r')?' +
        r'(' +
        pats['house_number'] +
        r')?' +
        r'(' +
        pats['intersection'] +
        r')?'
    ), [
        ('3-комнатная квартира, 90 м², 4/10 этаж, Кенесары хана 54/39',
         test_cases['https://krisha.kz//a/show/674680782']['title_info']),
        ('1-комнатная квартира, 35 м², 1/5 этаж, Мынбаева 47А — Ауэзова',
         test_cases['https://krisha.kz/a/show/679286505']['title_info']),
        ('3-комнатная квартира, 90 м², 4/9 этаж, мкр №12, 12-й мкр 22/2 — Шаляпина',
         test_cases['https://krisha.kz/a/show/27290921']['title_info']),
        ('2-комнатная квартира, 51.8 м², 4/5 этаж, мкр Кулагер, Мукатая Беспакова — Омарова',
         test_cases['https://krisha.kz/a/show/676253177']['title_info']),
        # ('1-комнатная квартира, 35 м², 1/5 этаж, Мынбаева 47А — Ауэзова',
        #  test_cases['https://krisha.kz/a/show/679286505']['title_info']
        #  )
    ])
}
