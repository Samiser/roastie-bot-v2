import os
import inspect
import importlib
from command import Command

class CommandHandler:
	def __init__(self, client, config):
		self.client = client
		self.prefix = config["Discord"]["Prefix"]
		self.commands = dict()
		
	async def handle(self, message):
		#Checks for a command and runs the command if one is present
		#Don't respond to bot
		if message.author.bot: return
		#Check for a prefix
		elif message.content[:len(self.prefix)] != self.prefix: return
		else:
			#Get the command
			command = message.content.split()[0][len(self.prefix):]
			#Seperate other parts of message into a list
			args = message.content.split()[1:]
			#Check if it's a real command
			if command in self.commands:
				await self.commands[command].run(message, args)
			
	def register_command(self, command):
		#Registers command to the bot
		#Check if Command
		if not issubclass(command, Command):
			print("Command not added; invalid command")
			return
		else:
			#Create an instance of the command class
			cmd = command(self.client)
			#Check for a name
			if cmd.name == None:
				print("Command not added; missing name")
				return
			#Check if already added
			elif cmd.name in self.commands:
				print(f"Command {cmd.name} not added; already exists")
				return
			else:
				#Add the Command
				self.commands[cmd.name] = cmd
				print(f"Command {cmd.name} loaded successfully")
		
	def register_commands_in_dir(self, dir):
		#Registers all commands within a directory
		#Get all files in dir
		for root, dirs, files in os.walk(f'{dir}'):
			for filename in files:
				#Filter out .pyc files
				if filename[-1] != 'c':
					#Get module name
					name = filename[:-3]
					#Get all module members
					members = inspect.getmembers(importlib.import_module(name))
					for member in members:
						#Get the main class member
						if inspect.isclass(member[1]) and member[1].__name__.lower() == name.lower():
							#Finally, register that command
							self.register_command(member[1])