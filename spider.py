import requests
import pandas
import numpy
import urllib.request
from lxml import etree
import time
import os

import logging
logging.basicConfig(filename='spider_log.log',level=logging.DEBUG)

start_page = 0
end_page = 200
book_number = 9140
# cookie_str = 'auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDIzODM0IiwiaXNzIjoid3d3Lm5ldGdlYXIuY29tIiwic3ViIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbw==.eeaab4505772a060bafb07e19b04b4b5417b9fa3f5412865e58781b3e8391e03; _ga=GA1.2.770111770.1566425870; _gid=GA1.2.1298927245.1566573228; csrf_cpb_cookie=2480f0264902ca17021cfe3b7ae78021; ublish_cpb=haeeh09ifnvpnu29o80igturrhl8ssfj; _gat=1; ublish_alert_delay=true'
cookie_str = '_ga=GA1.2.770111770.1566425870; csrf_cpb_cookie=80f6d4a4ffe6b242c7c090b9a261c148; _gid=GA1.2.471324130.1578568966; ublish_cpb=taqdq9jeuf9qgj0iors17d2s2i4bvimq'

dictionary = "./" + str(book_number)

if start_page > end_page:
    logging.warning("Start page shall not be smaller than end page.")
logging.info("Start downloading book %d, start from page %d, to page %d" % (book_number, start_page, end_page))

# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Referer': 'https://cambridgepub.com/ereader/9140/?preview', 'Sec-Fetch-Mode': 'no-cors'}
headers = {
    'Cookie' : cookie_str,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Sec-Fetch-Mode': 'navigate'
}

def format_url(start, end):
    urls = []
    # base_url = 'https://cambridgepub.com/ereader/9140/?preview#page/{}'
    # base_url = 'https://cambridgepub.com/ereader/103/'+ str(book_number) +'/{}.html?client=cpb&type=1&preview=1'
    base_url = 'https://cambridgepub.com/ereader/103/'+ str(book_number) +'/{}.html?client=cpb&type=1'
    for i in range(start, end):
        url = base_url.format(i)
        urls.append(url)
    return urls

urls = format_url(start_page, end_page)

def parse_base_info (url, headers = headers, number = '', ip = ''):
    if ip == '':
        html = requests.get(url, headers = headers)
    else:
        html = requests.get(url, headers = headers, proxies = ip)

    bs = etree.HTML(html.text)
    image = bs.xpath('//div[@class="wrap"]/img/@data-src') 

    if image == []:
        logging.warning("Missing image! Download is not complete")
        return False
    if not os.path.isdir(dictionary):
        os.makedirs(dictionary)

    try:
        urllib.request.urlretrieve(image[0], dictionary + "/" + str(number) + ".png")
        return True
    except:
        return False

count = start_page + 1
for url in urls:
    df = parse_base_info(url, headers = headers, number = count)
    if df == False:
        break
    time.sleep(0.1)
    print('Downloading page %d of book %d' % (count, book_number))
    logging.info("I am downloading book number %d page %d" % (book_number, count))
    count += 1

logging.info("Finished downloading book %d, last page %d" % (book_number, count))    