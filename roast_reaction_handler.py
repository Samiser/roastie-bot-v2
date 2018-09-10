from dbedit import dbedit

class ReactionHandler:
	def __init__(self, client, config):
		self.client = client
		self.config = config
		
	async def handle(self, reaction, user):
		#List of reactions
		reactions = [[self.config["Emojis"]["NonRoasts"], 'nonroasts', self.config["XpReward"]["NonRoasts"], 'You must do a proper one before you can post. Try again!'],
					[self.config["Emojis"]["BadRoasts"], 'badroasts', self.config["XpReward"]["BadRoasts"], 'Next time, try to be more specific and to give solutions to any problems you can hear.\n\nYou may now post.'],
					[self.config["Emojis"]["GoodRoasts"], 'goodroasts', self.config["XpReward"]["GoodRoasts"], 'Great job! Thanks for giving a solid roast.\n\nYou may now post.'], 
					[self.config["Emojis"]["FireRoasts"], 'fireroasts', self.config["XpReward"]["FireRoasts"], 'Wowsers, you nailed it. Thanks for giving an excellent roast!\n\nYou may now post.']]
		
		if user.bot: return
		elif user not in reaction.message.mentions: return
		elif dbedit.rated(reaction.message): return
		
		for i in reactions:
			if reaction.emoji == i[0]:
				#Log vote and Post to channel
				await self.client.send_message(reaction.message.channel, "{} {} has voted your roast as {}\n\n{}".format(reaction.message.author.mention, user.name, reaction.emoji, i[3]))
				
				#Update roast in roastsnposts table with rating
				await dbedit.rate_roast(reaction, reactions.index(i))
				
				#Update post in roastsnposts table that it has been roasted
				await dbedit.post_roasted(user, reaction.message.author)
				
				#Increment type of roast count
				print("User {}'s {} incremented by 1".format(reaction.message.author, i[1]))
				dbedit.increment(reaction.message.author, i[1], 1)
				
				if i[1] != 'nonroasts':
					#Increment total roast count
					print("User {}'s roastcount incremented by 1".format(reaction.message.author))
					dbedit.increment(reaction.message.author, 'roastcount', 1)
					
				#Increment roast xp
				print("User {}'s {} incremented by {}\n".format(reaction.message.author, 'roastxp', int(i[2])))
				dbedit.increment(reaction.message.author, 'roastxp', int(i[2]))
			await self.client.remove_reaction(reaction.message, i[0], self.client.user)