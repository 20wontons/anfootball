# Anfootball: Ultimate-Guitar Discord Bot

![Python-Version](https://img.shields.io/badge/Python-3.10.7-blue.svg)

Anfootball is a Discord bot that retrieves chords, tabs, and lyrics for a specified song from [Ultimate-Guitar](https://www.ultimate-guitar.com/).

🎸🎸🎸


## Commands
**Parameters:** `<>` - required, `[]` - optional, `\` - either/or
Do not include `<>` , `[]` or `\` when executing the command.
| Usage | Description |
| ------- | ----- |
| `/chords <artist> <song> [transpose]` | Finds the highest voted Chords tab for a song.<br>Transpose to change the key of the song `(beta)`. |
| `/tabs <artist> <song>` | Finds the highest voted Tabs tab for a song. |
| `/search <all\chords\tabs> <artist> <song>` | Search for a song. |
| `/explore <today\popular\recent\rating>` | Explore tabs on Ultimate-Guitar. |
| `/nevermeant` | The americ anfootball lick. |
| `/ping` | Pings the bot and returns the latency. |


## Images

<img src="https://pbs.twimg.com/media/FdeYINYUYAAz4Dv?format=png&name=small" height=300 alt="/chords artist:Hot Mulligan song:Pop Shuvit Hall of Meat Duh"/>
<img src="https://pbs.twimg.com/media/FdeYOJ7UUAA9hhZ?format=png&name=small" height=300 alt="/tabs artist:Chinese Football song: Electronic Girl"/>
<img src="https://pbs.twimg.com/media/FdeYd46UUAAVG7J?format=png&name=small" height=300 alt="/search all artist:Jimmy Eat World song:The Middle"/>


## References

* https://github.com/joncardasis/ultimate-api
    * found to be incompatible with ultimate guitar (checked on 2022/09/09)
* https://realpython.com/beautiful-soup-web-scraper-python/
* https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html
* https://github.com/interactions-py


## Setup
1. Install python3 from https://www.python.org/downloads/

1. Create a virtual environment of python3 in the anfootball folder:

    ```cmd
    pip install virtualenv
    virtualenv venv
    .\venv\Scripts\activate
    ```

1. Install dependencies:
    
    ```cmd
    pip install -r requirements.txt
    pip install -U discord-py-interactions
    pip install -U interactions-wait-for
    ```

    **Note:** `discord.py` is not used for slash commands so `pip install -U discord.py` is not needed. 

1. Run the bot:
    ```cmd
    python anfootball_bot.py
    ```

## Sprints

**Part 1: Web Scraper**

* [X] Will be able to successfully send a query to the API
    * Successfully able to access the html of a page (2022/09/09)
* [X] Will be able to successfully receive data from the API
    * Successfully able to return JSON extracted from the html (2022/09/09)
* [X] Will output the return data in chords and lyrics format (with hard-coded query)
    * Successfully able to return the tab content in chords and lyrics format, mirroring the original tab (2022/09/10)

**Part 2: Discord Bot**

* [X] Create a Discord bot that can produce output
    * Successfully pinged and received a "Pong!" (2022/09/10)
        * Added bot response latency in milliseconds to `/ping` (2023/06/20)
* [X] The bot can receive input and produce output
    * Successfully able to receive input and respond (2022/09/11)
* [X] The bot can display chord/lyric format
    * Successfully able to display chord/lyric format in a code block, limited to 2000 chars. (2022/09/11)
* [X] The bot can successfully apply Part 1
    * Successfully able to display tab in an embed. (2022/09/11)

**Part 3: Search Feature**

* [X] Make a web scraper for the search results on ultimate guitar that only returns chord type results
    * Successfully able to scrape for the results and return a JSON (2022/09/12)
* [X] Inputting an artist and song will return the first 5 (at most) chord results
    * Successfully able to input artist/song and filter for chords (2022/09/12) 
* [X] The Discord bot will be able to receive artist - song input and return a list of the results
    * Displays a 10 page (at most) list of at most 5 Chords and 5 Tabs. (2022/09/12)
    * ~~*Known issue: "This interaction failed." shows up whenever any buttons are pressed*~~
        * Fixed! (2022/09/13)
* [X] When the user chooses one of those results, the bot will correctly display the chord/lyric format for that specific chord tab
    * Successfully displays the chords format when the user chooses that result option (2022/09/12)


**Part 4: Additional Features**

* [X] Allow for transposition of songs
    * Chords can now be transposed by the `transpose:` option in `/chords`, but needs work on dealing with sharps and flats (2022/09/19)
    * [ ] Make transpose a pair of buttons on the tab embed rather than an input field
* [X] Support for Tabs. Differentiated from chords by the search results and lack of transposition ability
    * Added `/tabs` (2022/09/15)
* [X] Subcommands for search: search chords and search tabs
    * Main search function renamed to `/search all` and added `/search chords` and `/search tabs`
    * [X] Close brings back to search
* [ ] Able to display a specific Chords/Tabs tab by ID
    * ~~Not able to search by ID, checked (2023/06/20)~~
    * Use `https://tabs.ultimate-guitar.com/tab/print?id=` which redirects to the tab page
* [X] Add a function to browse top 10 popular today and all time (2023/06/20)
    * `/explore` function added: `/explore today`, `/explore popular`, `/explore recent`, and `/explore rating`
    * [X] Close brings back to browse
* [X] Search for an artist, able to return most popular songs
    * Issue with pagination: how to handle artists that have a lot of tabs