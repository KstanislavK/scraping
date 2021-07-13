import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from bs4 import BeautifulSoup as bs


class HhRuSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        dom = bs(response.text, 'html.parser')
        link = response.url
        name = dom.find('h1').text
        vacancy_salary = dom.find('p', {'class': 'vacancy-salary'}).text.replace('\xa0', '')
        salary_list = vacancy_salary.split()

        min_salary = None
        max_salary = None
        currency = None

        if vacancy_salary.find('вычета') != -1:
            min_salary = int(salary_list[1])
            max_salary = None
            currency = salary_list[2].replace('.', '')

        elif vacancy_salary.find('от') != -1 and vacancy_salary.find('до') != -1:
            min_salary = int(salary_list[1])
            max_salary = int(salary_list[3])
            currency = salary_list[4].replace('.', '')

        elif vacancy_salary.find('от') != -1:
            min_salary = int(salary_list[1])
            max_salary = None
            currency = salary_list[2].replace('.', '')

        elif vacancy_salary.find('до') != -1:
            min_salary = None
            max_salary = int(salary_list[1])
            currency = salary_list[2].replace('.', '')

        elif vacancy_salary.find('з/п не указана') != -1:
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

