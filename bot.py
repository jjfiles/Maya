import requests
import discord
import time
import datetime
import asyncio
import os.path
import pickle

from Cogs.Schedule import Schedule

from discord.ext.commands import Bot
from discord.ext import commands

Client = discord.Client()

#Set prefix to alert bot
bot_prefix = "~"

#allows bot to be addressed either with above prefix or @mention
client = commands.Bot(command_prefix = commands.when_mentioned_or(bot_prefix))

#Discord bot token
Token = "NjYzNjQ2MzE0MDgwMjM5NjI2.XhLjCQ.Xfbq5wtt_lxac4UiYkjXP5p9xtQ"

#Bot online message
@client.event
async def on_ready():
    print ("Bot Online")
    print ("Name: {}".format(client.user.name))
    print ("ID: {}".format(client.user.id) + '\n')

client.add_cog(Schedule(client))
client.run(Token)