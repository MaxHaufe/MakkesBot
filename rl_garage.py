import re

from bs4 import BeautifulSoup
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

import Trade
import Item_rl_Garage


def load_n_pages(url, n, path_to_chrome_driver):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(path_to_chrome_driver, options=chrome_options)
    # driver = webdriver.Chrome("/home/max/PycharmProjects/chromedriver")
    driver.get(url)
    # accept privacy policy
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, 'acceptPrivacyPolicy'))).click()
    # accept privacy policy again (wtf)
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, 'css-1tbbj19'))).click()

    for i in range(n):
        print("\rLoading Page " + str(i) + "/" + str(n), end="")
        try:
            WebDriverWait(driver, 20).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'rlg-btn-primary.rlg-btn-primary-pink'))).click()
        except TimeoutException:
            print("")
            print('\033[91m' + "Timeout, not all pages of rl_garage could be loaded, returning." + '\033[0m')
            return driver.page_source
    print("")
    return driver.page_source


# rl garage
def eval_url_bs4(content, time_now):
    soup = BeautifulSoup(content, 'html.parser')
    trades_html = soup.find_all('div', class_='rlg-trade')  # list of all trades
    idx = 0  # so idx can not be undefined
    trade_list = []
    for idx, trade in enumerate(trades_html):

        # Find all the single item tags for each trade
        has_item_html = trade.find('div', class_='rlg-trade__itemshas').find_all("a", class_='rlg-item')
        wants_item_html = trade.find('div', class_='rlg-trade__itemswants').find_all("a", class_='rlg-item')

        # if item wants are unequal to item hast => skip to next trade, runtime efficiency
        if len(has_item_html) != len(wants_item_html):
            continue

        # print("------------------------------------------------------------")
        rlg_name = trade.find('div', class_='rlg-trade__username').text.replace("\n", "")
        platform_details = trade.find('div', class_='rlg-trade__platformname').find_all('span')
        platform_name = platform_details[0].text
        platform_username = platform_details[1].text

        if platform_name == "Add on Steam":
            platform_name = "Steam"
            platform_link = trade.find('div', class_='rlg-trade__platforms').find('a')['href']
        else:
            platform_link = None

        # <span> 8 days ago </span>
        # <span> 1 week, 23 hours, 48 minutes, 40 seconds ago </span>
        # => take the second element
        trade_time_html = trade.find('span', class_='rlg-trade__time').find_all('span')
        trade_time_text = trade_time_html[1].text
        trade_time = parse_rlg_trade_time(trade_time_text, time_now)

        if trade.find('div', class_='rlg-trade__note') is None:
            trade_note = None
        else:
            trade_note = trade.find('div', class_='rlg-trade__note').text

        # print(platform_name)
        # print(rlg_name)
        # print(platform_link)
        # print(trade_time)
        # print(trade_note)
        # print("")

        items_wants_list = []
        items_has_list = []
        # for each item get name, color, amount
        for has, wants in zip(has_item_html, wants_item_html):
            # items offered
            has_item = get_item_from_trade(has)
            # items wanted
            wants_item = get_item_from_trade(wants)

            items_has_list.append(has_item)
            items_wants_list.append(wants_item)

        trade_list.append(Trade.Trade(rlg_name, platform_name, platform_username, platform_link,
                                      items_has_list, items_wants_list, trade_time, trade_note))
        print("\rEvaluating Trade " + str(idx) + "/" + str(len(trades_html)), end="")

        # print("\n\nCount: " + str(idx))
        print("")
    return trade_list


def get_item_from_trade(html):
    # name
    # make RLCS X (Octane) to  RLCS X [Octane] <= for RL insider
    item_name = html.find('h2', class_='rlg-item__name').text.replace("(", "[").replace(")", "]")
    item_rarity = html['class'][1].replace("-", "")
    # color
    try:
        # it's always \n item color
        item_color = html.find('div', class_='rlg-item__paint').text.replace(
            "\n",
            "").rstrip()
    except AttributeError:
        item_color = "Unpainted"
    # quantity
    try:
        item_quantity = int(html.find('div', class_='rlg-item__quantity').text)
    except AttributeError:
        item_quantity = 1
    return Item_rl_Garage.Item_rl_Garage(item_name, item_quantity, item_rarity, item_color)


def parse_rlg_trade_time(date_in_text_form, time_now):
    m_weeks = re.search(r"(?P<weeks>[0-9]*) week", date_in_text_form)
    m_days = re.search(r"(?P<days>[0-9]*) day", date_in_text_form)
    m_hours = re.search(r"(?P<hours>[0-9]*) hour", date_in_text_form)
    m_minutes = re.search(r"(?P<minutes>[0-9]*) minute", date_in_text_form)
    m_seconds = re.search(r"(?P<seconds>[0-9]*) second", date_in_text_form)

    # checking is more efficient in this case
    if m_weeks is None:
        weeks = 0
    else:
        weeks = int(m_weeks.group('weeks'))

    if m_days is None:
        days = 0
    else:
        days = int(m_days.group('days'))

    if m_hours is None:
        hours = 0
    else:
        hours = int(m_hours.group('hours'))

    if m_minutes is None:
        minutes = 0
    else:
        minutes = int(m_minutes.group('minutes'))

    if m_seconds is None:
        seconds = 0
    else:
        seconds = int(m_seconds.group('seconds'))

    return time_now - timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)


def insert_trade_list_into_database(connection, trade_list):
    print("Inserting Trades into Database")
    cursor = connection.cursor()
    for idx,trade in enumerate(trade_list):
        insert_trade_list = [
            trade.rlg_name,
            trade.platform,
            trade.platform_username,
            trade.platform_link,
            trade.time,
            trade.note
        ]

        cursor.execute(
            'INSERT INTO rl_garage_trade (rlg_name, platform, platform_username, platform_link, time, note) VALUES ('
            '?,?,?,?,?,?)', insert_trade_list
        )

        trade_id = cursor.lastrowid
        print("\rInserting Trade " + str(idx) + "/" + str(len(trade_list)), end="")

        for has_item, wants_item in zip(trade.has_item_list, trade.wants_item_list):
            insert_content_list = [
                trade_id,

                has_item.item_name,
                has_item.item_quantity,
                has_item.item_rarity,
                has_item.item_color,

                wants_item.item_name,
                wants_item.item_quantity,
                wants_item.item_rarity,
                wants_item.item_color
            ]

            cursor.execute('INSERT INTO rl_garage_trade_contents (trade_id, has_item_name, has_item_quantity, '
                           'has_item_rarity, has_item_color, wants_item_name, wants_item_quantity, wants_item_rarity, '
                           'wants_item_color) VALUES (?,?,?,?,?,?,?,?,?)', insert_content_list)
    print("")
    connection.commit()
