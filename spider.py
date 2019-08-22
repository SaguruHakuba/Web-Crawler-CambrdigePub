import requests
import pandas
import numpy
import urllib.request
from lxml import etree
import time
import os

start_page = 1
end_page = 122 + 16
book_number = 9140
dictionary = "./" + str(book_number)

# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', 'Referer': 'https://cambridgepub.com/ereader/9140/?preview', 'Sec-Fetch-Mode': 'no-cors'}
headers = {
    'Cookie' : 'auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOiIyMDIzODM0IiwiaXNzIjoid3d3Lm5ldGdlYXIuY29tIiwic3ViIjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbw==.eeaab4505772a060bafb07e19b04b4b5417b9fa3f5412865e58781b3e8391e03; csrf_cpb_cookie=6c86b3c12af0222e7a217ef8bf251436; _ga=GA1.2.770111770.1566425870; _gid=GA1.2.203320899.1566425870; ublish_cpb=0fi3bqht02irjhbgnhnjlphrr054amja',
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

urls = format_url(150, 160)

def parse_base_info (url, headers = headers, number = '', ip = ''):
    if ip == '':
        html = requests.get(url, headers = headers)
    else:
        html = requests.get(url, headers = headers, proxies = ip)

    bs = etree.HTML(html.text)
    image = bs.xpath('//div[@class="wrap"]/img/@data-src') 

    if not os.path.isdir(dictionary):
        os.makedirs(dictionary)

    try:
        urllib.request.urlretrieve(image[0], dictionary + "/" + str(number) + ".png")
        return True
    except:
        return False

count = 1
for url in urls:
    df = parse_base_info(url, headers = headers, number = count)
    if df == False:
        break
    time.sleep(0.1)
    print('I had crawled page of %d' % count)
    count += 1