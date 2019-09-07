import re
from lxml import etree
# 8 -1  关注
# 8 -2  粉丝

filepath = './资料详情.html'
with open(filepath, 'r') as f:
    content = f.read()

rule = '''\"html\":\"(.+?)\"}\)</script>'''
results = re.findall(rule, content)
# for i in results:
#     print(i)
string = results[-1]
# print(string)
string = string.replace('>\\r\\n', '>\n')
string = string.replace('\\t', '')
string = string.replace('\\', '')
html = etree.HTML(string)
# with open('string.html', 'wb') as f:
#     f.write(string.encode('utf-8'))
detail_group = {}
detail_group['name'] = html.xpath('//div[1]//div[1]//div[2]//li[1]/span[2]/text()')
detail_group['addr'] = html.xpath('//div[1]//div[1]//div[2]//li[2]/span[2]/text()')
detail_group['sex'] = html.xpath('//div[1]//div[1]//div[2]//li[3]/span[2]/text()')
detail_group['website'] = html.xpath('//div[1]//div[1]//div[2]//li[4]/span[2]//a/@href')
detail_group['intro'] = html.xpath('//div[1]//div[1]//div[2]//li[5]/span[2]/text()')
sigh_time = html.xpath('//div[1]//div[1]//div[2]//li[6]/span[2]/text()')
detail_group['sigh_time'] = re.search('([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))', sigh_time[0]).group()
detail_group['tags'] = html.xpath('//div[2]//div[2]//div[1]//ul[1]/li[1]/span/a/text()')

print(detail_group)
