from bs4 import BeautifulSoup
import requests
import streamlit as st

BASE_URL = "https://internshala.com/internships/"

preferences = {
    "custom": "matching-preferences/",
    0: "",
    "remote": "work-from-home-internships/",
    "part-time": "part-time-true/",
    2000: "stipend-2000/",
    4000: "stipend-4000/",
    6000: "stipend-6000/",
    8000: "stipend-8000/",
    10000: "stipend-10000/",
}


DATA_JOBS_URL = (
    BASE_URL
    + "work-from-home-big-data,data-analytics,data-science,machine-learning,python-internships/"
)


def get_page():
    return requests.get(DATA_JOBS_URL)


with open("internshala.html") as page:
    soup = BeautifulSoup(page, "lxml")


def find_jobs(soup):
    containers = soup.find_all("div", {"class": "internship_meta"})

    job_details = dict()
    counter = 1

    for container in containers:
        if counter == 1:
            counter += 1
            continue
        title = container.find("a", {"class": "view_detail_button"}).text
        link = container.find("a", {"class": "view_detail_button"})["href"]

        company = container.find(
            "a", {"class": "link_display_like_text view_detail_button"}
        ).text.strip()
        pay = container.find("span", {"class": "stipend"}).text
        # duration = container.find("div", {"class": "item_body"}).text

        job_details[f"job{counter}"] = {
            "title": title,
            "link": link,
            "pay": pay,
            "company": company,
            # "duration": duration,
        }
        counter += 1

    return job_details


def show_jobs(jobs):
    st.title("Internships at Internshala")
    for job in jobs:
        st.write(
            f'<b>{jobs[job]["title"]}</b><div>{jobs[job]["company"]}</div><p>Pay : {jobs[job]["pay"]}</p><p><a href= {jobs[job]["link"]}>Apply</a></p>',
            unsafe_allow_html=True,
        )


def main():
    jobs = find_jobs(soup)
    show_jobs(jobs)


if __name__ == "__main__":
    main()
