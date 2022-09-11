import scraper
import parser

def get_chords(url: str, for_discord=False) -> str:
    """Returns the chords/lyrics from the tab in the url."""
    data: dict = scraper.json_from_url(url)
    ch = parser.UGTab(data, for_discord=for_discord)
    #need to return the metadata, formatted too somehow
    return ch._content