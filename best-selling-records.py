import requests
from bs4 import BeautifulSoup
import pandas as pd


def max_len(s, l):
    return s if len(s) < l else s[0:l-3] + "..."

def parse_row(row):
    r = {} 
    tds = row.find_all("td")
    if tds[0].find("a"):
        r["Artist"] = tds[0].a.text
    else:
        r["Artist"] = tds[0].text
    r["Album"] = max_len(tds[1].a.text, 35)
    r["Released"] = tds[2].text.strip()
    genre = []
    for link in tds[3].find_all("a"):
        genre.append(link.text)
    genre_str = max_len(",".join(genre), 30)    
    r["Genre"] = genre_str
    r["Certified copies"] = tds[4].div.div.text
    r["Reported sales"] = tds[5].text.strip()
    return r

def parse_table(table):
    data = []
    for row in table.find_all("tr")[1:]:    
        data.append(parse_row(row))
    return data


r = requests.get("https://en.wikipedia.org/wiki/List_of_best-selling_albums")
soup = BeautifulSoup(r.text, 'html.parser')
tables = soup.find_all("table")

data = []
for table in tables[1:4]:
    data += parse_table(table)

df = pd.DataFrame(data)    

try:
    import tabulate
    print(df.to_markdown())
except ModuleNotFoundError:
    print(df.to_string())
