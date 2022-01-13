import alternate_functions as alternate
import mediamarkt_functions
import nbb_functions as nbb
import mediamarkt_functions as mdm
import chat_functions as chat
import caseking_functions as ck
import proxy_functions as proxy
import jacob_functions as jacob


#vars
import utility_functions

type = 0
price = 1
fullname = 2
link = 3

cards = [
    "GTX 1650",
    "GTX 1660",
    "RTX 2060",
    "RTX 2070",
    "RTX 2080",
    "RTX 3060",
    "RTX 3060 Ti",
    "RTX 3070",
    "RTX 3070 Ti",
    "RTX 3080",
    "RTX 3080 Ti",
    "RTX 3090",
    "RX 6600",
    "RX 6600 XT",
    "RX 6700",
    "RX 6700 XT",
    "RX 6800",
    "RX 6800 XT",
    "RX 6900",
    "RX 6900 XT"
]
'''
alternate.find_card(cards)
ck.find_card(cards)
mdm.find_card(cards)
'''

#chat.send_deal("kleiner Tipp", 501.32, 'Grafikkarten Drop im AMD Shop um 16:05', 'https://www.amd.com/de/direct-buy/de', 'AMD Shop', 2)

#fill up links
#nbb.find_card(cards)
#alternate.find_card(cards)

## experimental feature
try:
    mediamarkt_functions.find_card(cards)
except:
    pass

## experimental feature
try:
    mediamarkt_functions.find_card(cards)
except:
    pass

#update deals

#jacob.check_prices(cards) #checks prices for all cards, so the file only has to be downloaded once

for card_type in cards:
    print(card_type)
    #nbb.check_price(card_type)
    #alternate.check_price(card_type)

    ## experimental feature
    try:
        mediamarkt_functions.check_price(card_type)
    except:
        pass

    ## experimental feature
    try:
        mediamarkt_functions.check_price(card_type)
    except:
        pass

    #finshing touches
    utility_functions.mysql_update_deals(card_type)
    chat.check_and_send_deal(card_type)