

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

    Class Variables:
    - FOR_DISCORD: bool   | if True, then the chords in the formatted contents will be bolded by Discord syntax.
                            if False, then the chords will be plaintext unformatted
    
    Instance Variables:
    - info:     UGTabInfo | the tab info and metadata, in a UGTabInfo object
    - content:  str       | the tab content, which includes the formatted chords and lyrics
    """

    # set to True to bold the chords for Discord
    FOR_DISCORD = False

    def __init__(self, data: dict):
        self._info = UGTabInfo(data)
        self._content = self._format_content(data['store']['page']['data']['tab_view']['wiki_tab']['content'])
        #print(self._content)
    
    def _format_content(self, content: str) -> None:
        content = content.replace('[ch]', '**' if UGTab.FOR_DISCORD else '', -1)
        content = content.replace('[/ch]', '**' if UGTab.FOR_DISCORD else '', -1)
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