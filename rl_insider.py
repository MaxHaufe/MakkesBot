import re
import Item_rl_Insider
from bs4 import BeautifulSoup
import requests


def get_item_price_list(soup, container_name, is_paintable):
    table = soup.find(id=container_name).find_all('tr', class_='itemRow')
    item_list = []
    for row in table:
        # check for empty item rows
        if row.find('div', class_='itemNameSpan'):
            name = row.find('div', class_='itemNameSpan').text
            url_name = row['data-itemurl']
            rarity = row['data-itemrarity'].replace("|", "").lower()
            type_ = row['data-itemtype'].lower()

            default_price_range = parse_item_price(row, 'priceDefault priceRange')

            if is_paintable:
                black_price_range = parse_item_price(row, 'priceBlack priceRange')
                white_price_range = parse_item_price(row, 'priceWhite priceRange')
                grey_price_range = parse_item_price(row, 'priceGrey priceRange')
                crimson_price_range = parse_item_price(row, 'priceCrimson priceRange')
                pink_price_range = parse_item_price(row, 'pricePink priceRange')
                cobalt_price_range = parse_item_price(row, 'priceCobalt priceRange')
                sky_blue_price_range = parse_item_price(row, 'priceSkyBlue priceRange')
                burnt_sienna_price_range = parse_item_price(row, 'priceBurntSienna priceRange')
                saffron_price_range = parse_item_price(row, 'priceSaffron priceRange')
                lime_price_range = parse_item_price(row, 'priceLime priceRange')
                forest_green_price_range = parse_item_price(row, 'priceForestGreen priceRange')
                orange_price_range = parse_item_price(row, 'priceOrange priceRange')
                purple_price_range = parse_item_price(row, 'pricePurple priceRange')
            else:
                black_price_range = [None, None]
                white_price_range = [None, None]
                grey_price_range = [None, None]
                crimson_price_range = [None, None]
                pink_price_range = [None, None]
                cobalt_price_range = [None, None]
                sky_blue_price_range = [None, None]
                burnt_sienna_price_range = [None, None]
                saffron_price_range = [None, None]
                lime_price_range = [None, None]
                forest_green_price_range = [None, None]
                orange_price_range = [None, None]
                purple_price_range = [None, None]

            price_list = [default_price_range, black_price_range, white_price_range, grey_price_range,
                          crimson_price_range, pink_price_range, cobalt_price_range, sky_blue_price_range,
                          burnt_sienna_price_range, saffron_price_range, lime_price_range, forest_green_price_range,
                          orange_price_range, purple_price_range]

            item_list.append(Item_rl_Insider.Item_rl_Insider(name, url_name, rarity, type_, is_paintable, price_list))

            # print("----------------------------------------------")
            # print(name)
            # print(url_name)
            # print(rarity)
            # print(type_)
            # print("[" + str(white_price_range[0]) + ", " + str(white_price_range[1]) + "]")
            #
            # print(default_price_range)
    return item_list


# returns list of two elements - [low, high] or [-1, -1] in case of unavailable or [None,None] in case of undefined
def parse_item_price(row, class_name):
    # if price not available, return -1
    try:
        html_price_dump = row.find('td', class_=class_name)['data-info']
    except TypeError:
        return [-1, -1]

    # regex
    # technically available but undefined
    m = re.search(r"\"pc\":\[((?P<value_low>[0-9]*),(?P<value_high>[0-9]*)])", html_price_dump)
    try:
        return [m.group('value_low'), m.group('value_high')]
    except AttributeError:
        return [None, None]


# ögly code
# def insert_item_into_database(connection, item_list):
#     cursor = connection.cursor()
#     for item in item_list:
#         insert_list = [
#             item.name,
#             item.url_name,
#             item.rarity,
#             item.type,
#             item.is_paintable,
#             # default
#             item.price_list[0][0],
#             item.price_list[0][1],
#             # black
#             item.price_list[1][0],
#             item.price_list[1][1],
#             # white
#             item.price_list[2][0],
#             item.price_list[2][1],
#             # grey
#             item.price_list[3][0],
#             item.price_list[3][1],
#             # crimson
#             item.price_list[4][0],
#             item.price_list[4][1],
#             # pink
#             item.price_list[5][0],
#             item.price_list[5][1],
#             # cobalt
#             item.price_list[6][0],
#             item.price_list[6][1],
#             # sky blue
#             item.price_list[7][0],
#             item.price_list[7][1],
#             # sienna
#             item.price_list[8][0],
#             item.price_list[8][1],
#             # saffron
#             item.price_list[9][0],
#             item.price_list[9][1],
#             # lime
#             item.price_list[10][0],
#             item.price_list[10][1],
#             # forest green
#             item.price_list[11][0],
#             item.price_list[11][1],
#             # orange
#             item.price_list[12][0],
#             item.price_list[12][1],
#             # purple
#             item.price_list[13][0],
#             item.price_list[13][1]
#         ]
#
#         cursor.execute(
#             'INSERT INTO rl_insider VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
#             insert_list)
#
#         item_id = cursor.lastrowid
#
#         connection.commit()

def get_color_from_index(index):
    color_list = [
        "Unpainted",
        "Black",
        "Titanium White",
        "Grey",
        "Crimson",
        "Pink",
        "Cobalt",
        "Sky Blue",
        "Burnt Sienna",
        "Saffron",
        "Lime",
        "Forest Green",
        "Orange",
        "Purple"
    ]
    return color_list[index]


def insert_item_list_into_database(connection, item_list):
    cursor = connection.cursor()
    for item in item_list:
        insert_item_list = [
            item.name,
            item.url_name,
            item.rarity,
            item.type,
            item.is_paintable
        ]

        cursor.execute(
            'INSERT INTO rl_insider_item (item_name, item_url_name, item_rarity, item_type, item_is_paintable) VALUES '
            '(?,?,?,?,?)',
            insert_item_list)
        # rowid serves as PK in rl_insider_item
        item_id = cursor.lastrowid

        for idx, price_range in enumerate(item.price_list):
            # if price not available => skip
            if price_range[0] == -1:
                continue
            # if not paintable, only write default price to database
            if item.is_paintable is False and idx == 1:
                break


            item_color = get_color_from_index(idx)
            insert_price_list = [
                item_id,
                item_color,
                price_range[0],  # low
                price_range[1]   # high
            ]
            cursor.execute(
                'INSERT INTO rl_insider_prices (item_id, item_color, item_price_low, item_price_high) VALUES (?,?,?,?)',
                insert_price_list)

    connection.commit()


def insert_all_into_database(connection, url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    painted_BM_decals_list = get_item_price_list(soup, 'paintedBMDecalsPricesContainer', True)
    unpainted_BM_decals_list = get_item_price_list(soup, 'unpaintedBMDecalsPrices', False)
    painted_goal_explosions_list = get_item_price_list(soup, 'paintedGoalExplosionsPricesContainer', True)
    painted_cars_list = get_item_price_list(soup, 'paintedCarsPricesContainer', True)
    painted_EXOTIC_wheels_list = get_item_price_list(soup, 'paintedWheelsExoticPricesContainer', True)
    painted_LIMITED_wheels_list = get_item_price_list(soup, 'paintedWheelsLimitedPricesContainer', True)
    painted_IMPORT_wheels_list = get_item_price_list(soup, 'paintedWheelsImportPricesContainer', True)
    painted_VERY_RARE_wheels_list = get_item_price_list(soup, 'paintedWheelsVeryRarePricesContainer', True)
    painted_RARE_wheels_list = get_item_price_list(soup, 'paintedWheelsRarePricesContainer', True)
    painted_UNCOMMON_wheels_list = get_item_price_list(soup, 'paintedWheelsUncommonPricesContainer', True)
    painted_decals_list = get_item_price_list(soup, 'paintedDecalsPricesContainer', True)
    painted_boosts_list = get_item_price_list(soup, 'paintedBoostsPricesContainer', True)
    painted_toppers_list = get_item_price_list(soup, 'paintedToppersPricesContainer', True)
    painted_antennas_list = get_item_price_list(soup, 'paintedAntennasPricesContainer', True)
    painted_trails_list = get_item_price_list(soup, 'paintedTrailsPricesContainer', True)
    painted_banners_list = get_item_price_list(soup, 'paintedBannersPricesContainer', True)
    painted_avatar_borders_list = get_item_price_list(soup, 'paintedAvatarBordersPricesContainer', True)
    unpainted_alpha_beta_items_list = get_item_price_list(soup, 'alpha+BetaPricesContainer', False)
    unpainted_goal_explosions_list = get_item_price_list(soup, 'unpaintedGoalExplosionsPricesContainer',
                                                         False)
    unpainted_cars_list = get_item_price_list(soup, 'unpaintedCarsPricesContainer', False)
    unpainted_wheels_list = get_item_price_list(soup, 'unpaintedWheelsPricesContainer', False)
    unpainted_decals_list = get_item_price_list(soup, 'unpaintedDecalsPricesContainer', False)
    unpainted_boost_list = get_item_price_list(soup, 'unpaintedBoostsPricesContainer', False)
    unpainted_toppers_list = get_item_price_list(soup, 'unpaintedToppersPricesContainer', False)
    unpainted_antennas_list = get_item_price_list(soup, 'unpaintedAntennasPricesContainer', False)
    unpainted_trails_list = get_item_price_list(soup, 'unpaintedTrailsPricesContainer', False)
    unpainted_banners_list = get_item_price_list(soup, 'unpaintedBannersPricesContainer', False)
    unpainted_avatar_borders_list = get_item_price_list(soup, 'unpaintedAvatarBordersPricesContainer', False)
    unpainted_engine_audios_list = get_item_price_list(soup, 'engineAudioPricesContainer', False)
    unpainted_gift_packs_list = get_item_price_list(soup, 'giftPacksPricesContainer', False)
    unpainted_paint_finishes_list = get_item_price_list(soup, 'paintFinishesPricesContainer', False)

    complete_list = [
        painted_BM_decals_list,
        unpainted_BM_decals_list,
        painted_goal_explosions_list,
        painted_cars_list,
        painted_EXOTIC_wheels_list,
        painted_LIMITED_wheels_list,
        painted_IMPORT_wheels_list,
        painted_VERY_RARE_wheels_list,
        painted_RARE_wheels_list,
        painted_UNCOMMON_wheels_list,
        painted_decals_list,
        painted_boosts_list,
        painted_toppers_list,
        painted_antennas_list,
        painted_trails_list,
        painted_banners_list,
        painted_avatar_borders_list,
        unpainted_alpha_beta_items_list,
        unpainted_goal_explosions_list,
        unpainted_cars_list,
        unpainted_wheels_list,
        unpainted_decals_list,
        unpainted_boost_list,
        unpainted_toppers_list,
        unpainted_antennas_list,
        unpainted_trails_list,
        unpainted_banners_list,
        unpainted_avatar_borders_list,
        unpainted_engine_audios_list,
        unpainted_gift_packs_list,
        unpainted_paint_finishes_list
    ]
    for item_list in complete_list:
        insert_item_list_into_database(connection, item_list)
