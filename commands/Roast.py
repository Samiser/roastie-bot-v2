#Command for roasting

from command import Command
from dbedit import dbedit

class Roast(Command):
	def __init__(self, client):
		super().__init__(client)
		self.name = 'roast'
		self.brief = 'Roast another producer\'s post!'
		self.description = 'Use this command to roast another '\
							'producer\'s post. That producer may then '\
							'rate your roast, which (if your roast was good) '\
							'will earn you xp.\n\nTo use this command '\
							'type "!roast @producer postnumber roast".\n\n'\
							'Example: "!roast @Bean 163 I like this track but '\
							'you could eq the bass frequencies a bit higher"'
							
	async def run(self, message, args):
		if self.valid_roast(message):
			#Check if user in database
			dbedit.presence_check(message)
			#Add reactions to roast for voting
			await self.add_reactions(message)
			#Add roast to roastsnposts database
			await dbedit.new_roast(message)
			await self.client.send_message(message.channel, "Roasted!")
		else:
			await self.client.send_message(message.channel, "Invalid roast")
			
	def valid_roast(self, message):
		#Roast is valid if the message author and roastie are not mentioned and there is one mention
		if message.author not in message.mentions and self.client.user not in message.mentions and len(message.mentions) == 1:
			return True
			
	async def add_reactions(self, message):
		#Add reactions to roast for voting
		await self.client.add_reaction(message, "❌")
		await self.client.add_reaction(message, "👎")
		await self.client.add_reaction(message, "👍")
		await self.client.add_reaction(message, "🔥")