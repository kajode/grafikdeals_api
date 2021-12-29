from bs4 import BeautifulSoup as bs
import utility_functions as ut
import time

shop_name = 'mediamarkt'

def get_cards_html():
    cards_html = []

    #repeat for all pages
    for i in range(1,10):

        # parse website and extract all cards
        soup = ut.get_soup("https://www.mediamarkt.de/de/category/grafikkarten-4560.html?page="+str(i))
        cards_list = soup.find('div', attrs={"data-test": "mms-search-srp-productlist"})
        l_cards_html = cards_list.find_all('div',attrs={"data-test": "mms-search-srp-productlist-item"})

        for l_card_html in l_cards_html:
            cards_html.append(l_card_html)

    return cards_html


def find_card(cards):

    cards_html = get_cards_html()
    card_types = []

    for card in cards:
        card_types.append(card[0])

    for card_html in cards_html:
        card_fullname = card_html.find('h2', attrs={"data-test": "product-title"}).text
        card_link = 'https://www.mediamarkt.de' + card_html.find('a', attrs={"data-test": "mms-router-link"})['href']

        #remove ® and ™ from card name
        card_fullname = card_fullname.replace('™','').replace('®','')

        print(card_fullname)

        #check if the card is looked for and add it to list
        for card_type in card_types:
            if card_type+' Ti' in card_fullname:
                ut.add_link(shop_name, card_type+' Ti', card_link)
            elif card_type+' XT' in card_fullname:
                print('adding to list')
                ut.add_link(shop_name, card_type+' XT', card_link)
            elif card_type in card_fullname:
                print('adding to list')
                ut.add_link(shop_name, card_type, card_link)

def check_price(card):

    card_type = card[0]
    card_max_price = 0.9*ut.read_weekly_average(card_type)

    links = ut.read_links(shop_name, card_type)
    deals = []
    minprice  = ''

    print(links)
    for link in links:

        #load website
        soup = ut.get_soup(link)

        #check if availible
        status = soup.find('span', class_='StyledAvailabilityTypo-sc-901vi5-7')
        if 'Leider keine Lieferung möglich' in status:
            print('not in stock\n')
            continue

        card_price = float(soup.find('span', class_='ScreenreaderTextSpan-sc-11hj9ix-0').text.replace('undefined ',''))
        card_fullname = soup.find('h1', class_='StyledInfoTypo-sc-1jga2g7-0').text.replace('"','')

        #save price in history
        ut.write_price(card_type, card_price)

        if card_price <= card_max_price:
            print("Found a deal!")
            deals.append([card_type, card_price, card_fullname, link.replace('\n', ''), shop_name])

    return deals



