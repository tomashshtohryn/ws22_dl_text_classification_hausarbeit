import scrapy
from datetime import datetime, timedelta
from newsSpider.items import NewsspiderItem

class ArticlesSpider(scrapy.Spider):
    name = 'articles'

    # Create a list with dates
    delta = timedelta(days=1)
    dates = [datetime.strptime('2023/01/01', '%Y/%m/%d'),
             datetime.strptime('2023/01/02', '%Y/%m/%d')]
    date_list = []
    while dates[0] <= dates[1]:
        date_list.append(dates[0].strftime('%Y/%m/%d'))
        dates[0] += delta

    # Expand Spider with urls
    allowed_domains = ['www.derstandard.de']
    start_urls = [f'https://www.derstandard.at/international/{date}' for date in date_list]

    def parse(self, response):
        # Extract links
        article_links = response.xpath('//@href')
        for link in article_links:
            yield response.follow(link, self.parse_newsarticle)

    def parse_newsarticle(self, response):
        item = NewsspiderItem()
        article_text = response.xpath('//p/text()').getall() #//div[@class="article-body"]/p/text()
        if article_text:
            article_text = '\n'.join(article_text)
            item['article_text'] = article_text
            print(article_text)
            yield item
        else:
            print(f'not found{response.url}')
