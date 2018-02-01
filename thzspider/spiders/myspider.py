import scrapy
import re
from scrapinghub import ScrapinghubClient


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        'http://thz.la/forum-220-1.html',
    ]
    codelist = []
    namelist = []

    apikey = '11befd9da9304fecb83dfa114d1926e9'
    client = ScrapinghubClient(apikey)
    project = client.get_project(252342)

    for job in list(project.jobs.iter_last(spider='javcode', state='finished')):
        codejob = job

    print(codejob['key'])
    lastcodejob = project.jobs.get(codejob['key'])

    for item in lastcodejob.items.iter():
        codelist.append(item['code'])
        namelist.append(item['name'])

    def parse(self, response):

        for new in response.css('th.new'):
            try:
                code_new = re.split(r'[\[\]]', new.css(
                    'a.xst::text').extract_first())[1].upper()
                href_new = new.css('a.xst::attr("href")').extract_first()
                if code_new in MySpider.codelist:
                    name_new = MySpider.namelist[MySpider.codelist.index(
                        code_new)]
                    yield response.follow(href_new, self.getdetail, meta={'code': code_new, 'name': name_new})
            except Exception:
                pass

        for common in response.css('th.common'):
            try:
                code_common = re.split(r'[\[\]]', common.css(
                    'a.xst::text').extract_first())[1].upper()
                href_common = common.css('a.xst::attr("href")').extract_first()
                if code_common in MySpider.codelist:
                    name_common = MySpider.namelist[MySpider.codelist.index(
                        code_common)]
                    yield response.follow(href_common, self.getdetail, meta={'code': code_common, 'name': name_common})
            except Exception:
                pass

        next_page = response.css('a.nxt::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def getdetail(self, response):
        code = response.meta['code']
        name = response.meta['name']
        text = response.css('h1.ts span::text').extract_first()
        imgf = response.css('img.zoom::attr("file")').extract_first()
        yield {
            'code': code,
            'name': name,
            'text': text,
            'href': response.url,
            'imgf': imgf,
        }
