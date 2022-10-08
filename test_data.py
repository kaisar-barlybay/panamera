from my_types import TTestcase
building_types = ['монолитный', 'кирпичный', 'панельный', 'иное']

patterns: dict[str, tuple[str, list[tuple[str, dict]]]] = {
    'city': (r"(?P<city>.+), (?P<district>.+) р-н", [
        ('Алматы, Наурызбайский р-н', {
            'city': 'Алматы',
            'district': 'Наурызбайский',
        })
    ]),
    'title': ((
        # r'(?P<room_count>\d+)-комнатная квартира'
        r'(, (?P<area>\d+\.?\d+) м²)'
        r'(, (?P<floor>\d+)/(?P<max_floor>\d+) этаж)?'
        r'(, мкр (?P<neighborhood>\w+(-\d+)?))?'
        r'(,(?P<street>(\w+\s?)+))? '
        r'( (?P<house_number>\d+(\w+)?(/)?(\s\w+)?(\d+)?))?'
        r'( — (?P<intersection>.*))?'
    ), [
        ('3-комнатная квартира, 90 м², 4/10 этаж, Кенесары хана 54/39', {
            'room_count': '3',
            'area': '90',
            'floor': '4',
            'max_floor': '10',
            'street': 'Кенесары хана',
            'house_number': '54/39',
        })
    ])
}


test_cases: dict[str, TTestcase] = {
    'https://krisha.kz//a/show/674680782': {
        'title_info': {
            'room_count': (4, 'equal'),
            'general_area': (90, 'equal'),
            'floor': (4, 'equal'),
            'max_floor': (10, 'equal'),
            'street': ('Кенесары хана', 'equal'),
            'house_number': ('54/39', 'equal'),
            # 'intersection': ('Розыбакиева', 'equal'),
        },
        'offer_short_description': {
            'building_type': ('монолитный', 'equal'),
            'floor': (4, 'equal'),
            'max_floor': (10, 'equal'),
            'city': ('Алматы', 'equal'),
            'district': ('Наурызбайский', 'equal'),
            'general_area': (90, 'equal'),
            'condition': ('хорошее', 'equal'),
            'residential_complex': ('Хан Тенгри', 'equal'),
            'build_year': (2013, 'equal'),
        },
        'offer_description': {
            'bathroom': ('раздельный', 'equal'),
            'balcony': ('несколько балконов или лоджий', 'equal'),
            'is_balcony_glazed': (True, 'equal'),
            'door': ('металлическая', 'equal'),
            'internet': ('оптика', 'equal'),
            'parking': ('паркинг', 'equal'),
            'furniture': ('полностью', 'equal'),
            'floor_type': ('ламинат', 'equal'),
            'ceiling_height': (2.9, 'equal'),
            # bools
            'security': (True, 'equal'),
            'entry_phone': (True, 'equal'),
            'video_security': (True, 'equal'),
            # oths
            'former_hostel': (False, 'equal'),
            'exchange_possible': ('Не интересует', 'equal'),
        },
        'others': {
            'living_area': (90, 'equal'),
        },
        'others2': {
            'mortgaged': (False, 'equal'),
            'mortgage': (False, 'equal'),
            'installment': (False, 'equal'),
            'private_hostel': (False, 'equal'),
            'images_count': (22, 'equal'),
        },
    },
    # 'https://krisha.kz/a/show/665531675': {
    #     'general_area': (148, 'equal'),
    #     'kitchen_area': (24.7, 'equal'),
    #     'mortgage': (True, 'equal'),
    #     'installment': (True, 'equal'),
    #     'private_hostel': (False, 'equal'),
    #     'residential_complex': ('Lafayette', 'equal'),
    #     'street': ('Сейдимбека', 'equal'),
    #     'house_number': ('110/1', 'equal'),
    # },
    # 'https://krisha.kz/a/show/673950872': {
    #     'private_hostel': (True, 'equal'),
    #     'neighborhood': ('Аксай-3', 'equal'),
    #     'house_number': ('10 А', 'equal'),
    #     'intersection': ('Толе би', 'equal'),
    #
    #     'bars_on_the_window': (True, 'equal'),
    #
    #     'plastic_windows': (True, 'equal'),
    #     'non_angular': (True, 'equal'),
    #     'quiet_courtyard': (True, 'equal'),
    # },
    # 'https://krisha.kz/a/show/673740963': {
    #
    #
    #
    #
    #
    #
    #
    #
    #     'entry_phone': (True, 'equal'),
    # },
    # 'https://krisha.kz//a/show/672226546': {
    #     'ceiling_height': (3, 'equal'),
    # },
    # 'https://krisha.kz//a/show/673410125': {
    # },
}
