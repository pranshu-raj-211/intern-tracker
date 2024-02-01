import requests 
from bs4 import BeautifulSoup

with open('simplify.html') as f:
    soup=BeautifulSoup(f,'lxml')


# currently giving wrong output
class_containers=soup.find_all('div',class_='block')
for container in class_containers:
    title_element=container.find('h3',class_='text-base font-semibold')
    company_element=container.find('h4',class_='truncate text-xs')
    #company_link=container.find('a')
    location_element=container.find('p',class_='truncate text-xs')


    title = title_element.text.strip() if title_element else "Title not found"
    company = company_element.text.strip() if company_element else "Company not found"
    location = location_element.text.strip() if location_element else "Location not found"

    print(title,company,location)