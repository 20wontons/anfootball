import json
import requests
from bs4 import BeautifulSoup

DIV_CLASS = 'js-store'
URL = "https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421111"

def json_from_url(url: str) -> dict:
    """
    Extracts the data_content attribute from 
    the url's html, to access the tab's data, including
    tab info and content. Returns as a json.

    Parameters:
    - url:  the ultimate-guitar.com url as a string,
            compatible as of 2022/09/10
    
    Returns:
    - the JSON dict of the tab data
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find('body')
    
    cont = body.find('div', class_=DIV_CLASS)
    
    data_content = cont["data-content"]
    data_content.replace('&quot;', '\"')
    
    data_content_json = json.loads(data_content)
    return data_content_json
    # print(data_content_json["store"]["page"]["data"]["tab_view"]["wiki_tab"]["content"])


if __name__ == '__main__':
    json_from_url(URL)