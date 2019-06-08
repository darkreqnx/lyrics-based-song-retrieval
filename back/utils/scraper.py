from bs4 import BeautifulSoup as bs 
from requests import get
import log

def getGender(artist):
    artist = artist.replace(' ', '+')
    try:
        page = get("https://musicbrainz.org/search?query="+artist+"&type=artist&method=indexed")
        soup = bs(page.text, "html.parser")
        table = soup.find("tbody")
        table_rows = soup.find_all("tr")
        final_table=[]
        for tr in table_rows:
            td = tr.find_all("td")
            row = [i.text for i in td]
            final_table.append(row)
        return final_table[1][3]
    except Exception as e:
        log.writeExceptions(e, artist)