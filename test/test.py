import requests
# 资料详情
url1 = 'https://weibo.com/p/1003061192329374/info?mod=pedit_more'
# 主页
url2 = 'https://weibo.com/xiena?topnav=1&wvr=6&topsug=1&is_all=1'
# 粉丝
url3 = 'https://weibo.com/p/1003061192329374/follow?relate=fans&from=100306&wvr=6&mod=headfans&current=fans#place'
# 关注
url4 = 'https://weibo.com/p/1003061192329374/follow?from=page_100306&wvr=6&mod=headfollow#place'
# 热门微博
url5 = 'https://d.weibo.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Cookie': 'SUB=_2A25wa6aoDeRhGeBH7FoY9inFyDSIHXVTl8rgrDV_PUNbm9ANLWrakW1NQbkgYBB0PLm0sMf2MDktEFiu9myx42N_'
}

session = requests.Session()
response = session.get(url=url5, headers=headers)
print(response.status_code)
if response.status_code == 200 and response.content:
    with open('热门.html', 'wb') as file:
        file.write(response.content)

