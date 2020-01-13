# base imports
import requests
import discord
import time
import datetime
import asyncio
import os.path
import pickle

# internal imports
from secrets import token
from Cogs.Schedule import Schedule

# discord imports
from discord.ext.commands import Bot
from discord.ext import commands


Client = discord.Client()

# Set prefix to alert bot
bot_prefix = "~"

# allows bot to be addressed either with above prefix or @mention
client = commands.Bot(command_prefix=commands.when_mentioned_or(bot_prefix))

# Discord bot token
Token = token

# Bot online message
@client.event
async def on_ready():
    print("Bot Online")
    print(f"Name: {client.user.name}")
    print(f"ID: {client.user.id}" + '\n')


@client.event
async def on_command_completion(ctx):
    print(f"Command called: {ctx.command}")
    # fix these
    # print ("With msg: ")
    # print (f"{ctx.message}")
    print(f"From user: {ctx.author}")
    # fix this output too
    print(f"At: {datetime.datetime.now()}")

client.add_cog(Schedule(client))
client.run(Token)
