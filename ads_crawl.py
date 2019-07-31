#py3

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
import time
import random


logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='a')


main_address = 'https://sh.58.com/fushixm/pn61/?PGTID=0d306794-0000-28d1-d915-3fcc796bb31c&ClickID=1'
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


def request_url(header, url):
    r = requests.get(url, headers = header)
    if r.status_code == 200:
        return bs(r.content.decode('utf-8'))
    else:
        logging.info('url {} parser encountered something error...'.format(url))


def get_description(root):
    children = request_url(header, root).find_all('a', rel="nofollow", target="_blank")
    children = [x['href'] for x in children]
    print(len(children))
    return children
    


def page_shift(n):
    for i in range(2, n):
        root = 'https://sh.58.com/fushixm/pn{}/\
            ?PGTID=0d306794-0000-28d1-d915-3fcc796bb31c&ClickID=1'.format(i)

        ads_text = set()
        children = get_description(root)
        time.sleep(random.randint(5, 8))
        for child in children:
            try:
                print(child)
                lines = request_url(header, child).find_all('meta')
                for line in lines:
                    if line.has_attr('name') and line['name'] == 'description':
                        ads_text.add(line['content'])
                        break
            except:
                logging.info("children {} crawler encounted something error ...".format(child))
            time.sleep(random.randint(5, 8))
        with open('./crawer_advertisiment.txt', 'a') as f:
            for text in ads_text:
                f.write(text + '\n')
        #assert False
        #time.sleep(random.randint(5, 10))
            
            

page_shift(100)