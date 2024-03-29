import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

_DIV_CLASS = 'js-store'
_UG_TAB_URI     = "https://tabs.ultimate-guitar.com/tab/"
_UG_TAB_URI_LEN = 37
_UG_SEARCH_URI  = "https://www.ultimate-guitar.com/"
_UG_SEARCH_URI_LEN = 32

SAMPLE_SEARCH="https://www.ultimate-guitar.com/search.php?search_type=title&value=beach%20weather%20chit%20chat"


class InvalidLinkError(Exception):
    """Raised when the link is not an ultimate-guitar tab link."""
    pass


def json_from_url(url: str) -> dict:
    """
    Extracts the data_content attribute from 
    the url's html, to access the page's data.

    Parameters:
    - url:  the ultimate-guitar.com url as a string,
            compatible as of 2022/09/10
    
    Returns:
    - the JSON dict of the tab data

    Exceptions:
    - HTTPError:    if the page request does not return a successful
                    status code (200-299) then this exception will be raised
    - InvalidLinkError: Raised when the link is not an ultimate-guitar tab link.
    """
    
    if not _link_has_ug_uri(url):
        raise InvalidLinkError(f"`{url}` is not a valid link.")

    page = requests.get(url)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, "html.parser")
    body = soup.find('body')
    
    cont = body.find('div', class_=_DIV_CLASS)
    
    data_content = cont["data-content"]
    data_content.replace('&quot;', '\"')
    
    data_content_json = json.loads(data_content)
    return data_content_json


def json_from_search(artist: str, song: str = None) -> dict:
    """
    Extracts the data_content attribute from 
    the url's html, to access the page's data.

    Parameters:
    - artist:   the artist name
    - song:     the song name (can be None if searching by artist)
    
    Returns:
    - the JSON dict of the search results

    Exceptions:
    - HTTPError:    if the page request does not return a successful
                    status code (200-299) then this exception will be raised
    - InvalidLinkError: Raised when the link is not an ultimate-guitar tab link.
    """
    if song:
        query = artist.strip() + " " + song.strip()
        url = _UG_SEARCH_URI + "search.php?search_type=title&value=" + urllib.parse.quote(query)
    else:
        query = artist.strip()
        url = _UG_SEARCH_URI + "search.php?search_type=band&value=" + urllib.parse.quote(query)
    return json_from_url(url)


def json_from_explore(option: str) -> dict:
    """
    Extracts the data_content attribute from 
    the url's html, to access the page's data.

    Parameters:
    - option:   the explore option
    
    Returns:
    - the JSON dict of the search results

    Exceptions:
    - HTTPError:    if the page request does not return a successful
                    status code (200-299) then this exception will be raised
    - InvalidLinkError: Raised when the link is not an ultimate-guitar tab link.
    """
    query = option.strip()
    url = _UG_SEARCH_URI + "explore?order=" + urllib.parse.quote(query)
    return json_from_url(url)


def json_from_artist(artist_url: str) -> dict:
    """
    Extracts the data_content attribute from 
    the url's html, to access the page's data.

    Parameters:
    - artist_url:   the artist url
    
    Returns:
    - the JSON dict of the search results

    Exceptions:
    - HTTPError:    if the page request does not return a successful
                    status code (200-299) then this exception will be raised
    - InvalidLinkError: Raised when the link is not an ultimate-guitar tab link.
    """
    query = artist_url.strip()[1:]
    url = _UG_SEARCH_URI + urllib.parse.quote(query)
    return json_from_url(url)


# for debugging
def write_dict_to_file(data: dict, path: str) -> None:
    """Writes the JSON dict to a file."""
    f = open(path, 'w')
    json.dump(data, f)
    f.close()


def _link_has_ug_uri(url: str) -> bool:
    """Checks if the given URL contains an ultimate-guitar tab or search URI."""
    try:
        return url[:_UG_TAB_URI_LEN] == _UG_TAB_URI or url[:_UG_SEARCH_URI_LEN] == _UG_SEARCH_URI
    except IndexError:
        return False
