# LinkedIn HR Scraper

This Python script scrapes HR profiles from LinkedIn using a search query for a given company. 
The script collects profile data such as the name, job title, and a brief description of HR professionals working at that company.
The data is saved to an Excel file for easy viewing.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Required Python libraries (can be installed via pip)

pip install requests beautifulsoup4 pandas
Setup
Obtain LinkedIn Cookies:

Log in to LinkedIn in your web browser.
Open Developer Tools (Ctrl+Shift+I or Cmd+Option+I on Mac).
Go to the Application tab, find Cookies, and copy the value of the li_at cookie. This is required for authenticating requests.
Update Cookies:

In the script, replace the placeholder your_updated_li_at_cookie in the COOKIES dictionary with the li_at cookie value from your browser.
Install Dependencies:

Install the required Python libraries using the command:
bash
Copy
Edit
pip install requests beautifulsoup4 pandas
Run the Script:

Run the script with the following command:
bash
Copy
Edit
python linkedin_hr_scraper.py
Enter Company Name:

When prompted, enter the name of the company whose HR profiles you want to scrape (e.g., "Apple").
Output:

The script will search for HR professionals working at the entered company on LinkedIn and scrape their basic profile information (name, job title, about).
The data will be saved to an Excel file (hr_profiles.xlsx).
Features
Search by Company: Scrape profiles of HR professionals working at a specific company.
Profile Details: Extract names, titles, and about sections.
Export to Excel: Saves the scraped data in an Excel file (hr_profiles.xlsx).
Troubleshooting
Redirects: If LinkedIn redirects you, make sure your li_at cookie is up to date.
Blocked Requests: LinkedIn may block repeated scraping attempts. If this happens, consider using a proxy service or rotating your IP.
Rate Limiting: A 2-second delay is added between profile fetches to avoid rate limiting.
Notes
This scraper is intended for educational purposes. Please use LinkedIn's data in accordance with their Terms of Service.
The script uses a basic scraping approach and may be blocked by LinkedIn's anti-scraping measures.
Future Improvements
Support for handling paginated results in case there are more than 10 profiles.
Adding proxy rotation to avoid IP blocking.
Integration with LinkedIn’s official API (if API access is granted).
License
This project is licensed under the MIT License - see the LICENSE file for details. """

import requests from bs4 import BeautifulSoup import pandas as pd import time

Replace with your actual updated 'li_at' cookie
COOKIES = { "li_at": "your_updated_li_at_cookie" # Ensure this is your actual, updated 'li_at' cookie }

HEADERS = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1", "TE": "Trailers" }

def search_company(company_name): search_url = f"https://www.linkedin.com/search/results/people/?keywords={company_name} human resources"

python
Copy
Edit
# Disable automatic redirects to inspect the redirection URL
response = requests.get(search_url, cookies=COOKIES, headers=HEADERS, allow_redirects=False, timeout=5)

if response.status_code == 302:
    print(f"Redirected to: {response.headers['Location']}")
    print(f"Response content: {response.content[:500]}...")  # Print the first 500 chars of content to inspect the redirect page
    return None
elif response.status_code == 200:
    return response.text
else:
    print(f"Failed to fetch search results. Status code: {response.status_code}")
    return None
def scrape_hr_profiles(html_content): soup = BeautifulSoup(html_content, "html.parser") hr_profiles = []

arduino
Copy
Edit
profiles = soup.find_all("div", class_="entity-result")
for profile in profiles[:10]:  # Limit to 10 profiles
    try:
        name = profile.find("span", class_="entity-result__title-text").text.strip()
        profile_link = profile.find("a")["href"]
        about = profile.find("p", class_="entity-result__summary").text.strip() if profile.find("p", class_="entity-result__summary") else "No About Info"
    except AttributeError:
        continue
    
    hr_profiles.append({"Name": name, "About": about, "Profile Link": profile_link})

return hr_profiles
def scrape_profile_data(profile_url): profile_url = f"https://www.linkedin.com{profile_url}" # Full profile URL response = requests.get(profile_url, cookies=COOKIES, headers=HEADERS)

python
Copy
Edit
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Example of extracting name, title, and about section
    try:
        name = soup.find("h1").text.strip()  # Name of the profile
        title = soup.find("h2").text.strip()  # Job title
        about_section = soup.find("section", class_="pv-about-section")  # About section
        about = about_section.text.strip() if about_section else "No About Info"
        return {"Name": name, "Title": title, "About": about}
    except AttributeError:
        return None
else:
    print(f"Failed to access profile: {profile_url}")
    return None
def save_to_excel(data, filename="hr_profiles.xlsx"): df = pd.DataFrame(data) df.to_excel(filename, index=False) print(f"Data saved to {filename}")

if name == "main": company_name = input("Enter Company Name: ") html_content = search_company(company_name)

python
Copy
Edit
if html_content:
    hr_profiles = scrape_hr_profiles(html_content)
    detailed_profiles = []

    for profile in hr_profiles:
        print(f"Fetching details for {profile['Name']}")
        profile_data = scrape_profile_data(profile['Profile Link'])
        if profile_data:
            detailed_profiles.append(profile_data)
        time.sleep(2)  # Adding a delay to avoid making too many requests in a short time
    
    if detailed_profiles:
        save_to_excel(detailed_profiles)
    else:
        print("No detailed profiles found.")
else:
    print("No profiles found.")
markdown
Copy
Edit

### Explanation:
- The `README.md` contents are included as a **docstring** at the top of the Python file to provide instructions and guidelines directly inside the code.
- **Installation**, **usage**, and **troubleshooting** instructions are part of the docstring, so anyone who opens the file can easily understand how to set it up and use it.

### Next Steps:
- Save this script in your project folder as `linkedin_hr_scraper.py` and make sure the `README.md` file is also in your project folder or included in the comments as above.
- When you run the script, it will function as described in the instructions.

Let me know if you need more assistance!

