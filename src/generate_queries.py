import json


queries = []
job_title_tools = [
    ["python developer", "python", "django", "flask"],
    [
        "data analyst",
        "sql",
        "power bi",
        "r python",
    ],
    [
        "machine learning engineer",
        "scikit learn airflow",
        "pytorch tensorflow",
        "nltk",
    ],
    [
        "software engineer",
        "git",
        "integrated development environments ides",
        "selenium",
    ],
    [
        "backend developer",
        "rest",
        "postgresql mongodb",
        "nodejs django",
    ],
    [
        "devops engineer",
        "jenkins gitlab",
        "docker kubernetes",
        "terraform cloudformation",
    ],
    [
        "react developer",
        "reactjs",
        "javascript",
        "webpack",
    ],
    [
        "full stack developer",
        "react angular",
        "expressjs",
        "sql",
    ],
    [
        "mobile app developer",
        "flutter",
        "android studio",
        "cross platform development tools",
    ],
]

locations = [
    "",
    "hyderabad",
    "remote",
    "noida",
    "indore",
    "thane",
    "mumbai",
    "ahmedabad",
    "bengaluru",
    "chennai",
    "delhi",
    "pune",
]

for title in job_title_tools:
    for location in locations:
        unique_terms = list(set(title+[location]))
        queries.append(unique_terms)

with open("data/queries.json", "w") as f:
    json.dump({"query": queries}, f)
