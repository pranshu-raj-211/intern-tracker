from bs4 import BeautifulSoup
import json

# Your larger HTML document content
with open('indeed.html') as f:
    soup=BeautifulSoup(f,'lxml')


# Find all job snippet divs
job_snippets = soup.find_all('div', class_='job_seen_beacon')

# Create a list to store job details
jobs_list = []

# Extract information from each job snippet
for job_snippet in job_snippets:
    title_element = job_snippet.find('span', id=lambda value: value and value.startswith('jobTitle'))
    company_element = job_snippet.find('span', class_='css-1x7z1ps eu4oa1w0')
    location_element = job_snippet.find('div', class_='css-t4u72d eu4oa1w0')
    additional_info_elements = job_snippet.select('.job-snippet li')

    # Extract text content from elements
    title = title_element.text.strip() if title_element else "Title not found"
    company = company_element.text.strip() if company_element else "Company not found"
    location = location_element.text.strip() if location_element else "Location not found"
    additional_info = [info.text.strip() for info in additional_info_elements] if additional_info_elements else []

    # Store job details in a dictionary
    job_details = {
        "Title": title,
        "Company": company,
        "Location": location,
        "Additional Information": additional_info
    }

    # Append job details to the list
    jobs_list.append(job_details)

print(jobs_list)

# Store job details in a JSON object
#jobs_json = json.dumps(jobs_list, indent=2)

# Print or save the JSON object
#print(jobs_json)

# If you want to save the JSON object to a file
# with open('jobs_data.json', 'w') as file:
#     json.dump(jobs_list, file, indent=2)
