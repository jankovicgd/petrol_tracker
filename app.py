import requests
from bs4 import BeautifulSoup
import datetime

URL = "https://www.oeamtc.at/spritapp/SimpleSearch.do"
PARAMS = {
    "selectedFuelType": "diesel",
    "sortBy": "price",
    "state": "Wien",
    "ZIP": "1200",
    "resultPageSize": "50",
    "spritaction": "doSimpleSearch",
}
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
STATIONS = ["BP express"]
DB = '/home/nikola/Personal/petrol_tracker/prices.csv'

def main():
    session = requests.Session()
    response = session.get(URL, headers=HEADERS)
    response = session.get(URL, headers=HEADERS, params=PARAMS)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    l = []

    now = datetime.datetime.now().isoformat()
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols)>=4 and cols[2] in STATIONS:
            l.append([cols[2], now, cols[4].replace(',', '.')])


    with open(DB, 'a') as f:
        for line in l:
            f.write(f"{line[0]},{line[1]},{line[2]}\n")

if __name__ == "__main__":
    main()
