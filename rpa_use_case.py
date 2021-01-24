def uipath(keyword):
    import requests
    from bs4 import BeautifulSoup
    import io
    from tqdm import tqdm

    links = BeautifulSoup(requests.get(
        'https://www.uipath.com/resources/automation-case-studies').content, 'lxml').find_all('a', {'class': 'resource-item Success story'})

    links += BeautifulSoup(requests.get(
        'https://www.uipath.com/resources/automation-case-studies').content, 'lxml').find_all('a', {'class': 'resource-item Success story  featured'})

    for link in tqdm(links):
        try:
            try:
                report = BeautifulSoup(requests.get(
                    'https://www.uipath.com' + link['href']).content, 'lxml')
                for r in report(['script', 'style']):
                    r.extract()

                report = report.get_text().lower().replace('contact sales', '')

                if(keyword in report):
                    with io.open(keyword + ".txt", "w", encoding='utf-8') as f:
                        f.write('https://www.uipath.com' + link['href'])

            except:
                report = BeautifulSoup(requests.get(
                    link['href']).content, 'lxml')
                for r in report(['script', 'style']):
                    r.extract()

                report = report.get_text().lower().replace('contact sales', '')

                if(keyword in report):
                    with io.open(keyword + ".txt", "w", encoding='utf-8') as f:
                        f.write(link['href'])

        except:
            with io.open("error.txt", "w", encoding='utf-8') as f:
                f.write(link)


def automation_anywhere(keyword):
    from requests_html import HTMLSession
    import io
    from tqdm import tqdm

    session = HTMLSession()

    page_content = session.get(
        'https://www.automationanywhere.com/resources/customer-stories?filters=hasLink')

    page_content.html.render(sleep=1, keep_page=True, scrolldown=1, timeout=20)
    cases = page_content.html.find('.storyInfoBox')

    links = []

    for case in cases:
        if(len(case.absolute_links) > 0):
            links.append(list(case.absolute_links)[0])

    session.close()

    for link in tqdm(links):
        try:
            session = HTMLSession()
            report = ""

            case_content = session.get(link)

            case_content.html.render(
                sleep=1, keep_page=True, scrolldown=1, timeout=20)

            elements = case_content.html.find('div')
            elements += case_content.html.find('p')
            elements += case_content.html.find('h1')
            elements += case_content.html.find('h2')
            elements += case_content.html.find('h3')

            for element in elements:
                report += element.text

            if(keyword in report):
                with io.open(keyword + ".txt", "w", encoding='utf-8') as f:
                    f.write(link)

            session.close()
        except:
            with io.open("error.txt", "w", encoding='utf-8') as f:
                f.write(link)


if __name__ == '__main__':
    keyword = input("keyword: ")
    uipath(keyword)
    automation_anywhere(keyword)
