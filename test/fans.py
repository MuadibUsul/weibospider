import re
from lxml import etree
# 8 -1  关注
# 8 -2  粉丝

filepath = './粉丝.html'
with open(filepath, 'r') as f:
    content = f.read()

rule = '''\"html\":\"(.+?)\"}\)</script>'''
results = re.findall(rule, content)
print(len(results))
string = results[-1]
print(string)
string = string.replace('>\\r\\n', '>\n')
string = string.replace('\\t', '')
string = string.replace('\\', '')

html = etree.HTML(string)
items = html.xpath("//dd[@class='mod_info S_line1']")
follow_group = {}
for item in items:
    follow_group['title'] = item.xpath('./div[1]/a[1]/text()')
    follow_group['index_url'] = item.xpath('./div[1]/a[1]/@href')
    follow_group['v_type'] = item.xpath('./div[1]/a[2]/i/@title')
    follow_group['sex'] = item.xpath('./div[1]/a[4]/i/@class')
    follow_group['follows'] = item.xpath('./div[2]/span[1]/em/a/text()')
    follow_group['fans'] = item.xpath('./div[2]/span[2]/em/a/text()')
    follow_group['blogs'] = item.xpath('./div[2]/span[3]/em/a/text()')
    follow_group['addr'] = item.xpath('./div[4]/span/text()')
    follow_group['intro'] = item.xpath('./div[5]/span/text()')
    follow_group['follow_way'] = item.xpath('./div[6]/a/text()')

    print(follow_group)
