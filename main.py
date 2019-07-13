from scrapy import cmdline

name = "weibo"
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())