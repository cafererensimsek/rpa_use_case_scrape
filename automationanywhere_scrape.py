import requests
from bs4 import BeautifulSoup

cases = []

for i in range(1):
    page_content = BeautifulSoup(requests.get('https://www.automationanywhere.com/resources/customer-stories').content, 'lxml').find_all('div', {'class': 'storyInfoBox'})

    print(page_content)