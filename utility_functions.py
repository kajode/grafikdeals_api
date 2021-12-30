import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as bs
from mechanize import Browser
import re
from selenium_stealth import stealth
import mysql.connector
from enum import Enum

advertiser_list = {'alternate.de': 11731, 'notebooksbilliger.de': 11348}
publisher_id = 997083

def shop_get_fullname(shop):
    if shop == 'mdm' or shop == 'mediamarkt':
        return 'Media Markt'
    if shop == 'nbb':
        return 'Notebooksbilliger'
    if shop == 'alternate':
        return 'Alternate'
    if shop == 'caseking':
        return 'Caseking'


# connect to database
mydb = mysql.connector.connect(
    host="grafikdeals.de",
    user="graka_user",
    password="SasaHGSDhgshd2371283",
    database="laravel_db"
)


def add_link(shop_name, type, link):

    file_name = shop_name +'_'+ type.replace(' ', '_')
    path = shop_name + '/' + file_name
    # create file if it doesnt exist
    if not os.path.exists(path):
        open(path, "x")

    file = open(path, "r")
    for line in file:
        if line.replace('\n', '') == link:
            return 0
    file.close()

    file = open(path, "a")
    file.write(link+'\n')
    file.close()
    return 1

def read_links(shop_name, type):

    file_name = shop_name + '_' + type.replace(' ', '_')
    path = shop_name + '/' + file_name

    #return error if file doesnt exist
    if not os.path.exists(path):
        open(path, "x")
        return []

    file = open(path, "r")
    links = file.readlines()

    return links


# TODO: Implement clear cache
def get_html(link):  ##opens website and returns html code
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = Options()
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('--lang=de')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f'user-agent={user_agent}')


    browser = webdriver.Chrome(chrome_options=options)
    stealth(browser,
            languages=["de-de", "de"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    browser.get(link)

    ##wait for page to load and read it
    html = browser.page_source
    browser.delete_all_cookies()
    browser.close()


    return html

def get_soup(link):
    return bs(get_html(link), 'html.parser')

def get_html_fast(link):
    short_link = re.findall("^https://.*\..{2,3}/", link)[0]
    b = Browser()
    b.set_handle_robots(False)
    b.set_handle_referer(True)
    b.set_handle_refresh(True)
    b.addheaders = [
        ('Referer', short_link),
        ('sec-fetch-dest', 'empty'),
        ('accept-language', 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'),
        ('sec-fetch-site', 'cross-site'),
        ('sec-fetch-mode', 'cors'),
        ('accept', '*/*'),
        ('origin', short_link),
        ('sec-ch-ua-platform','"macOS"'),
        ('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'),
        ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'),
    ]
    if 'notebooksbilliger.de' in link:
        b.addheaders.append(('authority', 'async-px-eu.dynamicyield.com'))
    b.open(link)

     #assert

    html = b.response().read()

    return html

def get_soup_fast(link):
    return bs(get_html_fast(link), 'html.parser')

def write_price(card_type, card_price):
    path = 'price_history/'+card_type.replace(' ', '_')

    # create file if it doesnt exist
    if not os.path.exists(path):
        open(path, "x")

    file = open(path, 'a')
    content = str(card_price) + '|' + str(time.time()) + '\n'
    file.write(content)
    file.close()

def read_prices(card_type):
    path = 'price_history/' + card_type.replace(' ', '_')

    # skip file if it doesnt exist
    if not os.path.exists(path):
        return -1

    file = open(path, 'r')
    prices = file.readlines()
    file.close()

    return prices

def read_weekly_average(card_type):
    prices = read_prices(card_type)

    #ensure file exists
    if prices == -1:
        return -1

    total_price = 0
    divider = 0
    for raw_price in prices:
        raw_price = raw_price.split('|')
        price = float(raw_price[0])
        date = float(raw_price[1])

        #make sure data is not older than a week
        if time.time() - date > 60*60*24*7:
            continue

        total_price += price
        divider += 1
    try:
        div  = total_price / divider
        return div
    except:
        return 0


def mysql_dropall():

    mycursor = mydb.cursor()

    sql = "DELETE FROM deals WHERE card_type='*'"

    mycursor.execute(sql)

    mydb.commit()

    print(mycursor.rowcount, "record(s) deleted")

def mysql_update(card_type, card_price, link, shop):

    card_price = float(card_price)

    mycursor = mydb.cursor()

    sql = "SELECT * FROM deals WHERE card_type='%s'" % card_type
    mycursor.execute(sql)
    myresult = mycursor.fetchall()


    if len(myresult) == 0:
        # add row if it doesnt exist
        sql = "INSERT INTO deals (card_type, price, link, shop) VALUES ('%s', '%s', '%s', '%s')" % (card_type, card_price, link, shop_get_fullname(shop))
    else:
        #update the card
        sql = "UPDATE deals SET price = '%.2f', shop = '%s', link = '%s' WHERE card_type = '%s'" % (card_price, shop_get_fullname(shop), link, card_type)

    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"card(s) updated or added")
 
def mysql_add(card_type, card_price, link, shop):

    card_price = float(card_price)

    mycursor = mydb.cursor()

    # add row if it doesnt exist
    sql = "INSERT INTO grafikkarten (name, price, link, shop) VALUES ('%s', '%s', '%s', '%s')" % (card_type, card_price, link, shop_get_fullname(shop))

    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount,"card(s) added")


def create_reflink(link):
    vendor_link = re.findall("^https://.*\..{2,3}/", link)[0].replace('https://', '').replace('/', '').replace('www.','')

    #check if vendor is supported otherwise just use link
    try:
        advertiser_id = advertiser_list[vendor_link]
        publisher_id = 997083
    except:
        return link

    ##turn ids into string
    advertiser_id = str(advertiser_id)
    publisher_id = str(publisher_id)

    weird_link  = link.replace(':', '%3A').replace('/', '%2F')

    reflink = 'https://www.awin1.com/cread.php?awinmid='+advertiser_id+'&awinaffid='+publisher_id+'&ued='+weird_link
    return reflink







