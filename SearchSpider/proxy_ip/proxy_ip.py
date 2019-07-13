import requests
from SearchSpider.scrapy_redis.user_agents import agents
from SearchSpider.scrapy_redis.storage import RedisClient
from lxml import etree
import time
import random

headers = {
    "User-Agent": random.choice(agents)
}

client = RedisClient("ip", "port")


def get_and_set_proxy_ip(url):

    response = requests.get(url, headers=headers)

    html = etree.HTML(response.text)

    ip = html.xpath('//*[@id="list"]/table/tbody/tr/td[@data-title="IP"]/text()')
    port = html.xpath('//*[@id="list"]/table/tbody/tr/td[@data-title="PORT"]/text()')
    for i in range(len(ip)):
        proxy_ip = ip[i] + ":" + port[i]
        client.set("", proxy_ip)
        print("存储 " + proxy_ip + " 成功")


def get_next_page_url():
    for i in range(1, 2903):
        page_url = "https://www.kuaidaili.com/free/inha/" + str(i) + "/"
        print("第 " + str(i) + " 页")
        yield page_url


if __name__ == '__main__':
    for page_url in get_next_page_url():
        get_and_set_proxy_ip(page_url)
        time.sleep(random.randint(0, 3))




