import interactions
from interactions.ext.wait_for import wait_for_component, setup
# ctx: interactions.context._Context

import asyncio

from server import keep_alive

from ug_scraper import json_from_search, json_from_url, json_from_explore, InvalidLinkError, requests
from ug_parser import UGTab, UGSearch, UGSearchResult, UGChords, UGExplore, UGArtist

UG_YELLOW = 0xffc600

import os
from dotenv import load_dotenv

load_dotenv()

# token is in a file called .env
# TOKEN = '<BOT_TOKEN>'
_token = os.getenv('TOKEN')
_ready: bool = False

bot = interactions.Client(token=_token)
setup(bot)


@bot.event
async def on_ready():
    global _ready
    if not _ready:
        # sets listening status to "Listening to Never Meant"
        await bot.change_presence(
            presence=interactions.ClientPresence(
                activities=[interactions.PresenceActivity(
                    name="Never Meant",
                    type=interactions.PresenceActivityType.LISTENING,
                    # created_at=1662794760,
                    # details="americ anfootball",
                )]
            )
        )
        _ready = True
    



@bot.command(
    name = "ping",
    description = "Pings the bot and returns the latency.",
)
async def ping(ctx):
    await ctx.send(f"Pong! `{round(bot.latency)}ms`")



@bot.command(
    name = "nevermeant",
    description = "americ anfootball",
)
async def nevermeant(ctx):
    try:
        url = "https://tabs.ultimate-guitar.com/tab/american-football/never-meant-tabs-979718"
        ugtabs = UGTab(json_from_url(url))
        NM_GREEN = 0x606E36

        tab_embed = _format_tab_embed(ugtabs)

        embed = interactions.Embed(
            title = "Never Meant",
            url = url,
            description = \
"""```
E|------------0----0-----0----0-------0-----|
C|---4p2p0---0-0--0-----0-0--0-------0-0----|
G|--------0-2----4---5/7----9---10/12-------|
C|-0----------------------------------------|
A|------------------------------------------|
F|------------------------------------------|
```""",
            color = NM_GREEN,
        )
        embed.set_author(name="American Football", icon_url="https://f4.bcbits.com/img/a2991634193_10.jpg")
        embed.set_footer(text=url)
        
        await ctx.send("Let's just forget...", embeds=embed, components=nm_display_full_button)

        try:
            # Waiting for the button click
            button_ctx: interactions.ComponentContext = await bot.wait_for_component(
                components=[nm_display_full_button], 
                timeout=60
            )
            await button_ctx.edit(content=None, embeds=tab_embed, components=[])
        except asyncio.TimeoutError:
            return await ctx.edit(components=[])

    except InvalidLinkError as e:
        # Ephemeral message for invalid Links
        await ctx.send(e, ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        if e.response.status_code == 404:
            await ctx.send(f"Tab not found.", ephemeral=True)
        else:
            await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)


nm_display_full_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, 
    label="Display Full Tab",
    custom_id="nm display"
)



@bot.command(
    name = "chords",
    description = "Finds the highest voted Chords tab for a song.",
    options = [
        interactions.Option(
            name = "artist",
            description = "The artist name",
            type = interactions.OptionType.STRING,
            required = True
        ),
        interactions.Option(
            name = "song",
            description = "The song title",
            type = interactions.OptionType.STRING,
            required = True
        ),
        interactions.Option(
            name = "transpose",
            description = "The number of semitones to change the tonality of the song",
            type = interactions.OptionType.INTEGER,
            required = False,
        ),
        # interactions.Option(
        #     name = "url",
        #     description = "The URL for the Ultimate Guitar Tab",
        #     type = interactions.OptionType.STRING,
        #     required = True,
        # ),
    ],
)
async def chords(ctx, artist: str, song: str, transpose: int = 0): #url: str
    try:
        # Takes the first result in the sorted results listing.
        url = UGSearch(json_from_search(artist, song)).get_chords_results(1)[0].get_tab_url()
        ugchords = UGChords(json_from_url(url))
        ugchords.transpose(transpose)
        
        embed = _format_tab_embed(ugchords)
        
        await ctx.send(embeds=embed)
    except InvalidLinkError as e:
        # Ephemeral message for invalid Links
        await ctx.send(e, ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        if e.response.status_code == 404:
            await ctx.send(f"Tab not found.", ephemeral=True)
        else:
            await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)



@bot.command(
    name = "tabs",
    description = "Finds the highest voted Tabs tab for a song.",
    options = [
        interactions.Option(
            name = "artist",
            description = "The artist name",
            type = interactions.OptionType.STRING,
            required = True
        ),
        interactions.Option(
            name = "song",
            description = "The song title",
            type = interactions.OptionType.STRING,
            required = True
        ),
    ],
)
async def tabs(ctx, artist: str, song: str):
    try:
        # Takes the first result in the sorted results listing.
        url = UGSearch(json_from_search(artist, song)).get_tabs_results(1)[0].get_tab_url()
        ugtabs = UGTab(json_from_url(url))

        embed = _format_tab_embed(ugtabs)
        
        await ctx.send(embeds=embed)
    except InvalidLinkError as e:
        # Ephemeral message for invalid Links
        await ctx.send(e, ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        if e.response.status_code == 404:
            await ctx.send(f"Tab not found.", ephemeral=True)
        else:
            await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)



@bot.command(
    name = "search",
    description = "Search for a song.",
    options = [
        interactions.Option(
            name = "all",
            description = "Search for a song.",
            type = interactions.OptionType.SUB_COMMAND,
            options = [
                interactions.Option(
                    name = "artist",
                    description = "The artist name",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
                interactions.Option(
                    name = "song",
                    description = "The song title",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
            ]
        ),
        interactions.Option(
            name = "chords",
            description = "Search for song chords.",
            type = interactions.OptionType.SUB_COMMAND,
            options = [
                interactions.Option(
                    name = "artist",
                    description = "The artist name",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
                interactions.Option(
                    name = "song",
                    description = "The song title",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
            ]
        ),
        interactions.Option(
            name = "tabs",
            description = "Search for song tabs.",
            type = interactions.OptionType.SUB_COMMAND,
            options = [
                interactions.Option(
                    name = "artist",
                    description = "The artist name",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
                interactions.Option(
                    name = "song",
                    description = "The song title",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
            ]
        ),
        interactions.Option(
            name = "artist",
            description = "Search for a band/artist's chords and tabs.",
            type = interactions.OptionType.SUB_COMMAND,
            options = [
                interactions.Option(
                    name = "artist",
                    description = "The artist name",
                    type = interactions.OptionType.STRING,
                    required = True
                ),
            ]
        )
    ],
)
async def search(ctx: interactions.context._Context, sub_command: str, artist: str, song: str = None):
    try:
        if sub_command == "artist":
            ugsearch = UGSearch(json_from_search(artist))
            results = ugsearch.get_artists_results(10)
            results_embeds = _format_results_embeds(results)
            
            page = 0
            PAGE_MAX = len(results_embeds)-1
            search_row.components[0].disabled = True
            search_row.components[2].disabled = page == PAGE_MAX

            await ctx.send(embeds=results_embeds[page], components=search_row)
            
            try:
                while True:
                    # Waiting for the button click
                    button_ctx: interactions.ComponentContext = await bot.wait_for_component(
                        components=[search_left_button, search_choose_button, search_right_button], 
                        timeout=60
                    )
                    if button_ctx.custom_id == "next":
                        page += 1
                    elif button_ctx.custom_id == "prev":
                        page -= 1
                    elif button_ctx.custom_id == "choose":
                        break

                    search_row.components[0].disabled=page == 0
                    search_row.components[2].disabled=page == PAGE_MAX

                    await button_ctx.edit(embeds=results_embeds[page], components=search_row)
            except asyncio.TimeoutError:
                return await ctx.edit(embeds=results_embeds[page], components=[])
            
            url = "https://www.ultimate-guitar.com" + results[page].get_artist_url()
            ugsearch = UGSearch(json_from_url(url))
            sub_command = "all"
            await ctx.edit(embeds=results_embeds[page], components=[])
        else:
            ugsearch = UGSearch(json_from_search(artist, song))

        if sub_command == "all":
            results = ugsearch.get_results(10)
        elif sub_command == "chords":
            results = ugsearch.get_chords_results(10)
        elif sub_command == "tabs":
            results = ugsearch.get_tabs_results(10)
        
        results_embeds = _format_results_embeds(results)
        
        page = 0
        PAGE_MAX = len(results_embeds)-1
        search_row.components[0].disabled = True
        search_row.components[2].disabled = page == PAGE_MAX

        await ctx.send(embeds=results_embeds[page], components=search_row)
        
        try:
            while True:
                # Waiting for the button click
                button_ctx: interactions.ComponentContext = await bot.wait_for_component(
                    components=[search_left_button, search_choose_button, search_right_button], 
                    timeout=60
                )
                if button_ctx.custom_id == "next":
                    page += 1
                elif button_ctx.custom_id == "prev":
                    page -= 1
                elif button_ctx.custom_id == "choose":
                    break

                search_row.components[0].disabled=page == 0
                search_row.components[2].disabled=page == PAGE_MAX

                await button_ctx.edit(embeds=results_embeds[page], components=search_row)
        except asyncio.TimeoutError:
            return await ctx.edit(embeds=results_embeds[page], components=[])
        
        
        url = results[page].get_tab_url()
        ugtab = UGTab(json_from_url(url))

        embed = _format_tab_embed(ugtab)

        tab_row.components[0].url = url
        
        await button_ctx.edit(embeds=embed, components=tab_row)

        button_ctx = await bot.wait_for_component(
            components=[close_button],
            timeout=None
        )
        await button_ctx.edit(embeds=results_embeds[page], components=[])
        
    except InvalidLinkError as e:
        # Ephemeral message for invalid Links
        await ctx.send(e, ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        if e.response.status_code == 404:
            await ctx.send(f"Tab not found.", ephemeral=True)
        else:
            await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)


@bot.command(
    name = "explore",
    description = "Explore tabs on Ultimate-Guitar.",
    options = [
        interactions.Option(
            name = "today",
            description = "Today's most popular tabs.",
            type = interactions.OptionType.SUB_COMMAND
        ),
        interactions.Option(
            name = "popular",
            description = "Alltime popular tabs.",
            type = interactions.OptionType.SUB_COMMAND
        ),
        interactions.Option(
            name = "recent",
            description = "Recently added tabs.",
            type = interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name = "rating",
            description = "Highest rated tabs.",
            type = interactions.OptionType.SUB_COMMAND,
        )
    ],
)
async def explore(ctx: interactions.context._Context, sub_command: str):
    try:
        if sub_command == "today":
            option = "hitsdailygroup_desc"
        elif sub_command == "popular":
            option = "hitstotal_desc"
        elif sub_command == "recent":
            option = "date_desc"
        elif sub_command == "rating":
            option = "rating_desc"
        
        # Gets the highest voted 5 chord results and 5 tab results
        ugexplore = UGExplore(json_from_explore(option))
        results = ugexplore.get_results(10)
        
        results_embeds = _format_results_embeds(results)
        
        page = 0
        PAGE_MAX = len(results_embeds)-1
        search_row.components[0].disabled = True
        search_row.components[2].disabled = page == PAGE_MAX

        await ctx.send(embeds=results_embeds[page], components=search_row)
        
        # TODO: close brings back to the pagination
        try:
            while True:
                # Waiting for the button click
                button_ctx: interactions.ComponentContext = await bot.wait_for_component(
                    components=[search_left_button, search_choose_button, search_right_button], 
                    timeout=60
                )
                if button_ctx.custom_id == "next":
                    page += 1
                elif button_ctx.custom_id == "prev":
                    page -= 1
                elif button_ctx.custom_id == "choose":
                    break

                search_row.components[0].disabled=page == 0
                search_row.components[2].disabled=page == PAGE_MAX

                await button_ctx.edit(embeds=results_embeds[page], components=search_row)
        except asyncio.TimeoutError:
            return await ctx.edit(embeds=results_embeds[page], components=[])
        
        
        url = results[page].get_tab_url()
        ugtab = UGTab(json_from_url(url))

        embed = _format_tab_embed(ugtab)

        tab_row.components[0].url = url
        
        await button_ctx.edit(embeds=embed, components=tab_row)

        button_ctx = await bot.wait_for_component(
            components=[close_button],
            timeout=None
        )
        await button_ctx.edit(embeds=results_embeds[page], components=[])

            

    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        if e.response.status_code == 404:
            await ctx.send(f"Tab not found.", ephemeral=True)
        else:
            await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)




def _format_tab_embed(ugtab: UGTab) -> interactions.Embed:
    """Formats the tab to be an embed."""
    # FIXME: Handle chords/tabs that are too long (max: 4096)!!
    # temporary fix
    c = ugtab.get_content()
    if len(c) > 4096:
        c = c[:4000] + "\n\n... [TRUNCATED] ..." 

    embed = interactions.Embed(
        title = ugtab.get_artist() + " - " + ugtab.get_song() + " (" + ugtab.get_type() + ")",
        url = ugtab.get_tab_url(),
        description = "```" + c + "```",
        color = UG_YELLOW
    )
    embed.set_footer(text=ugtab.get_formatted_metadata())
    return embed



def _format_results_embeds(results: "list[UGSearchResult | UGArtist]") -> "list[interactions.Embed]":
    """Formats the results listing to be embeds."""
    results_embeds = []
    for i in range(len(results)):
        r = results[i]
        if type(r) is UGSearchResult:
            embed = interactions.Embed(
                title = r.get_artist() + " - " + r.get_song() + " (" + r.get_type() + ")",
                description = r.get_formatted_result_description(),
                color = UG_YELLOW
            )
        elif type(r) is UGArtist:
            embed = interactions.Embed(
                title = r.get_artist(),
                description = r.get_formatted_result_description(),
                color = UG_YELLOW
            )
        embed.set_footer(text=str(i+1)+"/"+str(len(results)))
        results_embeds.append(embed)
    return results_embeds



search_right_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, 
    label="Next",
    custom_id="next"
)
search_left_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, 
    label="Prev",
    custom_id="prev"
)
search_choose_button = interactions.Button(
    style=interactions.ButtonStyle.SUCCESS, 
    label="Display",
    custom_id="choose"
)
search_row = interactions.ActionRow(
    components=[
        search_left_button, 
        search_choose_button, 
        search_right_button
    ]
)

link_button = interactions.Button(
    style=interactions.ButtonStyle.LINK, 
    label="Open in UG"
)
close_button = interactions.Button(
    style=interactions.ButtonStyle.DANGER, 
    label="Close",
    custom_id="close"
)
tab_row = interactions.ActionRow(
    components=[
        link_button, 
        close_button
    ]
)


keep_alive()

bot.start()