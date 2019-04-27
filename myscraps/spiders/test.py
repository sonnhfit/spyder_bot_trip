import scrapy
import re
import json
import csv



class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.tripadvisor.com/Hotel_Review-g60763-d1646128-Reviews-InterContinental_New_York_Times_Square-New_York_City_New_York.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'qu2222otes-%s.html' % page
        print('conten la: ')
        print(response.xpath('//div/a/span/span/text()').getall())
        print('content 2: ')
        """
        /html/body/div[2]/div[2]/div[2]/div[8]/div/div[1]/div[1]/div/div[3]/div/div[3]/div/div[3]/div[3]/div[2]/div/span
        
        """
        #print(response.xpath('//div/div[1]/div[1]/div/div[3]/div/div[3]/div/div[3]/div[3]/div[2]/div/span/text()').getall())

        data = re.findall(r'(?=\{\"assets\"\:).+(?<=\"lazyLoadedModules\"\:\[\]\})',
                          response.body.decode("utf-8"), re.S)
        jso = json.loads(data[0])

        #print(jso['apolloCache'][4]['result']['locations'][0]['reviewList']['reviews'])
        list_review = []
        # id,
        # #'location' , 'name'
        #'publishedDate'
        #text
        #rating

        #'tripInfo' , 'FRIENDS'
        myreview = jso['apolloCache'][4]['result']['locations'][0]['reviewList']['reviews']
        fields = ['id', 'location', 'publishedDate', 'text', 'rating']

        with open('name.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            for item in myreview:
                sub_item = {}
                sub_item['id'] = item['id']
                sub_item['location'] = item['location']['name']
                sub_item['publishedDate'] = item['publishedDate']
                sub_item['text'] = item['text']
                sub_item['rating'] = item['rating']
                print(item['id'])
                writer.writerow({'id': item['id'], 'location': item['location']['name'],
                                 'publishedDate': item['publishedDate'], 'text': item['text'], 'rating': item['rating']})
            # file.write("%s,%s,%s,%s,%s\r\n" % (
            #     item['id'], item['location']['name'], item['publishedDate'], item['text'], item['rating']))
        csvfile.close()

        print('------------------------------------------------------------')

        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        self.log('Saved file %s' % filename)

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)
