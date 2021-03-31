import sys
import time
import sqlite3
from joblib import Parallel, delayed

import rl_garage
import rl_insider

from datetime import datetime

# TODO timeout and other exceptions

connection = sqlite3.connect("database.db")
start_time = time.time()

# url = "https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=0&filterMaxCredits=100000&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=0"
url_flags = "?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=1500&filterMaxCredits=3000&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=0"

# url = "https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=0" \
#       "&filterMaxCredits=100000&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=0 "
# url = "https://rocket-league.com/trades/DerMa_2007"

cursor = connection.cursor()
cursor.execute('PRAGMA FOREIGN_KEYS = ON')

# cursor.execute('DELETE FROM rl_garage_trade')
# connection.commit()
start_time = time.time()

rl_garage.parse_n_pages(url_flags, 10000, connection)
# trade_list = rl_garage.eval_url_bs4(
#     rl_garage.parse_n_pages(url_flags, 1), time_now)
# rl_garage.insert_trade_list_into_database(connection, trade_list)
# print("--- %s seconds ---" % (time.time() - start_time))

# rl_insider_url = "https://rl.insider.gg/en/pc?mobile" # chrome
rl_insider_url = "https://rl.insider.gg/en/pc"  # firefox only wtf??

# TODO importanté
# cursor.execute('DELETE FROM rl_insider_item')
# connection.commit()
# rl_insider.insert_all_into_database(connection, rl_insider_url)

connection.close()
# print("--- %s seconds ---" % (time.time() - start_time))
