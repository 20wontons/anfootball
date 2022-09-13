# Ultimate Guitar Discord Bot

This bot is able to display the chords and lyrics for a song that the user inputs.

![Python-Version](https://img.shields.io/badge/Python-3.10.7-blue.svg)

**References:**

* https://github.com/joncardasis/ultimate-api
    * found to be incompatible with ultimate guitar (checked on 2022/09/09)
* https://realpython.com/beautiful-soup-web-scraper-python/
* https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html
* https://github.com/interactions-py


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
    <img src='https://cdn.discordapp.com/attachments/821931361681276929/1018394753554972803/unknown.png'/>
* [X] The bot can receive input and produce output
    * Successfully able to receive input and respond (2022/09/11)
* [X] The bot can display chord/lyric format
    * Successfully able to display chord/lyric format in a code block, limited to 2000 chars. (2022/09/11)
    <img src='https://cdn.discordapp.com/attachments/821931361681276929/1018604956909043822/unknown.png'/>
* [X] The bot can successfully apply Part 1
    * Successfully able to display tab in an embed. (2022/09/11)
    <img src='https://cdn.discordapp.com/attachments/821931361681276929/1018748075738681374/unknown.png'/>

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

* [ ] Allow for transposition of songs
* [ ] Support for Tabs. Differentiated from chords by the search results and lack of transposition ability


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

## License

    Copyright 2022 Antoine Nguyen

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.