#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from myscraps.items import ReviewItem
from scrapy import Request

class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    # Cities: Recife, Porto Alegre, Salvador, Brasilia, Fortaleza, Curitiba, Belo Horizonte, Vitoria, Florianopolis, Natal, Goiania.
    start_urls = ["https://www.tripadvisor.com/Hotel_Review-g60763-d7787303-Reviews-The_New_York_EDITION-New_York_City_New_York.html"]

    def parse(self, response):
        urls = []

        print('res la: ')
        print(response)
        for href in response.xpath('//*[@id="component_13"]/div/div/div/div[1]/div/div[1]/a').extract():
            print('hrrel la : ')
            print(href)

            url = response.urljoin(href)
            print(url)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath('//*[@id="component_26"]/div[3]/div/div[8]/div/a').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            print(url)
            yield scrapy.Request(url, self.parse)

    def parse_page(self, response):

        review_page = response.xpath('//div[@class="wrap"]/div/a/@href').extract()

        if review_page:
            for i in range(len(review_page)):
                url = response.urljoin(review_page[i])
                yield scrapy.Request(url, self.parse_review)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_page)

    def parse_review(self, response):

        item = ReviewItem()

        contents = response.xpath('//div[@class="entry"]/p').extract()
        content = contents[0].encode("utf-8")

        ratings = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
        rating = ratings[0][0]


        item['rating'] = rating
        item['review'] = content
        yield item

