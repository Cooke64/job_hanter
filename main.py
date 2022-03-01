import requests
from bs4 import BeautifulSoup as bs
import time
import telebot


bot = telebot.TeleBot("5065016412:AAH7ScOT50OK5k7-46f2ahUluw4d_xqw64g")
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
              'avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'
}
LINKS = set()

def get_html(text, param=' '):
    # Получаем главную страницу с запросом по ключевому слову
    data = requests.get(
        f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={text}&from=suggest_post&page=0',
        headers=HEADERS,
        params=param)
    soup = bs(data.content, "html.parser")
    # Считаем количество страниц по диву с классом pager
    # и находим все элементы span, где находим элекмент ссылки
    # и последний нужный элемент спан, из которого получаем текст
    page_count = int(
        soup.find("div", attrs={"class": "pager"}).find_all(
            "span", recursive=False)[-1].find("a").find("span").text)
    # Запускаем цикл для получения всех страниц
    for page in range(page_count):
        unique_urls = set()
        try:
            data = requests.get(
                f'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text={text}&from=suggest_post&page={page}',
                headers=HEADERS,
                params=param)
            if data.status_code == 200:
                soup = bs(data.content, "html.parser")
                # Если получен код 200 и страницы нет в списке уникальных
                # ссылок, то передаем эту ссылку и добавляем список уникальных
                total = soup.find_all(
                    "a",
                    attrs={"data-qa": "vacancy-serp__vacancy-title"})
                for a in total:
                    href = a.attrs["href"]
                    if href not in unique_urls:
                        unique_urls.add(href)
                        yield a.attrs["href"]
                    else:
                        continue
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def get_job(link):
    data = requests.get(
        url=link,
        headers=HEADERS,)
    if data.status_code == 200:
        soup = bs(data.content, "html.parser")
    answer = ''
    try:
        name = soup.find(attrs={"data-qa": "vacancy-title"}).text
    except:
        name = "Нет названия"
    try:
        salary = soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"}).text.replace("\u2009", "").replace("\xa0", " ")
    except:
        salary = "Уточнить зарплату"
    try:
        excp = {soup.find(attrs={"data-qa":"vacancy-experience"}).text}
    except:
        excp = "Уточнить опыт"
    url_of_vacancy = link
    res = [
        f'Название вакансии: {name}',
        f'Зарплата: {salary}',
        f'Опыт работы: {excp}',
        f'Ссылка: {url_of_vacancy}',
    ]
    for item in res:
        answer += item + '\n'
    return answer
