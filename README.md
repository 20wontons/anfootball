# Ultimate Guitar Discord Bot

This bot is able to display the chords and lyrics for a song that the user inputs.

**References:**

* https://github.com/joncardasis/ultimate-api
    * found to be incompatible with ultimate guitar (checked on 2022/09/09)
* https://realpython.com/beautiful-soup-web-scraper-python/


## Sprints

**Part 1:**

* [X] Will be able to successfully send a query to the API
    * Successfully able to access the html of a page (2022/09/09)
* [X] Will be able to successfully receive data from the API
    * Successfully able to return JSON extracted from the html (2022/09/09)
* [ ] Will output the return data in chords and lyrics format (with hard-coded query)

**Part 2:**

* [ ] Create a Discord bot that can produce output
* [ ] The bot can receive input and produce output
* [ ] The bot can display chord/lyric format
* [ ] The bot can successfully apply Part 1


**Part 3:**

* [ ] Make a web scraper for the search results on ultimate guitar that only returns chord type results
* [ ] Inputting an artist and song will return the first 5 (at most) chord results
* [ ] The Discord bot will be able to receive artist - song input and return a list of the results
* [ ] When the user chooses one of those results, the bot will correctly display the chord/lyric format for that specific chord tab