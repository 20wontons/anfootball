import json
import requests
from bs4 import BeautifulSoup

_DIV_CLASS = 'js-store'
_UG_URI = 'https://tabs.ultimate-guitar.com/tab/'
_UG_URI_LEN = 37

class InvalidLinkError(Exception):
    """Raised when the link is not an ultimate-guitar tab link."""
    pass

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

    Exceptions:
    - HTTPError:    if the page request does not return a successful
                    status code (200-299) then this exception will be raised
    """
    
    if not _link_has_ug_uri(url):
        raise InvalidLinkError("Link is not a tabs.ultimate-guitar.com link.")

    page = requests.get(url)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find('body')
    
    cont = body.find('div', class_=_DIV_CLASS)
    
    data_content = cont["data-content"]
    data_content.replace('&quot;', '\"')
    
    data_content_json = json.loads(data_content)
    return data_content_json


# for debugging
def write_dict_to_file(data: dict, path: str) -> None:
    f = open(path, 'w')
    json.dump(data, f)
    f.close()

def _link_has_ug_uri(url: str) -> bool:
    try:
        return url[:_UG_URI_LEN] == _UG_URI
    except IndexError:
        return False