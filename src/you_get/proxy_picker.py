from bs4 import BeautifulSoup
from urllib import request
import random

def pick_a_chinese_proxy():
    content = request.urlopen(
        "http://www.proxynova.com/proxy-server-list/country-cn/").read()
    content = open("/tmp/proxies.html").read()
    soup = BeautifulSoup(content, 'lxml')
    all_proxies = []
    for row in soup.find_all('tr')[1:]:
        try:
            ip = row.find_all('span', {'class' : 'row_proxy_ip'})[0].text.strip()
            port = row.find_all('td')[1].text.strip()
            cur_proxy = "{}:{}".format(ip, port)
            all_proxies.append(cur_proxy)
        except:
            pass

    return random.choice(all_proxies)
