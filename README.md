# Maya
Multifuctional Discord Bot

## Table of Contents
- [Maya](#maya)
  - [Table of Contents](#table-of-contents)
  - [In Progress Cogs](#in-progress-cogs)
  - [TODO Cogs](#todo-cogs)
- [Setup](#setup)
  - [Set some up files and variables](#set-some-up-files-and-variables)
  - [Setup your environment](#setup-your-environment)
  - [Run the bot](#run-the-bot)
- [Cog Setups](#cog-setups)
  - [Schedule Cog](#schedule-cog)
- [Commands and Event Listeners](#commands-and-event-listeners)
  - [Base](#base)
  - [Schedule](#schedule)

## In Progress Cogs
1. [Base](bot.py)
2. [Schedule](Cogs/Schedule.py)

## TODO Cogs  
1. Patch Notes
2. Sound Board
3. Music Player
4. Decision Maker

# Setup
## Set some up files and variables
Create a file to hold your secret variables 
> must be named **secrets.py**

I prefer powershell
```powershell
ni secrets.py
```

In that put your discord bot token in a variable token
Acquired from [discord's dev portal](https://discordapp.com/developers/applications/)
> must be named **token**
```python
token = "YOUR BOT TOKEN GOES HERE"
```

## Setup your environment

```powershell
virtualenv venv

pip install -r requirements.txt

venv/Scripts/activate.ps1
```

## Run the bot

```powershell
python bot.py
```


---
# Cog Setups

## Schedule Cog
Find your spreadsheet id
> docs.google.com/spreadsheets/d/THIS_IS_YOUR_SPREADSHEET_ID/edit#gid=0

Put it in your secrets.py file
> must be named **spreadid**
```python
spreadid = "YOUR SPREAD ID GOES HERE"
```

Get your authorization credentials from google API
> Go [here](https://developers.google.com/sheets/api/quickstart/python) and click the "Enable the Google Sheets API" button. 
> Then the "Download Client Information" button and put that in your bot directory

Until it is made dynamic (coming soon), I am using this format for the spreadsheet

|     | A     | B      | ... | H        |
| --- | ----- | ------ | --- | -------- |
| 1   | 12 AM | Sunday | ... | Saturday |
| 2   | 1 AM  |        |     |          |
| 3   | 2 AM  |        |     |          |
| 4   | 3 AM  |        |     |          |
| 5   | 4 AM  |        |     |          |
| ... | ...   |        |     |          |
| 25  | 11 PM |        |     |          |

With the name of each sheet being the persons first name capitalized
> i.e. Jeff

# Commands and Event Listeners
## Base
* Help
  * The default help command from discord.py. This will be aided by help tags in each command to let users know what each command does
* on_ready listener
  * This outputs to the console with some identifying information about the bot when it comes online successfully.
* on_command_completion listener
  * This outputs to the console relevant context information when a command is succesfully run. More information and saving to a log file is planned

## Schedule
* whereis
  * This command with a name argument will search for a sheet in the schedule spreadsheet, at the current time, to see what that person is scheduled to be doing. Plans to add aliases are in the works.
* free
  * This command with a name argument will search for that person's schedule and see at what points that day they are free (from that current point onward). Plans to add more specific search arguments are on the TODO list.