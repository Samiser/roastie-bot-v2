#Command for autoroasting when you can't think of a roast
from command import Command
import random

class AutoRoast(Command):
	def __init__(self, client):
		super().__init__(client)
		self.name = 'autoroast'
		self.brief = 'For when you just don\'t know what to say!'
		self.description = 'Use this command to roast another person without any effort.\n\n'\
							'To use it, just type "!autoroast @name"\n'

	async def run(self, message, args):
			roasts = ["Well I really like ur track but I think it could be better really u should add more eq and compression and I think there should be more cool noises and stuff and maybe change some of the sounds to make it more fat and thick you know and maybe make sure you arrange ur track before mixing and then you master it",
						"Hmm interesting track I don't really like it and it's not my genre so I can't relly comment I only really make experimental music so I don't really know about this genre so I don't know what to say but I think maybe you should eq it a bit better and mix it some more and change the arrangement up so it sounds fresh and new",
						"WOWO I LOVE YOUR TRACK DUDE can you pm me how you did that thing with the bass it sounds so cool anyway I just wanted to say your track is awesome maybe u could change ur timbres and stuff I don't really know I'm not a pro producer so it's hard for me u know anyway keep goin with your producing its sounding good",
						"Lol this track is pretty bad I would maybe just delete it and start again with some new plugins and maybe a new daw and this time make sure ur bass is way better and eq'd more"]
			
			await self.client.send_message(message.channel, "{} {}".format(message.mentions[0].mention, random.choice(roasts)))