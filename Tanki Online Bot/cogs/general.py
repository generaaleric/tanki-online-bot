import dbl
import discord
import aiohttp
import datetime
import time
import json
import requests
import random
import aiosqlite
import sqlite3
import asyncio
from operator import itemgetter
import re
from random import randint
from random import choice as randchoice
from discord.ext.commands import Bot
from discord.ext import commands
import discord.enums
from tinydb import TinyDB, Query
from tinydb import where
import aiosqlite
from tinydb.operations import delete,increment
import data.checks as checks
from data.checks import blacklist_check



tu = datetime.datetime.now()

cm = TinyDB('commands.json')
Commands = Query()

def contains_word(s, w):
	return (' ' + w + ' ') in (' ' + s + ' ')

def ConvertSectoDay(seconds):
    intervals = (
	('decades', 315569520),
	('years', 31556952),
	('months', 2592000),
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result)

class General:
	def __init__(self, bot):
		self.bot = bot

	def contains_word(s, w):
		return (' ' + w + ' ') in (' ' + s + ' ')

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def war(self, ctx):
		async def fetch(session, url):
			async with session.get(url) as response:
				return await response.text()
		mydict = {}
		async def main():
			async with aiohttp.ClientSession() as session:
				html = await fetch(session, 'https://tankionline.com/pages/war_of_thrones/')
				lannies = re.findall(r"LANNS = '(\d+)'", html)
				staries = re.findall(r"STARIES = '(\d+)'", html)
				targies = re.findall(r"TARGIES = '(\d+)'", html)
				mydict["<:Lannies2:564980321129332797>  Lannies"] = lannies[0]
				mydict["<:Staries2:564980303739748382>  Staries"] = staries[0]
				mydict["<:Targies2:564980312430608384> Targies"] = targies[0]
		await main()
		newdict = sorted(mydict.items(), key=itemgetter(1), reverse = True)
		print(newdict)
		print(f"First: {newdict[0][0]} with {int(newdict[0][1]):,} stars")
		embed=discord.Embed(title="War Of Thrones",url="https://tankionline.com/pages/war_of_thrones/?lang=en", color=0x00ffff)
		#embed.set_image(url="https://i.imgur.com/8ReFcN5.png")

		embed.add_field(name="\u200b", value="\u200b", inline=True)
		embed.add_field(name=f"🥇{newdict[0][0]}", value=f"{int(newdict[0][1]):,} stars", inline=True)
		embed.add_field(name="\u200b", value="\u200b")
		embed.add_field(name=f"🥈{newdict[1][0]}", value=f"{int(newdict[1][1]):,} stars", inline=True)
		embed.add_field(name="\u200b", value="\u200b", inline=True)
		embed.add_field(name=f"🥉{newdict[2][0]}", value=f"{int(newdict[2][1]):,} stars", inline=True)
		await self.bot.say(embed=embed)



	@commands.command(pass_context = True, aliases = ["rep"])
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def reputation(self, ctx, user: discord.Member = None):
		if cm.contains(Commands.command == 'reputation'):
			cm.update(increment('usage'), Commands.command == 'reputation')
		else:
			cm.insert({'command': "reputation", 'usage': 1})
		if user is None:
			embed=discord.Embed(title=f"{ctx.message.author.display_name}, Correct usage:", description="`>reputation <user>`", color=0x00ffff)
			return await self.bot.say(embed=embed)
		if user.id == ctx.message.author.id:
			embed=discord.Embed(title=f"{ctx.message.author.display_name} you cannot give yourself a reputation point!", color=0x00ffff)
			return await self.bot.say(embed=embed)
		data = await checks.database_check(self, ctx.message.author.id)
		userdata = await checks.database_check(self, user.id)
		if data is None:
			embed=discord.Embed(title=f"{ctx.message.author.display_name}, you are not registered!\nUse `>register`", color=0x00ffff)
			return await self.bot.say(embed=embed)
		if userdata is None:
			embed=discord.Embed(title=f"{ctx.message.author.display_name}, {user.display_name} is not registered!", color=0x00ffff)
			return await self.bot.say(embed=embed)
		ts = time.time()
		cooldown = data[17]
		if int(cooldown) >= int(ts):
			cooldown = ConvertSectoDay(int(cooldown) - int(ts))
			embed=discord.Embed(title=f"{ctx.message.author.display_name} you can give a reputation point again in {cooldown}", color=0x00ffff)
			return await self.bot.say(embed=embed)
		async with aiosqlite.connect('database.db') as db:
			cursor = await db.execute("UPDATE users SET reputations = reputations + 1 WHERE id = :id", {'id': user.id})
			await db.commit()
			await cursor.close()
		async with aiosqlite.connect('database.db') as db:
			cursor = await db.execute("UPDATE users SET repcooldown = :repcooldown WHERE id = :id", {'repcooldown': ts + 86400,'id': ctx.message.author.id})
			await db.commit()
			await cursor.close()
		embed=discord.Embed(title=f"{ctx.message.author.display_name} awarded a reputation point to {user.display_name}!", color=0x00ffff)
		return await self.bot.say(embed=embed)

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def premium(self, ctx):
		if cm.contains(Commands.command == 'premium'):
			cm.update(increment('usage'), Commands.command == 'premium')
		else:
			cm.insert({'command': "premium", 'usage': 1})
		await self.bot.say("Premium account users have the following perks:\n     • Double Crystals on rank up\n     • Double XP when opening containers\n     • Double rewards in >daily, >hourly and >rewards command.\n\nHow to get premium?\nGiveaways in supprt server or you can buy 1$/ Month and contributor role in support server.")

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def stars(self, ctx, stars: int = None):
		if cm.contains(Commands.command == 'stars'):
			cm.update(increment('usage'), Commands.command == 'stars')
		else:
			cm.insert({'command': "stars", 'usage': 1})
		if stars is None:
			return await self.bot.say("You didn't give me any stars to calculate!")
		if stars > 10000:
			return await self.bot.say("Are you kidding me? You can't even earn 2k. Go farm stars")
		if stars <= 0:
			return await self.bot.say("The minimum star is 1.")
		seconds = int(stars) * 210
		bseconds = int(stars) * 70
		time1 = ConvertSectoDay(seconds)
		time2 = ConvertSectoDay(bseconds)
		battles = seconds / 420
		bbattles = bseconds / 420
		embed=discord.Embed(title="Stars Calculator", description=f"An average player would need **{time1} | {int(battles)} battles** to earn {stars} stars and with premium account **{time2} | {int(bbattles)} battles**.\n_Note: Time shown is playing non-stop._", color=0x00ffff)
		await self.bot.say(embed=embed)

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def report(self, ctx, arg1, *, arg2 = None):
		if cm.contains(Commands.command == 'report'):
			cm.update(increment('usage'), Commands.command == 'report')
		else:
			cm.insert({'command': "report", 'usage': 1})
		if arg2 is None:
			return await self.bot.say("**Correct Usage:** `>report @Blload#6680 Using third party programs to open containers while he is afk. Server: [Invite Link]`")
		blload = await self.bot.get_user_info("175680857569230848")
		await self.bot.send_message(blload, f"**Reported by:** {ctx.message.author}\n**Offender:**{arg1}\n**Reason:** {arg2}")
		await self.bot.delete_message(ctx.message)
		await self.bot.say("User has been reported!")

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.owner_only()
	async def change_game_status(self, ctx, *, arg = None):
		await self.bot.change_presence(game=discord.Game(name=arg))
		await self.bot.say(f"Successfully changed game status to `{arg}`")


	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def feedback(self, ctx, *, arg = None):
		if cm.contains(Commands.command == 'feedback'):
			cm.update(increment('usage'), Commands.command == 'feedback')
		else:
			cm.insert({'command': "feedback", 'usage': 1})
		if arg is None:
			return await self.bot.say("I can't send an empty feedback!")
		blload = await self.bot.get_user_info("175680857569230848")
		await self.bot.send_message(blload, f"**From:** {ctx.message.author}\n**Feedback:** {arg}")
		await self.bot.delete_message(ctx.message)
		await self.bot.say("You feedback has been sent!")

	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def owner(self, ctx):
		if cm.contains(Commands.command == 'owner'):
			cm.update(increment('usage'), Commands.command == 'owner')
		else:
			cm.insert({'command': "owner", 'usage': 1})
		sum = 0
		servers = self.bot.servers
		for server in servers:
			sum += server.member_count
		embed=discord.Embed(title="Profile card",url="http://www.tankionlinebot.com", color=0x00ffff)
		embed.add_field(name="Information", value="**Real name:** Alexandros Neli\n**Age:** 19\n**Sex:** Male\n**Instagram:** @alexandrosneli | @alexandrosneliphotography", inline=False)
		embed.add_field(name="Other Information", value="<:logo:483631810404679690> **Creator of the Tanki Online Bot**\nTanki Online bot, created on December 17th 2017, the most reputed tanki bot on Discord, in over {:,} servers and in use with {:,} users.\n**Descrption:** View Tanki Online statistics right from discord, Open Containers, Sell containers and much more!\n**Website:** [www.tankionlinebot.ml](http://tankionlinebot.ml/)".format(len(self.bot.servers), sum), inline=True)
		await self.bot.say(embed=embed)


	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	async def records(self, ctx):
		if cm.contains(Commands.command == 'records'):
			cm.update(increment('usage'), Commands.command == 'records')
		else:
			cm.insert({'command': "records", 'usage': 1})
		embed=discord.Embed(title="Tanki Online Bot Records",url="http://www.tankionlinebot.com", color=0x00ffff)
		embed.set_thumbnail(url="https://i.imgur.com/vqJPUbc.png")
		embed.add_field(name="• Most crystals earned at once •", value="**   ‍     ‍    ‍   ‍        CookiesGirly:** 289,796,891 Crystals", inline=False)
		embed.add_field(name="• Most crystals owned at once •", value="**   ‍    ‍         ‍    ‍     CookiesGirly:** 289,802,982 Crystals", inline=False)
		embed.add_field(name="• Most red crystals owned at once •", value="**   ‍    ‍         ‍    ‍     D.R.I.N.K.E.R:** 9,300 Red Crystals", inline=False)
		embed.add_field(name="• Highest win rate •", value="**   ‍    ‍         ‍    ‍     Slav:** 83% Win Ratio", inline=False)
		embed.set_footer(text="Last Updated: 2/4/2019 | Have a record you want to submit? DM Blload#6680")
		await self.bot.say(embed=embed)

	# @commands.command(pass_context=True)
	# @commands.cooldown(1, 3, commands.BucketType.user)
	# @checks.owner_only()
	# async def asdd(self, ctx):
		# async with aiosqlite.connect('database.db') as db:
		# 	cursor = await db.execute('SELECT * FROM clans')
		# 	test = await cursor.fetchall()
		# 	await cursor.close()
		# clanTags = []
		# clanNames = []
		# for x in test:
		# 	clanTags.append(x[4])
		# 	clanNames.append(x[3])
		# print(clanTags)
		# print(clanNames)
		# async with aiosqlite.connect('database.db') as db:
		# 	cursor = await db.execute("UPDATE users SET reputations = 0")
		# 	await db.commit()
		# 	await cursor.close()
		# async with aiosqlite.connect('database.db') as db:
		# 	cursor = await db.execute("UPDATE users SET repcooldown = 0")
		# 	await db.commit()
		# 	await cursor.close()

	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def set(self, ctx, nick = None):
		if cm.contains(Commands.command == 'set'):
			cm.update(increment('usage'), Commands.command == 'set')
		else:
			cm.insert({'command': "set", 'usage': 1})
		data = await checks.database_check(self, ctx.message.author.id)
		if data is None:
			embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		elif nick is None:
			embed=discord.Embed(title="{}, you didn't provide a nickname!".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		else:
			async with aiosqlite.connect('database.db') as db:
				cursor = await db.execute("UPDATE users SET tankinick = :tankinick WHERE id = :id",
					{'tankinick': nick, 'id': ctx.message.author.id})
				await db.commit()
				await cursor.close()
			embed=discord.Embed(title="{}, you have successfully linked your Tanki Online profile.".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)

	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def nickname(self, ctx, nick = None):
		if cm.contains(Commands.command == 'nickname'):
			cm.update(increment('usage'), Commands.command == 'nickname')
		else:
			cm.insert({'command': "nickname", 'usage': 1})
		chat_filter = ["pornhub", "fuck", "discord.gg", "fack", "gay", "cancer", "bastard", "porn", "fcuk", "suck me", "suck my", "sack my", "sack me", "suckme", "sackme", "fck", "fvck", "sex", "blowjob", "dick", "pussy", "pusy", "bitch", "cunt", "nigga", "fuk", "jizz", "xnxx", "xxx", "chaturbate"]
		if cm.contains(Commands.command == 'nickname'):
			cm.update(increment('usage'), Commands.command == 'nickname')
		else:
			cm.insert({'command': "nickname", 'usage': 1})
		data = await checks.database_check(self, ctx.message.author.id)
		async with aiosqlite.connect('database.db') as db:
			cursor = await db.execute('SELECT * FROM users WHERE name=:name', {'name': nick})
			qwe = await cursor.fetchone()
			await cursor.close()
		if data is None:
			embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		if nick is None:
			embed=discord.Embed(title="{}, please provide a nickname.".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		if len(nick) > 20:
			embed=discord.Embed(title="{}, this nickname is too big!".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		if any(badword in nick.lower() for badword in chat_filter):
			embed=discord.Embed(title="{}, insults are not allowed!".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		if qwe is None:
			coins = data[7]
			nickk = data[2]
			redcry = data[15]
			if redcry < 50:
				embed=discord.Embed(title=f"{ctx.message.author.display_name}, you do not have enough red crystals to change your nickname. You need {redcry - 50}  more.", color=0x00ffff)
				return await self.bot.say(embed=embed)
			embed=discord.Embed(title='{} are you sure you want to change your nickname to **{}** for 50 red crystals? Yes/No'.format(ctx.message.author.display_name, nick), color=0x00ffff)
			await self.bot.say(embed=embed)
			msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
			if msg is None:
				return await self.bot.say("**{}** Took too long to respond".format(ctx.message.author.display_name))
			if msg.content.lower() == "yes":
				async with aiosqlite.connect('database.db') as db:
					cursor = await db.execute("UPDATE users SET name = :name WHERE id = :id",
	                    {'name': nick, 'id': ctx.message.author.id})
					await db.commit()
					await cursor.close()
				async with aiosqlite.connect('database.db') as db:
					cursor = await db.execute("UPDATE containers SET name = :name WHERE id = :id",
	                    {'name': nick, 'id': ctx.message.author.id})
					await db.commit()
					await cursor.close()
				totalcoins = redcry - 50
				async with aiosqlite.connect('database.db') as db:
					cursor = await db.execute("UPDATE users SET redcrystals = :redcrystals WHERE id = :id",
	                    {'redcrystals': totalcoins, 'id': ctx.message.author.id})
					await db.commit()
					await cursor.close()
				embed=discord.Embed(title='{}, your new nickname is **{}**'.format(ctx.message.author.display_name, nick), color=0x00ffff)
				await self.bot.say(embed=embed)
			elif msg.content.lower() == "no":
				embed=discord.Embed(title='{}, exiting menu'.format(ctx.message.author.display_name), color=0x00ffff)
				return await self.bot.say(embed=embed)
			else:
				embed=discord.Embed(title='{}, invalid response.'.format(ctx.message.author.display_name), color=0x00ffff)
				return await self.bot.say(embed=embed)
		else:
			embed=discord.Embed(title="{}, that nickname is taken!".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)




	@commands.command(pass_context=True, aliases=["cf"])
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def coinflip(self, ctx, bet: int = None):
		if cm.contains(Commands.command == 'coinflip'):
			cm.update(increment('usage'), Commands.command == 'coinflip')
		else:
			cm.insert({'command': "coinflip", 'usage': 1})
		if bet is None:
			embed=discord.Embed(title="{} You need to enter an amount".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		data = await checks.database_check(self, ctx.message.author.id)
		if data is None:
			embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		coins = data[7]
		if bet < 1:
			embed=discord.Embed(title="{} The minimum bet is 1 crystal.".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		elif bet > 500000:
			embed=discord.Embed(title="{} The maximum bet is 500,000 crystal.".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		elif bet > coins:
			embed=discord.Embed(title="{} You only have {:,} crystals".format(ctx.message.author.display_name, coins), color=0x00ffff)
			return await self.bot.say(embed=embed)
		else:
			flip = random.choice(["heads", "tails"])
			embed=discord.Embed(title='Please choose Heads or Tails'.format(ctx.message.author.display_name), color=0x00ffff)
			await self.bot.say(embed=embed)
			msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
			msgs = ["heads", "tails"]
			if msg is None:
				return await self.bot.say("**{}** Took too long to respond".format(ctx.message.author.display_name))
			elif msg.content.lower() not in msgs:
				return await self.bot.say("**{}** Thats an invalid response".format(ctx.message.author.display_name))
			if flip == msg.content.lower():
				totalcoins = coins + bet
				async with aiosqlite.connect('database.db') as db:
					cursor = await db.execute("UPDATE users SET coins = :bet WHERE id = :id",
						{'bet': totalcoins, 'id': ctx.message.author.id})
					await db.commit()
					await cursor.close()
				embed=discord.Embed(title="{}, It's {}, you won! +{:,} crystals\nTotal Crystals: {:,}".format(ctx.message.author.display_name, flip, bet, totalcoins), color=0x32cd32)
				await self.bot.say(embed=embed)
			else:
				totalcoins = coins - bet
				async with aiosqlite.connect('database.db') as db:
					cursor = await db.execute("UPDATE users SET coins = :bet WHERE id = :id",
						{'bet': totalcoins, 'id': ctx.message.author.id})
					await db.commit()
					await cursor.close()
				embed=discord.Embed(title="{}, It's {}, you lost! -{:,} crystals\nTotal Crystals: {:,}".format(ctx.message.author.display_name, flip, bet, totalcoins), color=0xd8261a)
				await self.bot.say(embed=embed)

	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def vote(self, ctx):
		if cm.contains(Commands.command == 'vote'):
			cm.update(increment('usage'), Commands.command == 'vote')
		else:
			cm.insert({'command': "vote", 'usage': 1})
		await self.bot.say(":arrow_up: **Vote for the bot! https://discordbots.org/bot/408439037771382794/vote**")


	@commands.command(pass_context = True, aliases=["update"])
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def updates(self, ctx):
		if cm.contains(Commands.command == 'updates'):
			cm.update(increment('usage'), Commands.command == 'updates')
		else:
			cm.insert({'command': "updates", 'usage': 1})
		updates = "**-==[BigUpdate]==-**\n__------**Battle System Reworked**-------__\n\n:small_orange_diamond:  **__Got bored of random winners?__**  :small_orange_diamond:\n:small_orange_diamond:  **_With the new update you will be able to buy Turrets/Hulls and upgrade them to M1, M2, M3 and fight with them!_** :small_orange_diamond:\n\n**__New commands:__** `>shop`, `>buy`, `>garage`, `>equip`\n**__Commands renamed:__**` >c open ` => `>open`, `>c sell` => `>sell`, `>c inv`, `c  buy` => `>buy [amount]`\n\n• Removed unnecessary leaderboards.\n• Wins/Loses stats has been reset due to the new battle system.\n• Added leaderboard place to profile and clan profile\n• Removed unnecessary info from clan members command\n• Fixed a lot of minor errors/bugs\nInformation about Turrets/Hulls. Having something M3 doesn't mean its stronger than an M0. For example Firebird is the weakest turret and Shaft the strongest one in the bot. Firebird m3 does an average damage of 30. and Shaft m3 up to 500 damage. Same with hulls. You can check their stats using the stats command. `>stats Shaft m3`"
		await self.bot.say(updates)
		# embed=discord.Embed(title="Tanki Online Bot", color=0x00ffff)
		# embed.add_field(name = "Latest Updates", value = updates)
		# await self.bot.say(embed=embed)


	@commands.command(pass_context = True)
	@commands.cooldown(1, 86400, commands.BucketType.user)
	@checks.blacklist_check()
	async def daily(self, ctx):
		if cm.contains(Commands.command == 'daily'):
			cm.update(increment('usage'), Commands.command == 'daily')
		else:
			cm.insert({'command': "daily", 'usage': 1})
		dataa = await checks.database_check(self, ctx.message.author.id)
		if dataa is None:
			embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
			return await self.bot.say(embed=embed)
		premium = dataa[5]
		if premium == "Yes":
			cry = 15000 * 2
			clr = color=0xffff00
		else:
			cry = 15000
			clr = color = 0x00ffff
		async with aiosqlite.connect('database.db') as db:
			cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
				{'coins': cry, 'id': ctx.message.author.id})
			await db.commit()
			await cursor.close()
		embed=discord.Embed(title="{}, you received {:,} crystals!".format(ctx.message.author.display_name, cry), color=clr)
		return await self.bot.say(embed=embed)


	@commands.command(pass_context = True)
	@commands.cooldown(1, 3600, commands.BucketType.user)
	@checks.blacklist_check()
	async def donate(self, ctx):
		if cm.contains(Commands.command == 'donate'):
			cm.update(increment('usage'), Commands.command == 'donate')
		else:
			cm.insert({'command': "donate", 'usage': 1})
		await self.bot.say("https://www.paypal.me/tankionlinecontainer")

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3600, commands.BucketType.user)
	@checks.blacklist_check()
	async def hourly(self, ctx):
		if cm.contains(Commands.command == 'hourly'):
			cm.update(increment('usage'), Commands.command == 'hourly')
		else:
			cm.insert({'command': "hourly", 'usage': 1})

		dataa = await checks.database_check(self, ctx.message.author.id)
		if dataa is None:
			embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=clr)
			return await self.bot.say(embed=embed)
		premium = dataa[5]
		if premium == "Yes":
			cry = 5000 * 2
			clr = color = 0xffff00
		else:
			cry = 5000
			clr = color = 0x00ffff
		async with aiosqlite.connect('database.db') as db:
			cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
				{'coins': cry, 'id': ctx.message.author.id})
			await db.commit()
			await cursor.close()
		embed=discord.Embed(title="{}, you received {:,} crystals!".format(ctx.message.author.display_name, cry), color=clr)
		return await self.bot.say(embed=embed)

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def usages(self, ctx):
		commands = ["info",
		       "updates",
		       "stats",
		       "credits",
		       "vote",
		       "bitcoin",
		       "usages",
			   "voted",
		       "reputation",
		       "owner",
		       "feedback",
		       "report",
		       "level",
		       "inventory",
		       "leaderboard",
		       "open",
		       "sell",
		       "container",
		       "drop",
		       "rewards",
		       "records",
		       "nickname",
		       "daily",
		       "hourly",
		       "coinflip",
		       "shop",
		       "buy",
			   "garage",
		       "equip",
		       "battle",
		       "stats",
			   "reset",
			   "register",
			   "unregister",
			   "set",
			   "donate",
			   "premium",
			   "clan",
			   "ratings",
			   "xp",
			   "supplies",
			   "stars",
			   "weekly",
			   "gamemodes",
			   "invite",
			   "top"]
		listt = []
		for asd in cm:
			listt.append(asd["usage"])
		embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", color=0x00ffff)
		embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
		embed.add_field(name="{:,} commands have been used in total!".format(sum(listt)), value="Requested by {}".format(ctx.message.author.display_name), inline=True)
		return await self.bot.say(embed=embed)

	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def invite(self, ctx):
		if cm.contains(Commands.command == 'invite'):
			cm.update(increment('usage'), Commands.command == 'invite')
		else:
			cm.insert({'command': "invite", 'usage': 1})
		await self.bot.say("Want me to join your server? Click the link below!\nhttp://www.tankionlinebot.com/")

	@commands.command(pass_context = True, aliases=["credit"])
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def credits(self, ctx):
		if cm.contains(Commands.command == 'credits'):
			cm.update(increment('usage'), Commands.command == 'credits')

		else:
			cm.insert({'command': "credits", 'usage': 1})
		embed = discord.Embed(title="Tanki Online", description="Thanks to all of the people who helped make Tanki Online Bot possible", colour=discord.Colour(0x42d9f4))
		embed.set_author(name="Tanki Online", url="http://www.tankionlinebot.com", icon_url="https://i.imgur.com/4SKYtfq.png")
		embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
		blload = await self.bot.get_user_info("175680857569230848")
		quick = await self.bot.get_user_info("326366976853409803")
		ahsan = await self.bot.get_user_info("321673115891531787")
		#harvest = await self.bot.get_user_info("340063097949650945")
		greatest = await self.bot.get_user_info("396252017707843585")
		slav = await self.bot.get_user_info("255250213634179083")
		#bornkiller = await self.bot.get_user_info("393111149400293412")
		viceroy = await self.bot.get_user_info("464450798969946133")
		#rocket = await self.bot.get_user_info("387383995882799131")
		hexed = await self.bot.get_user_info("248816519180582912")
		poke = await self.bot.get_user_info("232167384742494208")
		geop = await self.bot.get_user_info("216156825978929152")
		embed.add_field(name="Code / Development", value=blload)
		embed.add_field(name="Website Development", value=quick)
		embed.add_field(name="Support", value=f"{blload}\n{quick}\n{ahsan}")
		embed.add_field(name="GFX", value=blload)
		embed.add_field(name="Items ID", value=f"{blload}\n{ahsan}")
		embed.add_field(name="Special Thanks", value=f"{hexed}\n{poke}\n{geop}")
		embed.add_field(name="Beta Testers", value=f"{ahsan}\n{greatest}\n{quick}\n{slav}\n{viceroy}")
		await self.bot.say(embed=embed)

	@commands.command(pass_context = True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def info(self, ctx):
		if cm.contains(Commands.command == 'info'):
			cm.update(increment('usage'), Commands.command == 'info')

		else:
			cm.insert({'command': "info", 'usage': 1})
		sum = 0
		servers = self.bot.servers
		for server in servers:
			sum += server.member_count
		embed = discord.Embed(title="\u200b", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
		embed.set_author(name="Tanki Online", url="http://www.tankionlinebot.com", icon_url="https://i.imgur.com/4SKYtfq.png")
		embed.add_field(name="Servers", value="{:,}".format(len(self.bot.servers)))
		embed.add_field(name="Users", value="{:,}".format(sum))
		embed.add_field(name="Owner", value="Blload#6680")
		embed.add_field(name="Support server", value="[Link](https://discord.gg/pXjDfHF)")
		embed.add_field(name="Donate", value="[Link](https://www.paypal.me/tankionlinecontainer)")
		embed.add_field(name="Website", value="[Link](http://www.tankionlinebot.com/)")
		embed.add_field(name="Invite", value="[Link](https://discordapp.com/api/oauth2/authorize?client_id=408439037771382794&permissions=1610087511&scope=bot)")
		await self.bot.say(embed=embed)



	@commands.command(pass_context=True)
	@commands.cooldown(1, 3, commands.BucketType.user)
	@checks.blacklist_check()
	async def bitcoin(self, ctx):
		if cm.contains(Commands.command == 'bitcoin'):
			cm.update(increment('usage'), Commands.command == 'bitcoin')

		else:
			cm.insert({'command': "bitcoin", 'usage': 1})
		url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
		response = requests.get(url)
		value = response.json()['bpi']['USD']['rate']
		await self.bot.say("Bitcoin price is: $" + value)

def setup(bot):
	bot.add_cog(General(bot))
