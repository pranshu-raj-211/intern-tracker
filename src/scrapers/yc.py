import time
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import pandas as pd
import datetime


date = datetime.datetime.now().strftime("%Y_%m_%d")

def get_data(soup):
    containers = soup.findAll(
        "div",
        class_="mb-1 flex flex-col flex-nowrap items-center justify-between gap-y-2 md:flex-row md:gap-y-0",
    )

    jobs = []
    for container in containers:
        job_title_element = container.find("a", class_="font-semibold text-linkColor")

        if job_title_element:
            job_title = job_title_element.text
            link = job_title_element['href']

        company_element = container.find("span", class_="block font-bold md:inline")
        if company_element:
            company = company_element.text

        location_element = container.find(
            "div",
            class_="border-r border-gray-300 px-2 first-of-type:pl-0 last-of-type:border-none last-of-type:pr-0",
        )
        if location_element:
            location = location_element.text

        date_posted_element = container.find('span', class_='hidden text-sm text-gray-400 md:inline')
        if date_posted_element:
            date_posted = date_posted_element.text.strip().split('(')[1].split(')')[0]
        jobs.append(
            {
                "title": job_title,
                "company": company,
                "location": location,
                "link": link,
                "date": date_posted,
            }
        )
    jobs = pd.DataFrame(jobs)
    return jobs

def scrape_pages(base_url, num_pages):
    driver = webdriver.Firefox()
    all_data = pd.DataFrame()

    for _ in range(num_pages):
        driver.get(base_url)
        driver.implicitly_wait(15)
        html = driver.page_source
        time.sleep(3 + random.random() * 10)
        soup = BeautifulSoup(html, 'html.parser')
        page_data = get_data(soup)
        all_data = pd.concat([all_data, page_data])

    driver.quit()

    return all_data

def main():
    base_url = "https://www.ycombinator.com/jobs/role"
    num_pages = 1
    data = scrape_pages(base_url, num_pages)

    data.to_csv(f"data/yc/{str(date)}.csv", index=False)

if __name__ == "__main__":
    main()