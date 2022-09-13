import interactions
from interactions.ext.wait_for import wait_for_component, setup
# ctx: interactions.context._Context

import asyncio

from scraper import json_from_search, json_from_url, InvalidLinkError, requests
from parser import UGTab, UGSearch, UGSearchResult

UG_YELLOW = 0xffc600

import os
from dotenv import load_dotenv

load_dotenv()

# token is in a file called .env
# TOKEN = '<BOT_TOKEN>'
_token = os.getenv('TOKEN')

bot = interactions.Client(token=_token)
setup(bot)

@bot.command(
    name = "ping",
    description = "Pings the bot.",
)
async def ping(ctx):
    await ctx.send("Pong!")


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
        # interactions.Option(
        #     name = "url",
        #     description = "The URL for the Ultimate Guitar Tab",
        #     type = interactions.OptionType.STRING,
        #     required = True,
        # ),
        # interactions.Option(
        #     name = "transpose",
        #     description = "Change the key (and chords) of the song.",
        #     type = interactions.OptionType.INTEGER,
        #     required = False,
        # ),
    ],
)
async def chords(ctx, artist: str, song: str):#url: str, transpose: int = 0):
    try:
        # Takes the first result in the sorted results listing.
        url = UGSearch(json_from_search(artist, song)).get_chords_results()[0].get_tab_url()
        ugchords = UGTab(json_from_url(url))
        embed = interactions.Embed(
            title = ugchords.get_artist() + " - " + ugchords.get_song(),
            url = ugchords.get_tab_url(),
            description = "```" + ugchords.get_content() + "```",
            color = UG_YELLOW
        )
        embed.set_footer(text=ugchords.get_formatted_metadata())
        
        await ctx.send(embeds=embed)
    except InvalidLinkError:
        # Ephemeral message for invalid Links
        await ctx.send("This is not a valid `tabs.ultimate-guitar.com/tabs/` link.", ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        await ctx.send(e, ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)



@bot.command(
    name = "search",
    description = "Search for a song.",
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
async def search(ctx: interactions.context._Context, artist: str, song: str):
    try:
        # Gets the highest voted 5 chord results and 5 tab results
        ugsearch = UGSearch(json_from_search(artist, song))
        results = ugsearch.get_chords_results()[:5] + ugsearch.get_tab_results()[:5]
        results_embeds = _format_results_embeds(results)
        
        page = 0
        PAGE_MAX = len(results_embeds)-1
        search_row.components[0].disabled = True
        search_row.components[2].disabled = page == PAGE_MAX

        await ctx.send(embeds=results_embeds[page], components=search_row)
        
        try:
            while True:
                # FIXME: after pressing any button it says "This interaction failed." but still works
                button_ctx: interactions.ComponentContext = await bot.wait_for_component(
                    components=[search_left_button, search_choose_button, search_right_button], timeout=60
                )
                if button_ctx.custom_id == "next":
                    page += 1
                elif button_ctx.custom_id == "prev":
                    page -= 1
                elif button_ctx.custom_id == "choose":
                    break

                search_row.components[0].disabled=page == 0
                search_row.components[2].disabled=page == PAGE_MAX

                await ctx.edit(embeds=results_embeds[page], components=search_row)
        except asyncio.TimeoutError:
            return await ctx.edit(components=[])
        
        url = results[page].get_tab_url()
        ugchords = UGTab(json_from_url(url))
        embed = interactions.Embed(
            title = ugchords.get_artist() + " - " + ugchords.get_song(),
            url = ugchords.get_tab_url(),
            description = "```" + ugchords.get_content() + "```",
            color = UG_YELLOW
        )
        embed.set_footer(text=ugchords.get_formatted_metadata())
        
        await ctx.edit(embeds=embed, components=[])

        
    except InvalidLinkError:
        # Ephemeral message for invalid Links
        await ctx.send("This is not a valid `tabs.ultimate-guitar.com/tabs/` link.", ephemeral=True)
    except requests.HTTPError as e:
        # Ephemeral message for unsuccessful HTTP connections
        await ctx.send(f"Unsuccessful connection: {e}. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)

def _format_results_embeds(results: list[UGSearchResult]) -> list[interactions.Embed]:
    results_embeds = []
    for i in range(len(results)):
        r = results[i]
        embed = interactions.Embed(
            title = r.get_artist() + " - " + r.get_song() + " (" + r.get_type() + ")",
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
    style=interactions.ButtonStyle.PRIMARY, 
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


bot.start()