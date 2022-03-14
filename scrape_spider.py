import scrapy
from ..items import NeuronSquareItem
class midsouth(scrapy.Spider):
    name = 'midsouth'
    pages = 2
    def start_requests(self):
        urls = [
            "https://www.amazon.in/earphones/s?k=earphones",
            "https://www.amazon.in/earphones/s?k=earphones&page=2&qid=1647172712&ref=sr_pg_2",
        ]
        for url in urls:
            yield scrapy.Request(url = url,callback=self.parse)

    def parse(self, response):
        price = response.css('.a-text-normal .a-price-whole::text').extract()
        earphones = response.xpath("//a[@class='a-link-normal s-no-outline']").xpath("@href").getall()
        earphones = earphones[1:]
        for earphone in earphones:
            yield response.follow(url=earphone,callback = self.parse_categ)

    def parse_categ(self,response):
        items = NeuronSquareItem()
        price = response.css('#corePrice_feature_div .a-price-whole::text').extract_first()
        description = response.css('#feature-bullets .a-list-item::text').extract()
        review = response.css('.a-expander-partial-collapse-content::text').extract()
        title = response.css('#productTitle::text').extract()
        stock = response.css('.a-color-success::text').extract()
        manufacturer = response.css('#merchant-info span::text').extract()
        items['price'] = price
        items['description'] = description
        items['review'] = review
        items['title'] = title
        if len(stock)==0:
            items['stock']=['false']
        else:
            items['stock']=['true']

        items['manufacturer'] = manufacturer
        yield items


