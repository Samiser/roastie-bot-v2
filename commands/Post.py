#Command for posting

import re
from command import Command
from dbedit import dbedit

class Post(Command):
	def __init__(self, client):
		super().__init__(client)
		self.name = 'post'
		self.brief = 'Submit your track for a good roasting!'
		self.description = 'Use this command to attach your track '\
							'to a post so it can be roasted. Your track will '\
							'then be roasted by another producer. '\
							'\n\nTo use this command '\
							'type "!post [link to post] [optional brief message about post]".\n\n'\
							'Example: "!post soundbound.org/mytrack This is my first attempt at this genre! '\
							'Would love to hear your opinions."'
							
	async def run(self, message, args):
		if await self.valid_post(message):
			#Check if user in database
			dbedit.presence_check(message)
			#Add roast to roastsnposts database
			await dbedit.new_post(message)
			await self.client.send_message(message.channel, "Post successful")
		else:
			await self.client.delete_message(message)
			
	async def valid_post(self, message):
		#Post is valid if there is an attachment or a link
		#And if the user has more roasts than posts
		#And if user has no currently unroasted posts
		regex = re.compile(
				r'^https?://'  # http:// or https://
				r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
				r'localhost|'  # localhost...
				r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
				r'(?::\d+)?'  # optional port
				r'(?:/?|[/?]\S+)$', re.IGNORECASE)
				
		url = re.findall(regex, message.content)
		
		if not dbedit.can_post(message.author):
			await self.client.send_message(message.channel, "Roast before you post!")
			return False
		elif dbedit.has_unroasted_posts(message.author):
			await self.client.send_message(message.channel, "You may only have one unroasted post at a time")
			return False
		elif not url and not message.embeds and not message.attachments:
			await self.client.send_message(message.channel, "You must link/attach the track you want roasted")
			return False
		else:
			return True