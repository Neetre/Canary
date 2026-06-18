from bs4 import BeautifulSoup
import requests

url = "https://www.vesselfinder.com/ports/ITTRS001"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

session = requests.Session()
resp = session.get(url, headers=headers, timeout=30)

print(resp.status_code)
if resp.ok:
    soup = BeautifulSoup(resp.text, "html.parser")
    # print(soup.prettify())
    section = soup.find("section", id="expected")
    print(section)
    tables = section.find_all("table", class_=["ships-in-range", "table", "is-hoverable", "is-fullwidth"])
    for table in tables:
        tbody = table.find('tbody')
        if not tbody:
            continue
        rows = tbody.find_all('tr')
        for tr in rows:
            print(tr)