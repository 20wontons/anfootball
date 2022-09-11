import interactions

import os
from dotenv import load_dotenv

load_dotenv()

# token is in a file called .env
# TOKEN = '<BOT_TOKEN>'
_token = os.getenv('TOKEN')

bot = interactions.Client(token=_token)


@bot.command()
async def ping(ctx):
    """Pings the bot."""
    await ctx.send("Pong!")



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