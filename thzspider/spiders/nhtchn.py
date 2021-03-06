# -*- coding: utf-8 -*-
import requests
import scrapy
from scrapinghub import ScrapinghubClient

BASE_URL = 'https://nhentai.net/language/chinese/'
API_KEY = '11befd9da9304fecb83dfa114d1926e9'
PROJECT_ID = '252342'


class NhtchnSpider(scrapy.Spider):
    name = 'nhtchn'
    start_urls = []

    def __init__(self):
        client = ScrapinghubClient(API_KEY, use_msgpack=False)
        project = client.get_project(PROJECT_ID)

        NhtchnSpider.start_urls.append(BASE_URL)

# div.contain .blue{color:blue;}
# div.contain.blue{color:blue;}
# 以上两种规则分别应用的元素如下：

# 1
#   <!--后代-->
#   <div class="contain">
#      contain
#   <span class="blue">blue</span>
#   </div>
# 2
# <!--多类-->
# <div class="contain blue">contain and blue</div>

    def parse(self, response):
        for codeitem in response.css('div.container.index-container'):
            for galleryitem in codeitem.css('div.gallery'):
                gallery_href = galleryitem.css('a::attr(href)').extract_first()
                gallery_caption = galleryitem.css(
                    'a .caption::text').extract_first()
                gallery_thumb = galleryitem.css(
                    'a .lazyload::attr(data-src)').extract_first()
                # id_code = codeitem.css('div.id::text').extract_first()
                # href_link = codeitem.css('a::attr(href)').extract_first()
                # img_small = codeitem.css('img::attr(src)').extract_first()
                yield {
                    'href': gallery_href,
                    'capt': gallery_caption,
                    'thmb': gallery_thumb,
                }
        # next_page = response.css('a.next::attr("href")').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
