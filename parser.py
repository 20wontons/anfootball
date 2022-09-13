class UGTabInfo():
    """
    An Ultimate-Guitar Tab Info object, which defines
    all of the metadata for a tab.
    
    Instance Variables:
    - tab_id:   int   | the id of the specific tab
    - tab_url:  str   | the url to the tab
    - artist:   str   | the artist name that wrote the song
    - song:     str   | the song title
    - tuning:   str or None
                      | the guitar tuning for the tab,
                        tunings could sometimes be included in the tab contents,
                        otherwise, if None, it could be assumed to be standard
    - key:      str or None
                      | the key of the song
    - capo:     int or None
                      | the capo setting for the tab,
                        capo settings could sometimes be included in the tab contents,
                        otherwise, if None, it could be assumed to be 0
    """

    def __init__(self, data: dict):
        tab_info: dict = data['store']['page']['data']['tab']
        self._tab_id: int = tab_info['id']
        self._tab_url: str = tab_info['tab_url']
        self._artist: str = tab_info['artist_name']
        self._song: str = tab_info['song_name']
        
        # the following meta fields could be None
        tab_meta: dict = data['store']['page']['data']['tab_view']['meta']
        self._tuning: str or None = tab_meta.get('tuning')['value'] if tab_meta.get('tuning') is not None else None
        self._key: str or None = tab_meta.get('tonality')
        self._capo: int or None = tab_meta.get('capo')
    
    def get_tab_id(self) -> int:
        return self._tab_id
    
    def get_tab_url(self) -> str:
        return self._tab_url
    
    def get_artist(self) -> str:
        return self._artist
    
    def get_song(self) -> str:
        return self._song
    
    def get_tuning(self) -> str or None:
        return self._tuning
    
    def get_key(self) -> str or None:
        return self._key

    def get_capo(self) -> int or None:
        return self._capo


class UGTab():
    """
    An Ultimate-Guitar Tab object, which defines
    the tab info and metadata, and the tab contents, 
    including the chords and lyrics.

    Instance Variables:
    - info:     UGTabInfo | the tab info and metadata, in a UGTabInfo object
    - content:  str       | the tab content, which includes the formatted chords and lyrics
    - for_discord: bool   | if True, then the chords in the formatted contents will be bolded by Discord syntax.
                            if False, then the chords will be plaintext unformatted.
    """
    # TODO: add version description
    def __init__(self, data: dict, for_discord: bool = False):
        self._info: UGTabInfo = UGTabInfo(data)
        self._for_discord: bool = for_discord
        self._content: str = self._format_content(data['store']['page']['data']['tab_view']['wiki_tab']['content'])
        
    
    def _format_content(self, content: str) -> str:
        content = content.replace('[ch]', '**' if self._for_discord else '', -1)
        content = content.replace('[/ch]', '**' if self._for_discord else '', -1)
        content = content.replace('[tab]', '', -1)
        content = content.replace('[/tab]', '', -1)
        content = content.replace('\r', '', -1)
        return content

    def get_content(self) -> str:
        return self._content
    
    def write_content_to_file(self, path: str):
        f = open(path, 'w')
        f.write(self._content)
        f.close()

    # getting the tab info
    def get_tab_id(self) -> int:
        return self._info.get_tab_id()
    
    def get_tab_url(self) -> str:
        return self._info.get_tab_url()
    
    def get_artist(self) -> str:
        return self._info.get_artist()
    
    def get_song(self) -> str:
        return self._info.get_song()
    
    def get_tuning(self) -> str or None:
        return self._info.get_tuning()
    
    def get_key(self) -> str or None:
        return self._info.get_key()

    def get_capo(self) -> int or None:
        return self._info.get_capo()

    def get_formatted_metadata(self) -> str:
        md = []
        if self.get_tuning() is not None:
            md.append("Tuning: " + self.get_tuning())
        if self.get_key() is not None:
            md.append("Key: " + self.get_key())
        if self.get_capo() is not None:
            md.append("Capo: " + str(self.get_capo()))
        return '\n'.join(md)


class UGSearchResult():
    """
    An Ultimate-Guitar Search Result object, 
    which defines all of the metadata for a search result;
    only supported for Chords and Tabs types
    
    Instance Variables:
    - tab_url:  str   | the url to the tab
    - artist:   str   | the artist name that wrote the song
    - song:     str   | the song title
    - type:     str   | could be Chords or Tab
    - votes:    int   | the number of votes for the tab
    - rating:   float | the rating for the tab, out of 5
    """
    def __init__(self, data: dict):
        self._tab_url: str = data['tab_url']
        self._artist: str = data['artist_name']
        self._song: str = data['song_name']
        self._type: str = data['type']
        self._votes: int = data['votes']
        self._rating: float = data['rating']
    
    def get_tab_url(self) -> str:
        return self._tab_url
    
    def get_artist(self) -> str:
        return self._artist
    
    def get_song(self) -> str:
        return self._song
    
    def get_type(self) -> str:
        return self._type
    
    def get_votes(self) -> int:
        return self._votes
    
    def get_rating(self) -> float:
        return self._rating

    def get_formatted_result_description(self) -> str:
        # TODO: add version description
        return f"**Rating:** `{self._rating}`\n" \
                + f"**Votes:** `{self._votes}`\n\n" \
                + f"**Link**\n{self._tab_url}"


class UGSearch():
    """
    An Ultimate-Guitar Search object,
    which parses the search results from a JSON,
    and can return the Chords results or Tabs results.

    Instance Variables:
    - raw_results:  list[dict]  | the search results as a list of results with data
    """
    # TODO: maybe look into https://stats.stackexchange.com/questions/6418/rating-system-taking-account-of-number-of-votes
    sort_key = lambda x: x.get_votes()

    def __init__(self, data: dict):
        self._raw_results: list[dict] = data["store"]["page"]["data"]["results"]

    def get_chords_results(self) -> list[UGSearchResult]: 
        ch_r = []
        for r in self._raw_results:
            try:
                if r['type'] == "Chords":
                    ch_r.append(UGSearchResult(r))
            except KeyError:
                pass
        ch_r.sort(reverse=True, key=UGSearch.sort_key)
        return ch_r
    
    def get_tab_results(self) -> list[UGSearchResult]:
        t_r = []
        for r in self._raw_results:
            try:
                if r['type'] == "Tabs":
                    t_r.append(UGSearchResult(r))
            except KeyError:
                pass
        t_r.sort(reverse=True, key=UGSearch.sort_key)
        return t_r