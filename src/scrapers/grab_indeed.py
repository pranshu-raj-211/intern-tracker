import os
import logging
import random
import time
import datetime
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium.common.exceptions import TimeoutException



logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d_%m_%y %H:%M:%S')
# this works well
driver = webdriver.Firefox()

job_titles = [
    "python developer",
    "data analyst",
    "machine learning intern",
    "software engineer",
    "backend developer",
    "devops engineer",
    "automation engineer",
    #"network engineer",
    #"vuejs developer",
    # "react developer",
    # "nodejs developer",
    # "frontend developer",
    # "full stack developer",
    #"ui developer",
    #"web application developer",
    #"javascript engineer",
    #"mobile app developer",
    ]

# pagination limits
num_pages = 5
current_date = datetime.datetime.now().strftime('%Y_%m_%d')
random.seed(int(datetime.datetime.now().strftime('%d')))
start_time = time.time()

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

for title in job_titles:
    all_jobs = []
    base_url = f"https://in.indeed.com/jobs?q={quote_plus(title)}&from=searchOnHP"

    logging.info(f'Starting process - scrape {title} from indeed')
    time.sleep(20+random.random()*5)

    for i in range(num_pages):
        try:
            driver.get(base_url + '&start='+ str(i*10))
        except TimeoutException:
            logging.exception(f'Timeout while loading url')
        # implicit wait - stops when page loads or time is over
        driver.implicitly_wait(15)
        # TODO: I should add in some random delay here
        time.sleep(30*random.random())
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        found_jobs = get_jobs(soup)
        all_jobs.extend(found_jobs)

    # Create directory if it doesn't exist
    directory = os.path.join(os.getcwd(),f'data/indeed/{current_date}')
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(os.path.exists(directory))
    logging.info(f'saving to {directory}')

    # Write to CSV
    fieldnames = all_jobs[0].keys()
    df = pd.DataFrame(all_jobs)
    df.to_csv(f'{directory}/{title.replace(" ", "_")}.csv', index=False)
    
    logging.info(f'Done with {title}, scraped {len(all_jobs)} jobs')

driver.quit()
end_time = time.time()

logging.info(f'Done in {end_time-start_time} seconds')