from discord.ext import  commands
from datetime import datetime
from colorama import init
import nest_asyncio
import threading
import requests
import discord
import asyncio
import time

# Kami147 [Midnight Development]
# Simple script to remind me when names I want are dropping, I keep forgotting... 

botToken = "" #Your bots token goes here
webHook = "" #Web hook to send alert to

'''
 ID's of users with access to this bot, yes I could make it channel based but I dont wanna get trollaged by Midnight's Administration
 Example:
 access = [
 	"234908238472894722",
 	"138476249583724987"
 ]
'''

access = [""]

bot = commands.Bot(command_prefix="+", help_command=None)

#
#Ok variables done lets get on with this script.
#

def add_Reminder(name):
	r = requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"})

	if r.status_code >= 400:
		requests.post(webHook, json={"embeds": [{"title": "Error", "description": f"This name isn't dropping", "color": 10038562}]})
	else:
		dropTime = float(r.json()["unix"])

		while dropTime > time.time():
			if(int(dropTime-60) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 1 minute", "color": 10038562}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1) #Prevent spam
			elif(int(dropTime-300) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 5 minutes", "color": 10038562}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)
			elif(int(dropTime-600) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 10 minutes", "color": 10038562}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)
			elif(int(dropTime-1800) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 30 minutes", "color": 10038562}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)

		requests.post(webHook, json={"embeds": [{"title": "Dropped", "description": f"The name {name} has dropped", "color": 10038562}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})

@bot.event
async def on_ready():
	print(f'\033[90m[\033[92m+\033[90m]\033[39m {bot.user} Is now: \033[92mOnline\033[39m')

@bot.command(name='remind', description="Set a reminder for a name")
async def set_reminder(ctx, name):
	if(str(ctx.message.author.id) in access):
		await ctx.send(f"Setting reminder for: {name}")
		threading.Thread(target=add_Reminder, args=(name,)).start()
	else:
		print(f"{ctx.message.author.id} Tried to set a reminder without access")

nest_asyncio.apply()
init() #This starts colorama
bot.run(botToken) #Start the bot
