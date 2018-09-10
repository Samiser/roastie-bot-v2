#Command for fetching a user's roast xp
from command import Command
from dbedit import dbedit

class Xp(Command):
	def __init__(self, client):
		super().__init__(client)
		self.name = 'xp'
		self.brief = 'Get yours or another producer\'s roast xp'
		self.description = 'Use this command to get yours or another user\'s roast xp.\n\n'\
							'To get your own xp just type "!xp"\n'\
							'To get another producer\'s xp type "!xp @name"'

	async def run(self, message, args):
		if message.mentions:
			xp = await dbedit.get("roastxp", message.mentions[0])
			await self.client.send_message(message.channel, "{} has {} xp.".format(message.mentions[0].mention, xp))
		else:
			xp = await dbedit.get("roastxp", message.author)
			await self.client.send_message(message.channel, "{} has {} xp.".format(message.author.mention, xp))
			
		