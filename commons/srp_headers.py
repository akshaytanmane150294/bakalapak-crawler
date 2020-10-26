def srp_data():
    headers = {
        'authority': 'www.bukalapak.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.bukalapak.com/c/handphone/hp-smartphone?',
        'accept-language': 'en-US,en;q=0.9'
    }
    return headers


def mi_data(more_info_url):
    mi_headers = {
        'authority': 'api.bukalapak.com',
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'origin': 'https://www.bukalapak.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': str(more_info_url),
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'ac854d5e67d7348f8eedea001507df08c252aaea'
    }
    return mi_headers


def auth_token(more_info_url):
    auth_headers = {
        'authority': 'www.bukalapak.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.bukalapak.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': str(more_info_url),
        'accept-language': 'en-US,en;q=0.9'
    }
    return auth_headers
# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://www.bukalapak.com/p/handphone/hp-smartphone/2i7k45a-jual-samsung-galaxy-s7-edge-new-resmi-sein?from=trend&keyword=&funnel=omnisearch&product_owner=normal_seller&pos=0&cf=1&ssa=0&sort_origin=last_relist_at%3Adesc&search_sort_default=false&promoted=1', headers=headers)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://www.bukalapak.com/trend/samsung-galaxy-s7?page=2', headers=headers)
# trend = re.findall(r'from=(.*?)&', more_info_url)[0]
# omnisearch = re.findall(r'funnel=(.*?)&', more_info_url)[0]
