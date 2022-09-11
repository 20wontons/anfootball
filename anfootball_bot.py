import interactions

import interface

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
        ch = "```" + interface.get_chords(url)[:1000] + "```"
        await ctx.send(ch)
    except interface.scraper.InvalidLinkError:
        # Ephemeral message for invalid Links
        await ctx.send("This is not a valid `tabs.ultimate-guitar.com/tabs/` link.", ephemeral=True)
    except interface.scraper.requests.HTTPError:
        # Ephemeral message for unsuccessful HTTP connections
        await ctx.send("Unsuccessful connection. Try again later.", ephemeral=True)
    except Exception as e:
        # Ephemeral message for all other errors
        print(e.with_traceback())
        await ctx.send("Something went wrong.", ephemeral=True)


bot.start()




### Not for slash commands ###

# import discord
# from discord.ext import commands

# bot = commands.Bot(command_prefix='&')

# @bot.event
# async def on_ready():
#     print("Logged in as a bot {0.user}".format(bot))

# @bot.command()
# async def ping(ctx):
#     await ctx.send('Pong!')

# bot.run(token)