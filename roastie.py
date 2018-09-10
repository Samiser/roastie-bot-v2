#Roastie bot
#Version 2.0
#
#Written by Sam Heney

import sys
import os
import io
import discord
import configparser
from dbedit import dbedit
from command_handler import CommandHandler
from roast_reaction_handler import ReactionHandler

#Connect to users database
dbedit.setup()

#Get the list of folders and add to sys.path
for root, dirs, files in os.walk(r'.'):
	for dir in dirs[:3]:
		sys.path.append(os.path.realpath(f'{root}/{dir}'))

config = configparser.ConfigParser()
config.read('data/config.ini', encoding='utf-8')

#Create a discord client
client = discord.Client()
#Create handlers
handler = CommandHandler(client, config)
reactionHandler = ReactionHandler(client, config)
#Register all commands
handler.register_commands_in_dir('./commands')

@client.event
async def on_ready():
	print("Logged in as: " + str(client.user.name))

@client.event
async def on_reaction_add(reaction, user):
	#Pass reaction to handler
	await reactionHandler.handle(reaction, user)
	
@client.event
async def on_message(message):
	#Pass message to handler
	await handler.handle(message)
	
client.run(config['Discord']['Token'])