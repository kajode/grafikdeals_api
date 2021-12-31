import logging
import telegram
import utility_functions as ut
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

token = '5037194249:AAHfgCGQ9D2mu2TxqoXcNNgJK2DUex4AgKU'
chatID = -1001777891004

def send(message):
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    bot = telegram.Bot(token=token)
    #bot.send_message(text=message, chat_id=chatID, parse_mode = telegram.ParseMode.MARKDOWN_V2)

def send_deal(card_type, price, card_fullname, link, shop_name):

    link = ut.create_reflink(link)
    text='''
-------- *%s* --------
%s                  
                    
für *%.2f€*         
%s                 
--------------------------
'''% (card_type, card_fullname, price, link)

    ## fix reserved character issue with markdown
    text = text.replace('.', '\.').replace('-', '\-').replace('+', '\+').replace('=', '\=').replace('<', '\<').replace('>', '\>').replace('(', '\(').replace(')','\)').replace('_','\c')

    print(text)

    send(text)

def send_deals(deals):
    for deal in deals:
           send_deal(deal[0], deal[1], deal[2], deal[3], deal[4])
    return 0