import requests 
from bs4 import BeautifulSoup

with open('simplify.html') as f:
    soup=BeautifulSoup(f,'lxml')

class_containers=soup.find('div',class_='block')
detail_block=class_containers.find('div',class_='mt-4')

title_element = class_containers.find('h3', class_='text-base font-semibold')
company_element = soup.find('h4', class_='truncate text-xs')
location_element = soup.find('p', class_='truncate text-xs')

title = title_element.text.strip() if title_element else "Title not found"
company = company_element.text.strip() if company_element else "Company not found"
location = location_element.text.strip() if location_element else "Location not found"

print(f"Title: {title}")
print(f"Company: {company}")
print(f"Location: {location}")