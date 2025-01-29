#NAUKRI
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_company_hr_details(company_name):
    query = company_name.replace(" ", "-").lower()
    url = f"https://www.naukri.com/{query}-hr-jobs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to retrieve page, status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("article", class_="jobTuple")

    hr_data = []

    for job in jobs:
        try:
            company = job.find("a", class_="subTitle").text.strip()
            title = job.find("a", class_="title").text.strip()
            location = job.find("li", class_="location").text.strip()
            experience = job.find("li", class_="experience").text.strip() if job.find("li", class_="experience") else "Not mentioned"
            job_desc = job.find("div", class_="job-description").text if job.find("div", class_="job-description") else "No description"

            email = "Not found"
            words = job_desc.split()
            for word in words:
                if "@" in word and "." in word:
                    email = word
                    break

            hr_data.append([company, title, location, experience, email])

        except Exception as e:
            print(f"Skipping job due to error: {e}")


    df = pd.DataFrame(hr_data, columns=["Company", "Job Title", "Location", "Experience", "HR Email"])
    filename = f"hr_details_{company_name.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False, encoding="utf-8")

    print(f"HR details saved in '{filename}'")

company_name = input("Enter the company name (e.g., 'TCS', 'Infosys'): ")
scrape_company_hr_details(company_name)
