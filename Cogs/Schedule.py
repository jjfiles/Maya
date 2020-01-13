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

from secrets import spreadid

# GSheets scopes and sheet ID
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SCHEDULE_SPREAD_ID = spreadid

# DO NOT CHANGE THESE
SHEET_END = "!"
RANGE_MID = ":"

# Cog to query schdules in a gsheet


class Schedule(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # create / load token file with G auth
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

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Build service with given creds
        service = build('sheets', 'v4', credentials=creds)

        # initialize spreadsheet
        self.sheet = service.spreadsheets()

        # define columns for get requests
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

        # define rows for get requests
        self.rows = {
            0: "2",
            1: "3",
            2: "4",
            3: "5",
            4: "6",
            5: "7",
            6: "8",
            7: "9",
            8: "10",
            9: "11",
            10: "12",
            11: "13",
            12: "14",
            13: "15",
            14: "16",
            15: "17",
            16: "18",
            17: "19",
            18: "20",
            19: "21",
            20: "22",
            21: "23",
            22: "24",
            23: "25",
        }

        Adam = "Adam"
        Jeff = "Jeff"
        Sam = "Sam"

        # TODO: MAKE DYNAMIC
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

        self.doing = ["Work", "School", "Free", "Outside", "Busy", "Sleep"]

        """
        request is as follows
        request = self.sheet.values().get(spreadsheetId=SCHEDULE_SPREAD_ID, range = 'sheetname!range_to_search:rangetosearch').execute()

        filter is as follows
        filter = request.get('values', [])
        """

    def __str__(self):
        return self.sheet

    @commands.command(pass_context=True, no_pm=False)
    async def whereis(self, ctx, arg):
        if arg in self.names:
            sheetid = self.names.get(arg)
            day = self.days.get(datetime.datetime.now().weekday())
            col = self.columns.get(day)
            row = self.rows.get(datetime.datetime.now().hour)

            query = sheetid + SHEET_END + col + row

            request = self.sheet.values().get(
                spreadsheetId=SCHEDULE_SPREAD_ID, range=query).execute()
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

    @commands.command(pass_context=True, no_pm=False)
    async def free(self, ctx, arg):
        hours = []
        breaks = []

        if arg in self.names:
            sheetid = self.names.get(arg)

            # current day and current hour
            curCol = self.columns.get(self.days.get(
                datetime.datetime.now().weekday()))
            curRow = self.rows.get(datetime.datetime.now().hour)
            for e in self.rows:
                if e < int(curRow):
                    pass
                else:
                    query = sheetid + SHEET_END + curCol + str(e)
                    request = self.sheet.values().get(
                        spreadsheetId=SCHEDULE_SPREAD_ID, range=query).execute()
                    response = request.get('values', [])

                    try:
                        sresponse = response[0]
                        sresponse = str(sresponse).strip("[]'")
                        if sresponse == "Free" or sresponse == None:
                            hours.append(e)
                    except IndexError:
                        hours.append(self.rows.get(e))

            for each in hours:
                print(each)

            for e in hours:
                try:
                    if int(hours[e]) == int(hours[int(e)+1]) - 1:
                        pass
                    else:
                        breaks.append(e)
                except IndexError:
                    breaks.append(e)
            for each in breaks:
                print(each)

            index = breaks[0]
            for e in breaks:
                try:
                    if breaks[int(e)] == hours[0]:
                        query1 = sheetid + SHEET_END + "A" + hours[0]
                        r1 = self.sheet.values().get(
                            spreadsheetId=SCHEDULE_SPREAD_ID, range=query1).execute()
                        re1 = r1.get('values', [])
                        # r2 =
                        # try:
                except IndexError:
                    pass
