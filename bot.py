import requests
import discord
import time
import datetime
import asyncio
import os.path
import pickle

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from discord.ext.commands import Bot
from discord.ext import commands
from discord import opus

Client = discord.Client()
bot_prefix = "~"
client = commands.Bot(command_prefix = commands.when_mentioned_or(bot_prefix))
Token = "NjYzNjQ2MzE0MDgwMjM5NjI2.XhLjCQ.Xfbq5wtt_lxac4UiYkjXP5p9xtQ"


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCHEDULE_SHEET_ID = '1AKu3quOJxEezhgCItjn3CpcnmRiIMPLIaNoov7OmofE'


@client.event
async def on_ready():
    print ("Bot Online")
    print ("Name: {}".format(client.user.name))
    print ("ID: {}".format(client.user.id) + '\n')

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open ('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)

        self.sheet = service.spreadsheets()
        self.result = self.sheet.values().get(spreadsheetId=SCHEDULE_SHEET_ID, range = 'A2').execute()
        self.values = self.result.get('values', [])

    def __str__(self):
        return self.sheet

    @commands.command(pass_context = True, no_pm = False)
    async def getValues(self, ctx):
        await ctx.send(self.values)

client.add_cog(Schedule(client))
client.run(Token)