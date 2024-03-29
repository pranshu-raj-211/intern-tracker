from typing import Dict, List
from bs4 import BeautifulSoup
from scraper import Scraper


class IndeedScraper(Scraper):
    def __init__(self, url: str, pagination_limit: int, source="indeed"):
        super.__init__(url, pagination_limit, source)

    def parse_soup(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Parses the soup object generated after scraping html.

        Args:
            soup (BeautifulSoup): Soup object required for parsing elements.
        Returns:
            jobs (List): A list of all jobs found in the soup object.
        """
        containers = soup.findAll("div", class_="job_seen_beacon")

        jobs = []
        for container in containers:
            job_title_element = container.find(
                "h2", class_="jobTitle css-14z7akl eu4oa1w0"
            )
            company_element = container.find("span", {"data-testid": "company-name"})
            salary_element = container.find(
                "div",
                {"class": "metadata salary-snippet-container css-5zy3wz eu4oa1w0"},
            )
            location_element = container.find("div", {"data-testid": "text-location"})
            # date_element = container.find("span", {"class": "css-qvloho eu4oa1w0"})
            # todo: add date parser, till then use date posted with sort by date filter

            job_title = job_title_element.text if job_title_element else None
            company = company_element.text if company_element else None
            salary = salary_element.text if salary_element else None
            location = location_element.text if location_element else None
            link = job_title_element.find("a")["href"] if job_title_element else None

            jobs.append(
                {
                    "title": job_title,
                    "company": company,
                    "salary": salary,
                    "location": location,
                    "source": self.source,
                    "link": link,
                    "date_sourced": self.date,
                }
            )
        return jobs
