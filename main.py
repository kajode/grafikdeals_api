import alternate_functions as alternate
import nbb_functions as nbb
import mediamarkt_functions as mdm
import chat_functions as chat
import caseking_functions as ck
import proxy_functions as proxy
import datetime


#vars
import utility_functions

type = 0
price = 1
fullname = 2
link = 3
timestamp = datetime.datetime.now()

cards = [
    ["RTX 2060", 500],
    ["RTX 2070", 600],
    ["RTX 2080", 1000],
    ["RTX 3060", 600],
    ["RTX 3060 Ti", 650],
    ["RTX 3070", 700],
    ["RTX 3070 Ti", 800],
    ["RTX 3080", 1000],
    ["RTX 3080 Ti", 1300],
    ["RTX 3090", 1500],
    ["RX 6600", 500],
    ["RX 6600 XT", 500],
    ["RX 6700", 700],
    ["RX 6700 XT", 700],
    ["RX 6800", 900],
    ["RX 6800 XT", 900],
    ["RX 6900", 1100],
    ["RX 6900 XT", 1100]
]
'''
ck.find_card(cards)
alternate.find_card(cards)
nbb.find_card(cards)
mdm.find_card(cards)
'''
alternate.find_card(cards)


for card in cards:
    chat.check_and_send_deal(card[0])

    alternate.check_price(card)
    mdm.check_price(card)
    ck.check_price(card)

# get best new price an save them in deals table
utility_functions.mysql_update_deals(timestamp)
