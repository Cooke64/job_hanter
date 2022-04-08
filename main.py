from typing import Any

import requests
from bs4 import BeautifulSoup as bs
import time
import telebot
from requests import RequestException

bot = telebot.TeleBot("bot_token")
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
              'avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'
}
LINKS = set()


def get_page_data(text: str, page: int = 0, param: str = '') -> Any:
    """Получаем страницу с указанными параметрами
    запроса по пагинации и содержанию вакансии.
    """
    try:
        data = requests.get(
            f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={text}&from=suggest_post&page={page}',
            headers=HEADERS,
            params=param)
        return data
    except RequestException as error:
        raise error


def get_amount_of_pages(soup: any) -> int:
    """Считаем количество страниц по div с классом pager
    и находим все элементы span, где находим элемент ссылки
    и последний нужный элемент span, из которого получаем текст.
    """
    try:
        total = int(
            soup.find("div", attrs={"class": "pager"}).find_all(
                "span", recursive=False)[-1].find("a").find("span").text)
    except ValueError as error:
        raise error
    return total


def get_parsed_vacancy_page(text):
    """Возвращает результаты парсинга каждой отдельной страницы
    запроса и сохраняет в set для проверки уникальности значений.
    """
    data = get_page_data(text, param=' ')
    soup = bs(data.content, "html.parser")
    page_count = get_amount_of_pages(soup)
    # Запускаем цикл для получения всех страниц
    for page in range(page_count):
        unique_urls = set()
        try:
            data = get_page_data(text, param=' ')
            if data.status_code == 200:
                soup = bs(data.content, "html.parser")
                # Если получен код 200 и страницы нет в списке уникальных
                # ссылок, то передаем эту ссылку и добавляем список уникальных
                total = soup.find_all(
                    "a",
                    attrs={"data-qa": "vacancy-serp__vacancy-title"})
                for item in total:
                    href = item.attrs["href"]
                    # Проверка уникальности ссылки на вакансию
                    if href not in unique_urls:
                        unique_urls.add(href)
                        # Возвращаем ссылку на конкретную вакансию
                        yield item.attrs["href"]
                    else:
                        continue
        except Exception as e:
            raise e
        time.sleep(1)


def show_result(link: str, name: str, salary: str, excp: str) -> str:
    answer = ''
    res = [
        f'Название вакансии: {name}',
        f'Зарплата: {salary}',
        f'Опыт работы: {excp}',
        f'Ссылка: {link}',
    ]
    for item in res:
        answer += item + '\n'
    return answer


def get_requested_job(link):
    """Показывает результаты запроса на вакансию в человека-читаемом
    виде и предает в бот для отображения результатов.
    """
    try:
        data = requests.get(
            url=link,
            headers=HEADERS,)
    except RequestException as error:
        raise error

    soup = bs(data.content, "html.parser")
    try:
        name = soup.find(attrs={"data-qa": "vacancy-title"}).text
    except:
        name = "Нет названия"
    try:
        salary = (soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"})
                  .text.replace("\u2009", "").replace("\xa0", " ")
                  )
    except:
        salary = "Уточнить зарплату"
    try:
        excp = {soup.find(attrs={"data-qa":"vacancy-experience"}).text}
    except:
        excp = "Уточнить опыт"
    show_result(link, name, salary, excp)
