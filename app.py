import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Replace with your actual updated 'li_at' cookie
COOKIES = {
    "li_at": "your_updated_li_at_cookie"  # Ensure this is your actual, updated 'li_at' cookie
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"
}

def search_company(company_name):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={company_name} human resources"
    
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

def scrape_hr_profiles(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    hr_profiles = []
    
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

def scrape_profile_data(profile_url):
    profile_url = f"https://www.linkedin.com{profile_url}"  # Full profile URL
    response = requests.get(profile_url, cookies=COOKIES, headers=HEADERS)

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

def save_to_excel(data, filename="hr_profiles.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    company_name = input("Enter Company Name: ")
    html_content = search_company(company_name)
    
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
