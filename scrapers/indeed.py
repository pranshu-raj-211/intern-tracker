import requests 
from bs4 import BeautifulSoup

with open('indeed.html') as f:
    soup=BeautifulSoup(f,'lxml')


class_container=soup.find('div',class_='job_seen_beacon')

for container in class_container:
    link_element=container.find('a')
    company_element=container.find('div',class_='company_location')

    if company_element:
        company=company_element.find('span')
        company_location=company_element.find('div',class_='t4u72d')
    else:
        company=None
        company_location=None

    metadata_element=container.find('div',class_='heading6')
    salary_element=container.find('div',class_='css-lihavw2 eu4oalw0')
    posted_element=container.find('span',class_='date')

    #extra_details=container.find('div',class_='job-snippet')

    link=link_element.text.strip() if link_element else 'No link'
    posted=posted_element.text.strip() if posted_element else 'umu'
    company=company.text.strip() if company else 'No company too lol'
    print(link,company,company_location,posted)

