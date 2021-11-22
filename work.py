import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1;rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax')
        div_lst = main_div.find_all('div', attrs={'class' : 'job-link'})
        if main_div:
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
            jobs.append({'title' :title.text, 'url':domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        table = soup.find('table', id='ctl00_content_vacancyList_gridList')
        if table:
            tr_lst = table.find_all('tr', attrs={'id': True})
            for tr in tr_lst:
                div = tr.find('div', attrs={'class': 'card-body'})
                if div:
                    title = div.find('h2', attrs={'class': 'card-title'})
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'card-description'})
                    company = 'No name'
                    p = div.find('div', attrs={'class': 'card-logo'})
                    if p:
                        company = p.a.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Table does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


def djinni(url):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_lu = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_lu:
            li_lst = main_lu.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_lst:
                    title = li.find('div', attrs={'class': 'list-jobs__title'})
                    href = title.a['href']
                    cont = li.find('div', attrs={'class': 'list-jobs__description'})
                    content = cont.text
                    company = 'No name'
                    com = li.find('div', attrs={'class': 'list-jobs__details__info'})
                    if com:
                        company = com.text
                    jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Table does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/keyword-python/kyiv/'
    jobs, errors = djinni(url)
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
