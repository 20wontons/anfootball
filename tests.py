import unittest
import scraper

class TestScraper(unittest.TestCase):
    """
    Tests for the basic functionality of scraper.py
    """
    def setUp(self):
        self.url = "https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421111"
        self.broken_url = "https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421"
        self.url2 = "https://tabs.ultimate-guitar.com/tab/echosmith/bright-chords-1442936"
        
        # Writes JSON to files, uncomment for debug
        # scraper.write_dict_to_file(scraper.json_from_url(self.url), 'sample/sample_json/chit_chat.json')
        # scraper.write_dict_to_file(scraper.json_from_url(self.url2), 'sample/sample_json/bright.json')


    def test_incorrect_link_raises_http_error(self):
        self.assertRaises(scraper.requests.HTTPError, 
            scraper.json_from_url, self.broken_url)
    
    def test_link_returns_jsondict(self):
        self.assertTrue(type(scraper.json_from_url(self.url)) == dict)





if __name__ == '__main__':
    unittest.main()