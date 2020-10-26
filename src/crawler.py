import csv
import os
import re
import requests
import openpyxl
from os.path import abspath
import pandas as pd
from lxml import html
from itertools import cycle
import pytest
from pandas.tests.io.excel.test_xlrd import xlrd
from commons.proxy_file import get_proxies
from commons.srp_headers import srp_data, mi_data, auth_token

input_file_dir = abspath("./commons")
file_name = os.path.join(input_file_dir, 'bukalapak_product_input.xlsx')
file_csv_name = os.path.join(input_file_dir, 'bukalapak_product_input.csv')
file_name_bakalapak = os.path.join(input_file_dir, 'bukalapak_product_output_final.xlsx')
file_csv_bakalapak = os.path.join(input_file_dir, 'bukalapak_product_output_final.csv')

proxies = get_proxies()
proxy_pool = cycle(proxies)
url = 'https://www.bukalapak.com/trend/samsung-galaxy-s7'


def write_to_csv(file_csv_name, dump_info, write_headers=True):
    print("Here is your post{}-{}-{}".format(file_csv_name, dump_info, write_headers))
    keys = dump_info[0].keys()
    with open(file_csv_name, 'a+') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        if write_headers: dict_writer.writeheader()
        dict_writer.writerows(dump_info)


def scraper_data(data_listing_size, Product_name, Product_price, Product_url):
    lst = []
    count = 0
    while int(data_listing_size) > count:
        print(
            "listing - {}, Product_name - {}, Product_price - {}, Product_url - {}".format(count, Product_name[count],
                                                                                           Product_price[count],
                                                                                           Product_url[count]))
        hsh = {"Categaory": "HHP", "Product_name": Product_name[count].strip(),
               "Product_price": Product_price[count].strip(),
               "Product_url": Product_url[count].strip()}
        lst.append(hsh)
        count = count + 1
    return lst


def crawler():
    response = requests.get('https://www.bukalapak.com/trend/samsung-galaxy-s7', headers=srp_data())
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        total_list_count = tree.xpath('//p[contains(@class,"te-total-products")]//text()')[0]
        expected_count = ''.join(re.findall(r'[0-9]+', total_list_count))
        print("Total Listing count - ", format(total_list_count))
        page_start = 0
        page_no = 1
        write_headers = True
        while int(expected_count) > page_start:
            if page_no == 1:
                tree = html.fromstring(response.content)
            else:
                params = (('page', str(page_no)),)
                response = requests.get(url, headers=srp_data(), params=params)
                tree = html.fromstring(response.content)
            Product_name = tree.xpath('//div[@class="bl-product-card__description-name"]//p/a//text()')
            Product_price = tree.xpath('//div[@class="bl-product-card__description-price"]//p/text()')
            Product_url = tree.xpath('//div[@class="bl-product-card__description-name"]//p/a//@href')
            data_listing_size = len(tree.xpath('//div[contains(@class,"bl-product-card te-product-card")]'))
            all_data = scraper_data(data_listing_size, Product_name, Product_price, Product_url)
            write_to_csv(file_csv_name, all_data, write_headers=write_headers)
            read_file = pd.read_csv(file_csv_name)
            read_file.to_excel(file_name, index=None, header=True)
            write_headers = False
            print(
                "Inventory fetch page_no - {}, listings_count - {}, fetched {}".format(page_no, expected_count,
                                                                                       page_start + data_listing_size))
            page_no = page_no + 1
            page_start = page_start + data_listing_size
            if page_start >= 200:
                break
        loc = (file_name)
        print(loc)
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        sheet.cell_value(0, 3)
        new_lst = []
        for i in range(sheet.nrows):
            if i > 0:
                print(sheet.cell_value(i, 3))
                more_info_url = sheet.cell_value(i, 3)
                id = re.findall(r'hp-smartphone\/(.*)\-jual', more_info_url)[0]
                data = '{"application_id":1,"authenticity_token":""}'
                response = requests.post('https://www.bukalapak.com/westeros_auth_proxies',
                                         headers=auth_token(more_info_url), data=data)
                data_json = response.json()
                access_token = data_json['access_token']
                params = (('access_token', access_token),)
                resp = requests.get('https://api.bukalapak.com/products/' + str(id), headers=mi_data(more_info_url),
                                    params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    Listing_Title = data['data']['name']
                    if 'original_price' not in data['data']['deal']:
                        Listing_Price = "Not available"
                    else:
                        Listing_Price = data['data']['deal']['original_price']
                    Promo_Price = data['data']['price']
                    Prod_Rating = data['data']['rating']['average_rate']
                    Prod_Raview = data['data']['rating']['user_count']
                    Stock = data['data']['stock']
                    Sku_Id = data['data']['sku_id']
                    Url = data['data']['url']
                    Site_Prod_ID = data['data']['id']
                    Stocks_availability = data['data']['state']
                    Description = data['data']['description']

                    if "ukuran_layar" not in data['data']['specs']:
                        Size = "Not available"
                    else:
                        Size = data['data']['specs']['ukuran_layar']

                    if "specs" not in data['data']:
                        Specification = "Not available"
                    else:
                        Specification = data['data']['specs']

                    if "name" not in data['data']['store']:
                        Seller_Name = "Not available"
                    else:
                        Seller_Name = data['data']['store']['name']

                    if 'cheapest' not in data['data']['warranty']:
                        Warranty = "Not available"
                    else:
                        Warranty = data['data']['warranty']['cheapest']

                    if 'merk' not in data['data']['specs']:
                        Brand = "Samsung"
                    else:
                        Brand = data['data']['specs']['merk']

                    print(Listing_Title)
                    print(
                        "Listing_Title - {}, Listing_Price - {}, Promo_Price - {}, Prod_Rating - {},Prod_Raview - {},Stock - {} ,Sku_Id - {},Url - {}, Site_Prod_ID -{}".format(
                            Listing_Title, Listing_Price, Promo_Price,
                            Prod_Rating, Prod_Raview, Stock, Sku_Id, Url, Site_Prod_ID))
                    hsh = {"Listing_Title": Listing_Title, "Listing_Price": Listing_Price, "Promo_Price": Promo_Price,
                           "Prod_Rating": Prod_Rating, "Prod_Raview": Prod_Raview, "Stock": Stock,
                           "Sku_Id": Sku_Id, "Url": Url, "Site_Prod_ID": Site_Prod_ID, "Brand": Brand,
                           "Seller_Name": Seller_Name, "Stocks_availability": Stocks_availability, "Warranty": Warranty,
                           "Size": Size, "Description": Description, "Specification": Specification
                           }
                    new_lst.append(hsh)
                else:
                    print("NOT found any data in more detail page")
        all_new_data = new_lst
        write_headers = True
        write_to_csv(file_csv_bakalapak, all_new_data, write_headers=write_headers)
        read_file = pd.read_csv(file_csv_bakalapak)
        read_file.to_excel(file_name_bakalapak, index=0, header=True)
    else:
        print(response.status_code)

if __name__ == "__main__":
    crawler()
