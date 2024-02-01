from bs4 import BeautifulSoup
import streamlit as st
import requests
import os

base_url = "https://cuvette.tech/app/student/jobs/internships"
refresh_jobs = False

with open("cuvette.html") as page:
    soup = BeautifulSoup(page, "lxml")


def get_page(url):
    return requests.get(url)


def find_jobs(soup):
    job_containers = soup.find_all(
        "div", {"class": "BrowseInternship_cardsContainer__W8lvl"}
    )

    job_details = dict()
    counter = 0

    for _ in job_containers:
        inner_container = soup.find(
            "div", {"class": "StudentInternshipCard_innerContainer__3shqY"}
        )
        job_header = inner_container.find(
            "div", {"class": "StudentInternshipCard_left__2Ju1U"}
        )
        title = job_header.find("h3").contents[0]
        if " Internship" in title:
            title = title.split("Internship")[0]

        recruiter = job_header.find("p").contents[0]
        company, company_location = recruiter.split(" | ")
        if ", India" in company_location:
            company_location = company_location.split(", India")[0]

        mode = inner_container.find(
            "label",
            {"class": "StudentInternshipCard_blueLabel__1UMD-"},
        ).contents[0]

        level = inner_container.find("p", {"class": "sc-jJEKmz"}).contents[0]

        pay = inner_container.find(
            "div", {"class": "StudentInternshipCard_infoValue__E3Alf"}
        ).contents[0]

        date_info = (
            inner_container.find(
                "div", {"class": "StudentInternshipCard_currentInfoLeft__1jLNL"}
            )
            .find("p")
            .contents[0]
        )

        # cannot find links to jobs, will need to improvise

        job_details[f"job_{counter}"] = {
            "role": title,
            "company": company,
            "based": company_location,
            "mode": mode,
            "level": level,
            "pay": pay,
            "dates": date_info,
        }
        counter += 1


def display_jobs(job_details: dict):
    for details in job_details.values():
        st.write(f'<h3>{details["role"]}</h3>', unsafe_allow_html=True)
        st.write(
            f'{details["company"]}\t |\t {details["based"]}\n{details["mode"]}\n{details["pay"]}'
        )


def main():
    if refresh_jobs:
        curr = os.getcwd()
        os.chdir(curr + "cache/")
        os.remove(os.getcwd() + "cuvette.html")


# i want to refresh page content by downloading every set interval or so
