import time
from selenium import webdriver
from bs4 import BeautifulSoup

# this works well
driver = webdriver.Firefox()
base_url = "https://in.indeed.com/jobs?q=machine+learning&l=Remote&from=searchOnHP"


jobs =[]

def get_jobs(soup):
    containers = soup.findAll('div', class_='job_seen_beacon')

    jobs = []
    for container in containers:
        job_title_element = container.find('h2', class_='jobTitle css-14z7akl eu4oa1w0')
        company_element = container.find('span', {'data-testid': 'company-name'})
        salary_element = container.find('div', {'class': 'metadata salary-snippet-container css-5zy3wz eu4oa1w0'})
        location_element = container.find('div', {'data-testid': 'text-location'})
        date_element = container.find('span', {'class': 'css-qvloho eu4oa1w0'})

        job_title = job_title_element.text if job_title_element else None
        company = company_element.text if company_element else None
        salary = salary_element.text if salary_element else None
        location = location_element.text if location_element else None
        link = job_title_element.find('a')['href'] if job_title_element else None
        date = list(date_element.children)[-1] if date_element else None

        jobs.append({
            'title': job_title,
            'company': company,
            'salary': salary,
            'location': location,
            'duration':'Not specified',
            'link': link,
            'date': date
        })
    return jobs

# pagination limits
num_pages = 5
all_jobs = []

for i in range(num_pages):
    driver.get(base_url + '&start='+ str(i*10))
    # implicit wait - stops when page loads or time is over
    driver.implicitly_wait(15)
    # TODO: I should add in some random delay here
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'html.parser')

    found_jobs = get_jobs(soup)
    all_jobs.extend(found_jobs)

driver.quit()

for job in all_jobs:
    print(job)

# TODO: Add code to push data to a csv/pipeline