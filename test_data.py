from my_types import TTestcase
building_types = ['монолитный', 'кирпичный', 'панельный', 'иное']


# Arailym
test_cases: dict[str, TTestcase] = {
    'https://krisha.kz//a/show/674680782': {
        'title_info': {
            'room_count': 3,
            'floor': 4,
            'area': 90,
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
            'living_area': 90,
        },
        'others2': {
            'mortgaged': False,
            'mortgage': False,
            'installment': False,
            'private_hostel': False,
            'images_count': 22,
        },
    },
    'https://krisha.kz/a/show/679286505': {
        'title_info': {
            'room_count': 1,
            'area': 35,
            'floor': 1,
            'max_floor': 5,
            'street': 'Мынбаева',
            'house_number': '47А',
            'intersection': 'Ауэзова',
        },
        'offer_short_description': {

        },
        'offer_description': {

        },
        'others': {

        },
        'others2': {

        },
    },
    'https://krisha.kz/a/show/27290921': {
        'title_info': {
            'room_count': 3,
            'area': 90,
            'floor': 4,
            'max_floor': 9,
            'microdistrict': '№12',
            'street': '12-й мкр',
            'house_number': '22/2',
            'intersection': 'Шаляпина',
        },
        'offer_short_description': {

        },
        'offer_description': {

        },
        'others': {

        },
        'others2': {

        },
    },
    'https://krisha.kz/a/show/676253177': {
        'title_info': {
            'room_count': 2,
            'area': 51.8,
            'floor': 4,
            'max_floor': 5,
            'microdistrict': 'Кулагер',
            'street': 'Мукатая Беспакова',
            'house_number': None,
            'intersection': 'Омарова',
        },
        'offer_short_description': {

        },
        'offer_description': {

        },
        'others': {

        },
        'others2': {

        },
    },
}

pats = {
    'street': r'(?P<street>[а-яА-Я]{1,}(\s[а-яА-Я]+){0,})',
    'house_number': r'(?P<house_number>(\d)+(\/?\w*)*)',
    'microdistrict': r'(?P<microdistrict>\w+(-\d+)?)',
    'intersection': r' — (?P<intersection>[а-яА-Я]{1,}(\s[а-яА-Я]+){0,})',
}

# Kaisar
patterns: dict[str, tuple[str, list[tuple[str, dict]]]] = {
    # 'city': (r"(?P<city>.+), (?P<district>.+) р-н", [
    #     ('Алматы, Наурызбайский р-н', {
    #         'city': 'Алматы',
    #         'district': 'Наурызбайский',
    #     })
    # ]),
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
    ]),
    'house_number': (pats['house_number'], [
        ('54/39', {
            'house_number': '54/39'
        }),
        ('47А', {
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
    ]),
    'title_info': ((
        r'(?P<room_count>\d+)-комнатная квартира' +
        r'(, (?P<area>\d+\.?\d+) м²)' +
        r'(, (?P<floor>\d+)/(?P<max_floor>\d+) этаж)?' +
        # r'(, мкр ' +
        # pats['microdistrict'] +
        # r')?' +
        r'(, ' +
        pats['street'] +
        r')? ' +
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
