class UGTabInfo():
    """
    An Ultimate-Guitar Tab Info object, which defines
    all of the metadata for a tab.
    
    Instance Variables:
    - tab_id:   int   | the id of the specific tab
    - type:     str   | the type of tab (Chords or Tabs)
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
        self._type: str = tab_info['type']
        self._tab_url: str = tab_info['tab_url']
        self._artist: str = tab_info['artist_name']
        self._song: str = tab_info['song_name']
        
        # the following meta fields could be None
        tab_meta: dict = data['store']['page']['data']['tab_view']['meta']
        self._tuning: str or None = tab_meta.get('tuning')['value'] if type(tab_meta) is dict and tab_meta.get('tuning') is not None else None
        self._key: str or None = tab_meta.get('tonality') if type(tab_meta) is dict else None
        self._capo: int or None = tab_meta.get('capo') if type(tab_meta) is dict else None
    
    def get_tab_id(self) -> int:
        return self._tab_id
    
    def get_type(self) -> str:
        return self._type
    
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
    the tab info and metadata, and the tab contents.

    Instance Variables:
    - info:     UGTabInfo | the tab info and metadata, in a UGTabInfo object
    - content:  str       | the tab content, which includes the formatted chords and lyrics
    """
    # TODO: add version description
    def __init__(self, data: dict):
        self._info: UGTabInfo = UGTabInfo(data)
        self._content: str = self._format_content(data['store']['page']['data']['tab_view']['wiki_tab']['content'])
        
    
    def _format_content(self, content: str, fchords: bool = True) -> str:
        if fchords:
            content = content.replace('[ch]', '', -1)
            content = content.replace('[/ch]', '', -1)
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
    
    def get_type(self) -> int:
        return self._info.get_type()
    
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
        md = [self.get_type()+" ID: "+str(self.get_tab_id())]
        if self.get_tuning() is not None:
            md.append("Tuning: " + self.get_tuning())
        if self.get_key() is not None:
            md.append("Key: " + self.get_key())
        if self.get_capo() is not None:
            md.append("Capo: " + str(self.get_capo()))
        return '\n'.join(md)



class UGChords(UGTab):
    """
    An Ultimate-Guitar Tab object, which defines
    the tab info and metadata, and the tab contents, 
    including the chords and lyrics.
    Inherits from UGTab.

    Class Variables:
    - tonalities          | The available chord names

    Instance Variables:
    - content_with_chords | The content still with '[ch]' and '[/ch]' surrounding the chords
    - transposition       | The integer by which the song's chords will be transposed
    """
    tonalities = ["A","Bb","B","C","Db","D","Eb","E","F","Gb","G","Ab"]

    # keys = {
    #     'Ab': ['Ab','Bb','C','Db','Eb','F','G'],
    #     'A': ['A','B','C#','D','E','F#','G#'],
    #     'Bb': ['Bb','C','D','Eb','F','G','A'],
    #     'B': ['B','C#','D#','E','F#','G#','A#'],
    #     'C': ['C','D','E','F','G','A','B'],
    #     'Db': ['Db','Eb','F','Gb','Ab','Bb','C'],
    #     'D': ['D','E','F#','G','A','B','C#'],
    #     'Eb': ['Eb','F','G','Ab','Bb','C','D'],
    #     'E': ['E','F#','G#','A','B','C#','D#'],
    #     'F': ['F','G','A','Bb','C','D','E'],
    #     'F#': ['F#','G#','A#','B','C#','D#','E#'],
    #     'G': ['G','A','B','C','D','E','F#'],
    # }

    def __init__(self, data: dict):
        self._info: UGTabInfo = UGTabInfo(data)
        self._content_with_chords: str = self._format_content(data['store']['page']['data']['tab_view']['wiki_tab']['content'], fchords=False)
        self._content: str = self._format_content(self._content_with_chords)
        self._chords_og: list[str] = list(data['store']['page']['data']['tab_view']['applicature'].keys())
        self._transposition: int = 0
    
    def transpose(self, transposition: int = 0) -> None:
        self._transposition = transposition%12
        if self._transposition == 0:
            self._content_with_chords: str = self._format_content(self._content_with_chords, fchords=True)
            return
        #FIXME: How to deal with sharps / flats
        content = self._content_with_chords
        for c in self._chords_og:
            new_chord = c
            slash_i = new_chord.find('/')
            if slash_i != -1:
                try:
                    new_chord = UGChords.tonalities[(UGChords.tonalities.index(c[:slash_i][:2])+self._transposition)%12] \
                        + c[2:slash_i] \
                        + UGChords.tonalities[(UGChords.tonalities.index(c[slash_i+1:])+self._transposition)%12]
                except ValueError:
                    try:
                        new_chord = UGChords.tonalities[(UGChords.tonalities.index(c[:slash_i][0])+self._transposition)%12] \
                            + c[1:slash_i] \
                            + UGChords.tonalities[(UGChords.tonalities.index(c[slash_i+1:])+self._transposition)%12]
                    except ValueError:
                        pass
            else:
                try:
                    new_chord = UGChords.tonalities[(UGChords.tonalities.index(c[:2])+self._transposition)%12] \
                        + c[2:]
                except ValueError:
                    try:
                        new_chord = UGChords.tonalities[(UGChords.tonalities.index(c[0])+self._transposition)%12] \
                            + c[1:]
                    except ValueError:
                        pass
            content = content.replace(
                f"[ch]{c}[/ch]",
                new_chord
            )
            
        self._content = content


    def get_transposition(self) -> int:
        return self._transposition
    
    def get_formatted_metadata(self) -> str:
        return super().get_formatted_metadata() + "\nTransposition: " + str(self.get_transposition())



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
        self._tab_id: int = data['id']
        self._tab_url: str = data['tab_url']
        self._artist: str = data['artist_name']
        self._song: str = data['song_name']
        self._type: str = data['type']
        self._votes: int = data['votes']
        self._rating: float = data['rating']
    
    def get_tab_id(self) -> str:
        return self._tab_id

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
                + f"**ID:** `{self._tab_id}`\n" \
                + f"**Link**\n{self._tab_url}"
    

class UGArtist():
    def __init__(self, data: dict):
        self._artist: str = data['artist_name']
        self._artist_url: str = data['artist_url']
    
    def get_artist(self) -> str:
        return self._artist
    
    def get_artist_url(self) -> str:
        return self._artist_url
    
    def get_formatted_result_description(self) -> str:
        return f"**Link**\n{'https://www.ultimate-guitar.com' + self._artist_url}"


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
        try:
            self._raw_results: list[dict] = data["store"]["page"]["data"]["results"]
        except KeyError:
            self._raw_results: list[dict] = data["store"]["page"]["data"]["other_tabs"]

    def get_results(self, num: int) -> "list[UGSearchResult]":
        """
        Returns a list of search results.
        Currently sorts the results by highest number of votes.
        """
        assert num > 0
        s_r = []
        for r in self._raw_results:
            try:
                if r['type'] == "Chords" or r['type'] == "Tabs":
                    s_r.append(UGSearchResult(r))
            except KeyError:
                pass
        s_r.sort(reverse=True, key=UGSearch.sort_key)
        return s_r[:num]

    def get_chords_results(self, num: int) -> "list[UGSearchResult]": 
        """
        Returns a list of search results that are for Chords type results.
        Currently sorts the results by highest number of votes.
        """
        assert num > 0
        ch_r = []
        for r in self._raw_results:
            try:
                if r['type'] == "Chords":
                    ch_r.append(UGSearchResult(r))
            except KeyError:
                pass
        ch_r.sort(reverse=True, key=UGSearch.sort_key)
        return ch_r[:num]
    
    def get_tabs_results(self, num: int) -> "list[UGSearchResult]":
        """
        Returns a list of search results that are for Tabs type results.
        Currently sorts the results by highest number of votes.
        """
        assert num > 0
        t_r = []
        for r in self._raw_results:
            try:
                if r['type'] == "Tabs":
                    t_r.append(UGSearchResult(r))
            except KeyError:
                pass
        t_r.sort(reverse=True, key=UGSearch.sort_key)
        return t_r[:num]
    
    def get_artists_results(self, num: int) -> "list[UGArtist]":
        """
        Returns a list of artist results.
        """
        assert num > 0
        a_r = []
        for r in self._raw_results:
            a_r.append(UGArtist(r))
        return a_r[:num]
    
class UGExplore(UGSearch): #TODO: still sorts by votes, turn sorting off
    def __init__(self, data: dict):
        self._raw_results: list[dict] = data["store"]["page"]["data"]["data"]["tabs"]