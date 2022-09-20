import unittest


import scraper

class TestScraper(unittest.TestCase):
    """
    Tests for the basic functionality of scraper.py
    i.e. web scraping ultimate-guitar.com
    """
    def setUp(self):
        self.url = "https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421111"
        self.broken_url = "https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421"
        self.url2 = "https://tabs.ultimate-guitar.com/tab/echosmith/bright-chords-1442936"
        
        # Writes JSON to files, uncomment for debug
        # scraper.write_dict_to_file(scraper.json_from_url(self.url), 'sample/sample_json/chit_chat.json')
        # scraper.write_dict_to_file(scraper.json_from_url(self.url2), 'sample/sample_json/bright.json')
        # scraper.write_dict_to_file(scraper.json_from_search("beach weather", "chit chat"), 'sample/sample_json/chit_chat_search.json')
        # scraper.write_dict_to_file(scraper.json_from_search("oasis", "wonderwall"), 'sample/sample_json/wonderwall_search.json')

    def test_invalid_link_raises_InvalidLinkError(self):
        self.assertRaises(scraper.InvalidLinkError, scraper.json_from_url, 'https://www.google.com/')
        self.assertRaises(scraper.InvalidLinkError, scraper.json_from_url, 'https://www.youtube.com/watch?v=rogKZtOhg44&list=LL&index=8&ab_channel=Astro%27s2ndchannel')

    def test_incorrect_link_raises_HTTPError(self):
        self.assertRaises(scraper.requests.HTTPError, scraper.json_from_url, self.broken_url)
    
    def test_link_returns_jsondict(self):
        self.assertTrue(type(scraper.json_from_url(self.url)) == dict)



import parser

class TestParser(unittest.TestCase):
    """
    Tests for the basic functionality of parser.py
    i.e. parsing the JSON from ultimate-guitar.com
    """
    def setUp(self):
        f = open('sample/sample_json/chit_chat.json', 'r')
        data = scraper.json.loads(f.read())
        self.tab = parser.UGTab(data)
        
        f2 = open('sample/sample_json/bright.json', 'r')
        data2 = scraper.json.loads(f2.read())
        self.tab2 = parser.UGTab(data2)

        f.close()
        f2.close()
        

    def test_tab_info_values_are_correct_values(self):
        # Beach Weather - Chit Chat
        self.assertEqual(2421111, self.tab.get_tab_id())
        self.assertEqual("https://tabs.ultimate-guitar.com/tab/beach-weather/chit-chat-chords-2421111", self.tab.get_tab_url())
        self.assertEqual("Beach Weather", self.tab.get_artist())
        self.assertEqual("Chit Chat", self.tab.get_song())
        self.assertEqual("E A D G B E", self.tab.get_tuning())
        self.assertEqual("A", self.tab.get_key())
        self.assertIsNone(self.tab.get_capo())

        # Echosmith - Bright
        self.assertEqual(1442936, self.tab2.get_tab_id())
        self.assertEqual("https://tabs.ultimate-guitar.com/tab/echosmith/bright-chords-1442936", self.tab2.get_tab_url())
        self.assertEqual("Echosmith", self.tab2.get_artist())
        self.assertEqual("Bright", self.tab2.get_song())
        self.assertIsNone(self.tab2.get_tuning())
        self.assertIsNone(self.tab2.get_key())
        self.assertEqual(2, self.tab2.get_capo())
    
    def test_content_is_formatted(self):
        tab_content = self.tab.get_content()
        self.assertEqual(-1, tab_content.find("[ch]"))
        self.assertEqual(-1, tab_content.find("[/ch]"))
        self.assertEqual(-1, tab_content.find("[tab]"))
        self.assertEqual(-1, tab_content.find("[/tab]"))

        tab2_content = self.tab2.get_content()
        self.assertEqual(-1, tab2_content.find("[ch]"))
        self.assertEqual(-1, tab2_content.find("[/ch]"))
        self.assertEqual(-1, tab2_content.find("[tab]"))
        self.assertEqual(-1, tab2_content.find("[/tab]"))
    
    def test_content_is_correct(self):
        f = open('sample/chit_chat.txt', 'r')
        sample_content = f.read()
        f.close()
        self.assertEqual(sample_content, self.tab.get_content())


if __name__ == '__main__':
    unittest.main()