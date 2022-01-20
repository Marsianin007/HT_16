# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

base = sqlite3.connect("base.db")
cur = base.cursor()
base.execute('CREATE TABLE IF NOT EXISTS authors_table(title text, news text, tegs text, link text)')

class ScraperSqlPipeline:
    def process_item(self, item, spider):
        print("Title: " + item["title"])
        print("News_text: " + "".join(item["news_text"]))
        print("Tegs: " + ", ".join(item["tegs"]))
        print("Link: " + item["link"])

        str_news = " ".join(item["news_text"])
        str_tegs = "#".join(item["tegs"])

        cur.execute('INSERT INTO authors_table VALUES(?, ?, ?, ?)', (item["title"], str_news, str_tegs, item["link"]))
        base.commit()
        return item
