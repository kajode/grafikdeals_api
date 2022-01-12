import csv
import utility_functions as ut
import requests
import gzip
import io

shop_name = 'JACOB Computer'
data_feed = 'https://productdata.awin.com/datafeed/download/apikey/7d75b4e43ab4ecaaa20a4d0df774a5c7/language/de/fid/43441,43443/columns/aw_deep_link,product_name,merchant_category,search_price,merchant_name,in_stock/format/csv/delimiter/%2C/compression/gzip/adultcontent/1/'


def run(cards):
    #get the csv file
    re = requests.get(data_feed, stream=True, allow_redirects=True)


    with gzip.open(io.BytesIO(re.content), 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        ##find graphics card in
        product_name_index = 0
        merchant_category_index = 0
        price_index = 0
        link_index = 0
        in_stock_index = 0
        counter = 0


        for row in csv_reader:
            if line_count == 0:
                for name in row:
                    if name == 'aw_deep_link':
                        link_index = counter
                    if name == 'product_name':
                        product_name_index = counter
                    if name == 'merchant_category':
                        merchant_category_index = counter
                    if name == 'search_price':
                        price_index = counter
                    if name == 'in_stock':
                        in_stock_index = counter
                    counter += 1

                line_count = 1

            else:
                for card_type in cards:
                    if 'Grafikkarten' in row[merchant_category_index] and card_type in row[product_name_index] and int(row[in_stock_index]) == 1:
                        card_fullname = row[product_name_index]
                        card_price = row[price_index]
                        link = row[link_index]
                        print(link)

                        ut.mysql_add_to_temp(card_type, card_price, link, shop_name, card_fullname)
                        ut.mysql_add(card_type, card_price, link, shop_name)

def check_prices(cards):
    try:
        print('trying to check prices at jacob')
        run(cards)
    except:
        print('failed to check prices at jacob')
