import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from bs4 import BeautifulSoup as bs
import re


class SJobSpider(scrapy.Spider):
    name = 'S_job'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        dom = bs(response.text, 'html.parser')
        vacancy_link = dom.find_all('a', {'class': re.compile('icMQ_ _6AfZ9')})
        vacancy_link = list(map(lambda item: 'https://www.superjob.ru' + item['href'], vacancy_link))

        for item in vacancy_link:
            yield response.follow(item, callback=self.vacancy_parse)

        domain = 'https://www.superjob.ru/'
        next_link = dom.find('a', text='Дальше')['href']

        if next_link != None:
            next_page = domain + next_link
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        dom = bs(response.text, 'html.parser')
        link = response.url

        name = dom.find('h1').text
        salary_string = dom.find('span', {'class': '_1h3Zg _2Wp8I _2rfUm _2hCDz'}).text
        salary_list = salary_string.split()

        min_salary = None
        max_salary = None
        currency = None

        if salary_list[0] == 'до':
            min_salary = None
            max_salary = int(salary_list[1] + salary_list[2])
            currency = salary_list[3].replace('.', '')

        elif salary_list[0] == 'от':
            min_salary = int(salary_list[1] + salary_list[2])
            max_salary = None
            currency = salary_list[3].replace('.', '')

        elif salary_list[0].isdigit() and salary_list[2] == '-':
            min_salary = int(salary_list[0] + salary_list[1])
            max_salary = int(salary_list[3] + salary_list[4])
            currency = salary_list[5].replace('.', '')

        elif salary_list[0].isdigit():
            min_salary = None
            max_salary = int(salary_list[0] + salary_list[1])
            currency = salary_list[2].replace('.', '')

        elif salary_string.find('По договорённости') != -1:
            min_salary = None
            max_salary = None
            currency = None

        item = JobparserItem(
            name=name,
            link=link,
            min_salary=min_salary,
            max_salary=max_salary,
            currency=currency,
            )

        yield item
