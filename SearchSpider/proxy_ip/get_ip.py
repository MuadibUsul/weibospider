from SearchSpider.scrapy_redis.storage import RedisClient


ip = RedisClient("ip", "port").random()

