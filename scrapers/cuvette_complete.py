import time
from selenium import webdriver
from bs4 import BeautifulSoup


# cuvette needs login, need a workaround for that
# maybe calling apis directly could work

def get_data(soup):
    """
    Extract data from a BeautifulSoup object and return it.
    This function should be customized for each specific scraping task.
    """
    containers = soup.findAll(
        "div", class_="StudentInternshipCard_innerContainer__3shqY"
    )

    jobs = []

    for container in containers:
        job_title_element = container.find("h3")
        job_title = job_title_element.text if job_title_element else None

        company_element = container.find("p")
        company = company_element.text if company_element else None

        info_divs = container.findAll("div", class_="StudentInternshipCard_info__1HW16")
        duration = None
        salary = None
        for div in info_divs:
            info_top = div.find("div", class_="StudentInternshipCard_infoTop__3yl8o")
            if info_top and "Duration" == info_top.text.strip():
                duration_element = div.find(
                    "div", class_="StudentInternshipCard_infoValue__E3Alf"
                )
                duration = duration_element.text if duration_element else None
            elif info_top and "Stipend per month" == info_top.text.strip():
                salary_element = div.find(
                    "div", class_="StudentInternshipCard_infoValue__E3Alf"
                )
                salary = salary_element.text if salary_element else None

        location_element = container.find(
            "div", class_="StudentInternshipCard_infoValue__E3Alf undefined"
        )
        location = location_element.text if location_element else None

        link = None

        date_card = container.find(
            "div", class_="StudentInternshipCard_currentInfoLeft__1jLNL"
        )
        date_element = date_card.find("p") if date_card else None
        date = date_element.text if date_element else None

        jobs.append(
            {
                "title": job_title,
                "company": company,
                "salary": salary,
                "location": location,
                "duration": duration,
                "link": link,
                "date": date,
            }
        )


def scrape_pages(base_url, num_pages):
    """
    Scrape multiple pages of a website using Selenium and BeautifulSoup.
    """

    driver = webdriver.Firefox()
    all_data = []

    for i in range(num_pages):
        driver.get(base_url +'&start='+ str(i * 10))
        driver.implicitly_wait(10)

        html = driver.page_source
        time.sleep(2)

        soup = BeautifulSoup(html, "html.parser")
        page_data = get_data(soup)
        all_data.extend(page_data)

    driver.quit()

    return all_data


def main():
    base_url = (
        "https://cuvette.tech/app/student/jobs/internships/filters?sortByDate=true"
    )

    num_pages = 5
    data = scrape_pages(base_url, num_pages)
    for item in data:
        print(item)


if __name__ == "__main__":
    main()
