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

#Set prefix to alert bot
bot_prefix = "~"

#allows bot to be addressed either with above prefix or @mention
client = commands.Bot(command_prefix = commands.when_mentioned_or(bot_prefix))

#Discord bot token
Token = "NjYzNjQ2MzE0MDgwMjM5NjI2.XhLjCQ.Xfbq5wtt_lxac4UiYkjXP5p9xtQ"


#
@client.event
async def on_ready():
    print ("Bot Online")
    print ("Name: {}".format(client.user.name))
    print ("ID: {}".format(client.user.id) + '\n')


#GSheets scopes and sheet ID
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SCHEDULE_SPREAD_ID = '1AKu3quOJxEezhgCItjn3CpcnmRiIMPLIaNoov7OmofE'

#DO NOT CHANGE THESE
SHEET_END = "!"
RANGE_MID = ":"

#Cog to query schdules in a gsheet
class Schedule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        #create / load token file with G auth
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

        #Build service with given creds
        service = build('sheets', 'v4', credentials=creds)

        #initialize spreadsheet
        self.sheet = service.spreadsheets()

        #define columns for get requests
        self.columns = {
            "Index": "A",
            "Sunday": "B",
            "Monday": "C",
            "Tuesday": "D",
            "Wednesday": "E",
            "Thursday": "F",
            "Friday": "G",
            "Saturday": "H",
        }

        #define rows for get requests
        self.rows = {
            "WEEK": "1", 
            "00": "2", 
            "01": "3", 
            "02": "4", 
            "03": "5", 
            "04": "6", 
            "05": "7", 
            "06": "8", 
            "07": "9", 
            "08": "10", 
            "09": "11", 
            "10": "12", 
            "11": "13", 
            "12": "14", 
            "13": "15", 
            "14": "16", 
            "15": "17", 
            "16": "18", 
            "17": "19", 
            "18": "20", 
            "19": "21", 
            "20": "22", 
            "21": "23", 
            "22": "24", 
            "23": "25", 
        }


        Adam = "Adam"
        Jeff = "Jeff"
        Sam = "Sam"

        #TODO: MAKE DYNAMIC
        self.names = {
            "jeff": Jeff, 
            "Jeff": Jeff,
            "adam": Adam,
            "Adam": Adam,
            "sam": Sam,
            "Sam": Sam,
        }

        self.days = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }

        self.doing = ["Work", "School", "Free", "Outside", "Busy"]
        """
        request is as follows
        request = self.sheet.values().get(spreadsheetId=SCHEDULE_SPREAD_ID, range = 'sheetname!range_to_search:rangetosearch').execute()

        filter is as follows
        filter = request.get('values', [])
        """

        self.request = self.sheet.values().get(spreadsheetId=SCHEDULE_SPREAD_ID, range = 'Jeff!B1:H1').execute()
        self.filter = self.request.get('values', [])

    def __str__(self):
        return self.sheet

    @commands.command(pass_context = True, no_pm = False)
    async def getValues(self, ctx):
        await ctx.send(self.filter)

    @commands.command(pass_context = True, no_pm = False)
    async def whereis(self, ctx, arg):
        if arg in self.names:
            sheetid = self.names.get(arg)
            day = self.days.get(datetime.datetime.now().weekday())
            col = self.columns.get(day)
            row = self.rows.get(str(datetime.datetime.now().hour))

            query = sheetid + SHEET_END + col + row
            print(query)
            print("Query called by {}".format(ctx.author) + "\n")

            request = self.sheet.values().get(spreadsheetId=SCHEDULE_SPREAD_ID, range = query).execute()
            response = request.get('values', [])
            try:
                sresponse = response[0]
                sresponse = str(sresponse).strip("[]'")
                if sresponse in self.doing:
                    await ctx.send(sresponse)
                elif sresponse == None or sresponse == "":
                    await ctx.send("Unknown, but probably free.")
                else:
                    await ctx.send(sresponse)
            except IndexError:
                await ctx.send("Unknown, but probably free.")
        else:
            await ctx.send("That name is not in our Database.")

client.add_cog(Schedule(client))
client.run(Token)