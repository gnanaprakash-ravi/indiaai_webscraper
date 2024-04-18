import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://indiaai.gov.in/startup/aircto"

with open('startup_links.txt', 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

# Send an HTTP request and get the page content
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def safe_extract(soup, tag, text, next_tag):
    try:
        return soup.find(tag, text=text).find_next(next_tag).text.strip()
    except AttributeError:
        return None

# with open('output2.txt', 'w', encoding='utf-8') as file:
#     file.write(str(soup))

all_startup_data = []

for url in urls:

    startup_data = {
        "Name": [],
        "Founded": [],
        "People": [],
        "Location": [],
        "Sector": [],
        "Technology": [],
        "Business Function": [],
        "Business Model": [],
        "About": [],
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    startup_cards = soup.find_all("div", class_="startup-details")

    startup_data["Name"] = soup.find("h4", class_="startup-name").text.strip()

    metadata = soup.find_all("span", class_="md__founded")
    startup_data["Founded"] = None
    for item in metadata:
        if "Founded" in item.text:
            startup_data["Founded"] = item.find("b").text.strip()
            break

    people_info = soup.find("span", class_="md__people")
    if people_info:
        startup_data["People"] = people_info.find("b").text.strip()
    else:
        startup_data["People"] = None

    location = soup.find("span", class_="md__location")
    if location:
        location = location.find("b").text.strip()
        startup_data["Location"] = location.replace("\n", "").replace(" ", "")
    else:
        startup_data["Location"] = None

    startup_data["Sector"] = safe_extract(soup, "th", "Sector", "td")
    startup_data["Technology"] = safe_extract(soup, "th", "Technology", "td")
    startup_data["Business Function"] = safe_extract(soup, "th", "Business Function", "td")
    startup_data["Business Model"] = safe_extract(soup, "th", "Business Model", "td")

    startup_data["About"] = soup.find("h2", id="start_up_profile").find_next("p").text.strip()

    print("Startup Name:", startup_data["Name"])
    print("Founded Year:", startup_data["Founded"])
    print("Location:", startup_data["Location"])
    print("Sector:", startup_data["Sector"])
    print("Technology:", startup_data["Technology"])
    print("Business Function:", startup_data["Business Function"])
    print("Business Model:", startup_data["Business Model"])
    print("About:", startup_data["About"])

    all_startup_data.append(startup_data)


df = pd.DataFrame(all_startup_data)
print(df.head())

df.to_excel("startup_data_Test.xlsx", index=False)
print("Data written to startup_data.xlsx")