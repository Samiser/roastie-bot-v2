import sqlite3

class dbedit:
	def setup():
		try:
			db = sqlite3.connect('data/data.db')
			cursor = db.cursor()
			print("Connected to data/data.db")
			#If database doesn't exist. make it)
			cursor.execute('''CREATE TABLE IF NOT EXISTS users(
				username	TEXT,
				discordid	INTEGER,
				roastxp		INTEGER,
				roastcount	INTEGER,
				postcount	INTEGER,
				nonroasts	INTEGER,
				badroasts	INTEGER,
				goodroasts	INTEGER,
				fireroasts	INTEGER
			)''')
			cursor.execute('''CREATE TABLE IF NOT EXISTS roastsnposts(
				id INTEGER,
				discordid INTEGER,
				isroast INTEGER,
				israted INTEGER,
				content TEXT,
				rating INTEGER
			)''')
			#Commit changes
			db.commit()
		except Exception as e:
			# Roll back any change if something goes wrong
			db.rollback()
			raise e
			
		db.close()	
			
	def presence_check(message):
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		cursor.execute("SELECT * FROM users WHERE discordid=?", (message.author.id,))
		user = cursor.fetchone()
	
		#if it isn't, insert a new entry with their id:
		if (user == None):
			cursor.execute("INSERT INTO users(username, discordid, roastxp, roastcount, postcount, nonroasts, badroasts, goodroasts, fireroasts) VALUES(?,?,?,?,?,?,?,?,?)", (message.author.name,message.author.id,0,0,0,0,0,0,0))
			db.commit()
			cursor.execute("SELECT * FROM users WHERE discordid=?", (message.author.id,))
			user = cursor.fetchone()
			print(f"New user {message.author.name} inserted into database")
		
			#Commit
			db.commit()
			
		db.close()
		
	def increment(user, value, amount):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
		
		#Get index of value
		values = ['username', 'discordid', 'roastxp', 'roastcount', 'postcount', 'nonroasts', 'badroasts', 'goodroasts', 'fireroasts']
		for i in values:
			if value == i:
				valueIndex = values.index(i)
	
		#Update the database
		try:
			cursor.execute("UPDATE users SET {} = {}+{} WHERE discordid = {}".format(value, value, amount, user.id))
			db.commit()
		except Exception as e:
			# Roll back any change if something goes wrong
			db.rollback()
			raise e
			
		db.close()
		
	async def get(col, user):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		cursor.execute("SELECT {} FROM users WHERE discordid = {}".format(col, user.id))
		result = cursor.fetchone()[0]
		
		db.close()
		
		return(result)
		
	async def new_roast(message):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		cursor.execute("INSERT INTO roastsnposts(id, discordid, isroast, israted, content, rating) VALUES(?,?,?,?,?,?)", (message.id,message.author.id,1,0,'"'+message.clean_content+'"',0))
		db.commit()
		print("New roast by {}: {}".format(message.author.name, message.clean_content))
		
		db.close()
		
	async def new_post(message):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Increment poster's postcount
		cursor.execute("UPDATE users SET postcount = postcount+1 WHERE discordid = {}".format(message.author.id))
		db.commit()
	
		#Add post to roastsnposts
		cursor.execute("INSERT INTO roastsnposts(id, discordid, isroast, israted, content, rating) VALUES(?,?,?,?,?,?)", (message.id,message.author.id,0,0,'"'+message.clean_content+'"',0))
		db.commit()
		print("New post by {}: {}".format(message.author.name, message.clean_content))
		
		db.close()
		
	async def rate_roast(reaction, rating):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Set post to rated and store it's rating
		cursor.execute("UPDATE roastsnposts SET israted = 1, rating = {} WHERE id = {}".format(rating, reaction.message.id))
		db.commit()
		
		#Log event
		print("Roast by {} was rated as {}".format(reaction.message.author.name, rating))
		
		db.close()
		
	async def post_roasted(poster, roaster):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Get newly roasted post for log reference
		cursor.execute("SELECT * FROM roastsnposts WHERE discordid = {} AND isroast = 0 AND israted = 0".format(poster.id))
		post = cursor.fetchone()
	
		#Set post to roasted
		cursor.execute("UPDATE roastsnposts SET israted = 1 WHERE discordid = {} AND isroast = 0 AND israted = 0".format(poster.id))
		db.commit()
		
		#Log event
		print("Post by {} was roasted by {}".format(poster.name, roaster.name))
		
		#Close connection
		db.close()
		
	def can_post(author):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Compare roasts and posts
		cursor.execute("SELECT * FROM users WHERE discordid = {} AND roastcount > postcount".format(author.id))
		user = cursor.fetchone()
		
		#Close database connection
		db.close()
		
		#Return
		if user: return True
		
	def has_unroasted_posts(author):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Try and get unroasted posts by author
		cursor.execute("SELECT * FROM roastsnposts WHERE discordid = {} AND isroast = 0 AND israted = 0".format(author.id))
		post = cursor.fetchone()
		
		#Close connection
		db.close()
		
		#Return true if post is found
		if post: return True
		
	def rated(message):
		#Connect to database and assign cursor
		db = sqlite3.connect('data/data.db')
		cursor = db.cursor()
	
		#Get israted from the roast's record
		cursor.execute("SELECT israted FROM roastsnposts WHERE id = {}".format(message.id))
		israted = cursor.fetchone()[0]
		
		#Close connection
		db.close()
		
		#Return israted value
		return israted
		