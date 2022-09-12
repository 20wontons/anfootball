import interactions

from scraper import json_from_url, InvalidLinkError, requests
from parser import UGTab

UG_YELLOW = 0xffc600

import os
from dotenv import load_dotenv

load_dotenv()

# token is in a file called .env
# TOKEN = '<BOT_TOKEN>'
_token = os.getenv('TOKEN')

bot = interactions.Client(token=_token)


@bot.command(
    name = "ping",
    description = "Pings the bot.",
)
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(
    name = "chords",
    description = "Find the chords and lyrics for a song.",
    options = [
        interactions.Option(
            name = "url",
            description = "The URL for the Ultimate Guitar Tab",
            type = interactions.OptionType.STRING,
            required = True,
        ),
        # interactions.Option(
        #     name = "transpose",
        #     description = "Change the key (and chords) of the song.",
        #     type = interactions.OptionType.INTEGER,
        #     required = False,
        # ),
    ],
)
async def chords(ctx, url: str):#, transpose: int = 0):
    try:
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
    except requests.HTTPError:
        # Ephemeral message for unsuccessful HTTP connections
        await ctx.send("Unsuccessful connection. Try again later.", ephemeral=True)
    # except Exception as e:
    #     # Ephemeral message for all other errors
    #     print(e)
    #     await ctx.send("Something went wrong.", ephemeral=True)


bot.start()