import sys
import time
import sqlite3


import rl_garage
import rl_insider

from datetime import datetime


# TODO timeout and other exceptions

path_to_chrome_driver = sys.argv[1]

connection = sqlite3.connect("database.db")
start_time = time.time()

url = "https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterMinCredits=0" \
      "&filterMaxCredits=100000&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=0 "
# url = "https://rocket-league.com/trades/DerMa_2007"
cursor = connection.cursor()
cursor.execute('PRAGMA FOREIGN_KEYS = ON')
# not a lot of results
# url = "https://rocket-league.com/trading?filterItem=1694&filterCertification=0&filterPaint=0&filterMinCredits=0&filterMaxCredits=100000&filterSearchType=1&filterItemType=0"

# prints all trades of n pages TODO integrate in class
# time should be defined prior to calling loag_n_pages because it takes forever
# cursor.execute('DELETE FROM rl_garage_trade')
# connection.commit()
for i in range(2):
    time_now = datetime.now()
    trade_list = rl_garage.eval_url_bs4(rl_garage.load_n_pages(url, 12, path_to_chrome_driver), time_now)
    rl_garage.insert_trade_list_into_database(connection, trade_list)

# scans rl.insider.gg for ALL item prices
# rl_insider_url = "https://rl.insider.gg/en/pc?mobile" # chrome
rl_insider_url = "https://rl.insider.gg/en/pc"  # firefox only wtf??

# TODO importanté
cursor.execute('DELETE FROM rl_insider_item')
connection.commit()
rl_insider.insert_all_into_database(connection, rl_insider_url)

connection.close()
print("--- %s seconds ---" % (time.time() - start_time))
