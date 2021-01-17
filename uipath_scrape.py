import requests
from bs4 import BeautifulSoup
import logging
import io
import os


def scrape_with_keyword(keyword):
    links = BeautifulSoup(requests.get(
        'https://www.uipath.com/resources/automation-case-studies').content, 'lxml').find_all('a', {'class': 'resource-item Success story'})

    links += BeautifulSoup(requests.get(
        'https://www.uipath.com/resources/automation-case-studies').content, 'lxml').find_all('a', {'class': 'resource-item Success story  featured'})

    j = 1

    try:
        os.mkdir(keyword)
    except:
        print('directory could not be created!')
        quit()

    for link in links:
        try:
            try:
                report = BeautifulSoup(requests.get(
                    'https://www.uipath.com' + link['href']).content, 'lxml')
                for r in report(['script', 'style']):
                    r.extract()

                report = report.get_text().lower().replace('contact sales', '')

                if(keyword in report):
                    print('https://www.uipath.com' + link['href'])
                    with io.open(keyword + "/" + str(j) + ".txt", "w", encoding='utf-8') as f:
                        f.write(report)

                    j += 1

            except:
                report = BeautifulSoup(requests.get(
                    link['href']).content, 'lxml')
                for r in report(['script', 'style']):
                    r.extract()

                report = report.get_text().lower().replace('contact sales', '')

                if(keyword in report):
                    print(link['href'])
                    with io.open(keyword + "/" + str(j) + ".txt", "w", encoding='utf-8') as f:
                        f.write(report)

                    j += 1
        except:
            logging.exception('exception')
            pass


if __name__ == '__main__':
    scrape_with_keyword(input("keyword: "))
