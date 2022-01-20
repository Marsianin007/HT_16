import datetime
import scrapy

from Scraper_sql.items import ScraperSqlItem


# функція перевірки дати
def get_date():
    date_check = True
    date = input("Введіть дату у форматі yyyy/mm/dd: ")

    try:
        valid_date = datetime.datetime.strptime(date, '%Y/%m/%d')

        if valid_date.date() > datetime.datetime.now().date():
            date_check = False
    except:
        date_check = False

    return date_check, date

# клас, метод якого "start_requests" викликається першим при запуску павука
class SiteSpider(scrapy.Spider):
    date, date_check = None, None

    def start_requests(self):
        SiteSpider.date_check, SiteSpider.date = get_date()
        while SiteSpider.date_check is False:
            SiteSpider.date_check, SiteSpider.date = get_date()
        else:
            yield scrapy.Request(url=self.start_urls[0] + str(SiteSpider.date), callback=self.parse)

    name = "spider_sql"
    start_urls = ["https://www.vikka.ua/"]  #посилання на початкову сторінку

    def parse(self, response):
        for link in response.xpath("//h2[@class='title-cat-post']//a/@href"): #проходження по всім новинам на сторінці
            yield response.follow(link, callback=self.parse_news)

        next_page = response.xpath("//a[@class='page-numbers']/@href").get() #пошук посилання на нову сторінку(пагінація)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_news(self, response):
        item = ScraperSqlItem()
        item["title"] = response.xpath("//h1[@class='post-title -margin-b']/text()").get()
        item["news_text"] = response.xpath("//div[@class='entry-content -margin-b']/p/text()").getall()
        item["tegs"] = response.xpath("//a[@class='post-tag']/text()").getall()
        item["link"] = response.url
        item["date"] = self.date
        yield item
