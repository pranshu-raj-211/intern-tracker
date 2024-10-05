import os
import logging
import random
import time

import datetime
import yaml
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium.common.exceptions import TimeoutException, WebDriverException


# TODO: create loggers to do streamhandling and file handling
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d_%m_%y %H:%M:%S",
)


# ! there is a stray webdriver in here somewhere, find and remove to save resources and prevent tracing
# todo: refactor this whole file to be a lot more easier to understand
def init_driver():
    """Initiates a webdriver for firefox in headless mode."""
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options)


def load_config(config_path="src\scrapers\indeed_config.yaml"):
    """Load config params, including job titles and number of pages."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


config = load_config()


def get_jobs(soup):
    """
    Parses a soup object to get job data and return it as a list of dicts."""
    containers = soup.findAll("div", class_="job_seen_beacon")

    jobs = []
    for container in containers:
        job_title_element = container.find("h2", class_="jobTitle css-198pbd eu4oa1w0")
        company_element = container.find("span", {"data-testid": "company-name"})
        salary_element = container.find(
            "div", {"class": "metadata salary-snippet-container css-5zy3wz eu4oa1w0"}
        )
        location_element = container.find("div", {"data-testid": "text-location"})
        date_element = container.find("span", {"class": "css-qvloho eu4oa1w0"})

        job_title = job_title_element.text if job_title_element else None
        company = company_element.text if company_element else None
        salary = salary_element.text if salary_element else None
        location = location_element.text if location_element else None
        link = job_title_element.find("a")["href"] if job_title_element else None
        date = list(date_element.children)[-1] if date_element else None

        jobs.append(
            {
                "title": job_title,
                "company": company,
                "salary": salary,
                "location": location,
                "link": link,
                "date": date,
            }
        )
    return jobs


def save_scraped_jobs(jobs_df, title):
    """Saves scraped jobs to a database, currently using csv file for this purpose."""
    data_dir = config["data_dir"]
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    jobs_df.to_csv(f"{data_dir}/{current_date}.csv", index=False)
    logging.info(f"Saved jobs to {data_dir}/{current_date}.csv")


def scrape_jobs(driver, title):
    """Iterate over pages for each job title and collect data."""
    all_jobs = []
    base_url = config["base_url"].format(quote_plus(title))
    logging.info(f"Starting process - scrape {title} from indeed")
    time.sleep(20 + random.random() * 5)

    for i in range(config["num_pages"]):
        try:
            driver.get(base_url + "&start=" + str(i * 10))
        except TimeoutException:
            logging.exception(f"Timeout while loading url")
            continue
        except WebDriverException as e:
            logging.exception(f"WebDriverException: {e}")
            break

        driver.implicitly_wait(15)
        time.sleep(30 * random.random())
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        found_jobs = get_jobs(soup)
        all_jobs.extend(found_jobs)
    return all_jobs


def main():
    start_time = time.time()
    jobs_df = pd.DataFrame()
    driver = init_driver()

    try:
        for title in config["job_titles"]:
            all_jobs = scrape_jobs(driver, title)
            if all_jobs:
                df = pd.DataFrame(all_jobs)
                df["query"] = title
                df["source"] = "indeed"
                jobs_df = pd.concat([jobs_df, df], ignore_index=True)
                logging.info(f"Done with {title}, scraped {len(all_jobs)} jobs")
            else:
                logging.warning(f"No jobs found for {title}")

        save_scraped_jobs(jobs_df, title)
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    finally:
        driver.quit()

    end_time = time.time()
    logging.info(f"Done in {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
