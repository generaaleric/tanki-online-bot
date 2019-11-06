import discord
from discord.ext import commands
import aiosqlite
import json
import asyncio
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete

cm = TinyDB('data/blacklist.json')
Commands = Query()

listt = []
def blacklist_check():
	def predicate(ctx):
		for asd in cm:
			listt.append(asd["command"])
		return ctx.message.author.id not in listt
	return commands.check(predicate)

def owner_only():
	def predicate(ctx):
		whitelist = ["325610332150038530", "248816519180582912", "175680857569230848"]
		return ctx.message.author.id in whitelist
	return commands.check(predicate)

async def clan_create(self, clanid, id, owner, name, tag, member, memberid, membercount, clanslots, desc, created, rank, logo):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO clans VALUES (:clanid, :id, :owner, :name, :tag, :member, :memberid, :membercount, :clanslots, :desc, :created, :rank, :logo)", {'clanid': clanid, 'id': id, 'owner': owner, 'name': name, 'tag': tag, 'member': member, 'memberid': memberid, 'membercount' :membercount, 'clanslots' :clanslots, 'desc': desc, 'created': created, 'rank': rank, 'logo': logo})
		await db.commit()
		await cursor.close()
	return

async def clan_invite(self, clanid, id, owner, name, tag, member, memberid, membercount, clanslots, desc, created, rank, logo):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO clans VALUES (:clanid, :id, :owner, :name, :tag, :member, :memberid, :membercount, :clanslots, :desc, :created, :rank, :logo)", {'clanid': clanid, 'id': id, 'owner': owner, 'name': name, 'tag': tag, 'member': member, 'memberid': memberid, 'membercount' :membercount, 'clanslots' :clanslots, 'desc': desc, 'created': created, 'rank': rank, 'logo': logo})
		await db.commit()
		await cursor.close()
	return

async def clan_check(self, id):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute('SELECT * FROM clans WHERE memberid=:memberid', {'memberid': id})
		data = await cursor.fetchone()
		await cursor.close()
	return data

async def clan_members(self, id):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute('SELECT * FROM clans WHERE id=:id', {'id': id})
		data = await cursor.fetchall()
		await cursor.close()
	return data

async def clan_kick(self, memberid):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("DELETE FROM clans WHERE memberid=:memberid", {'memberid': memberid})
		await db.commit()
		await cursor.close()
	return

async def clan_delete(self, clanid):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("DELETE FROM clans WHERE clanid=:clanid", {'clanid': clanid})
		await db.commit()
		await cursor.close()
	return

async def database_check(self, id):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute('SELECT * FROM users WHERE id=:id', {'id': id})
		data = await cursor.fetchone()
		await cursor.close()
	return data

async def database_container_check(self, id):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute('SELECT * FROM containers WHERE id=:id', {'id': id})
		data = await cursor.fetchone()
		await cursor.close()
	return data

async def add_garage(self, id, name):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO garage VALUES (:id, :name, :wasp, :firebird, :hornet, :hunter, :viking, :dictator, :titan, :mammoth, :freeze, :isida, :hammer, :twins, :ricochet, :smoky, :striker, :vulcan, :thunder, :railgun, :magnum, :shaft)", {'id': id, 'name': name, 'wasp': 0, 'firebird': 0, 'hornet': None, 'hunter': None, 'viking': None, 'dictator': None, 'titan': None, 'mammoth': None, 'freeze': None, 'isida': None, 'hammer': None, 'twins': None, 'ricochet': None, 'smoky': None, 'striker': None, 'vulcan': None, 'thunder': None, 'railgun': None, 'magnum': None, 'shaft': None})
		await db.commit()
		await cursor.close()
	return

async def add_user(self, id, name):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO users VALUES (:id, :xp, :name, :level, :emoji, :premium, :rank, :coins, :containers, :wins, :losts, :premleft, :tankinick, :voted, :license, :redcrystals, :reputations, :repcooldown, :turret, :hull)", {'id': id, 'xp': 0, 'name': name, 'level': 'Recruit', 'emoji': ':Recruit:', 'premium': 'No', 'rank': 'https://i.imgur.com/tlyR0dt.png', 'coins': 10000, 'containers': 0, 'wins': 0, 'losts': 0, 'premleft': 0, 'tankinick': None, 'voted': False, 'license': None, 'redcrystals': 0, 'reputations': 0, 'repcooldown': 0, 'turret': 'Firebird m0', 'hull': 'Wasp m0'})
		await db.commit()
		await cursor.close()
	return

async def add_user_containers(self, id, name):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO containers VALUES (:id, :name, :amount, :common, :uncommon, :rare, :epic, :legendary, :exotic, :firstaid, :armor, :damage, :nitro, :mine, :gold, :battery, :turret, :hull, :rarepaint, :epicpaint, :legendarypaint)", {'id': id, 'name': name, 'amount': 0, 'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'exotic': 0, 'firstaid': 0, 'armor': 0, 'damage': 0, 'nitro': 0, 'mine': 0, 'gold': 0, 'battery': 0, 'turret': 0, 'hull': 0, 'rarepaint': 0, 'epicpaint': 0, 'legendarypaint': 0})
		await db.commit()
		await cursor.close()
	return

async def delete_user(self, id):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("DELETE FROM users WHERE id=:id", {'id': id})
		await db.commit()
		await cursor.close()
		cursor = await db.execute("DELETE FROM containers WHERE id=:id", {'id': id})
		await db.commit()
		await cursor.close()
	return

async def ban_check(self, id, name):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO users VALUES (:id, :xp, :name, :level, :emoji, :premium, :rank, :coins, :containers, :wins, :losts, :premleft, :tankinick, :voted, :license, :redcrystals, :reputations, :repcooldown, :turret, :hull)", {'id': id, 'xp': 0, 'name': name, 'level': 'Banned', 'emoji': ':Recruit:', 'premium': 'No', 'rank': 'https://i.imgur.com/40Nl0TE.png', 'coins': 0, 'containers': 0, 'wins': 0, 'losts': 0, 'premleft': 0, 'tankinick': None, 'voted': False, 'license': False, 'redcrystals': 0, 'reputations': 0, 'repcooldown': 0, 'turret': 'Firebird m0', 'hull': 'Wasp m0'})
		await db.commit()
		await cursor.close()
		cursor = await db.execute("INSERT INTO containers VALUES (:id, :name, :amount, :common, :uncommon, :rare, :epic, :legendary, :exotic, :firstaid, :armor, :damage, :nitro, :mine, :gold, :battery, :turret, :hull, :rarepaint, :epicpaint, :legendarypaint)", {'id': id, 'name': name, 'amount': 0, 'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'exotic': 0, 'firstaid': 0, 'armor': 0, 'damage': 0, 'nitro': 0, 'mine': 0, 'gold': 0, 'battery': 0, 'turret': 0, 'hull': 0, 'rarepaint': 0, 'epicpaint': 0, 'legendarypaint': 0})
		await db.commit()
		await cursor.close()
	cm.insert({'command': id})
	return


async def unban_check(self, id, name):
	async with aiosqlite.connect('database.db') as db:
		cursor = await db.execute("INSERT INTO users VALUES (:id, :xp, :name, :level, :emoji, :premium, :rank, :coins, :containers, :wins, :losts, :premleft, :tankinick, :voted, :license, :redcrystals, :reputations, :repcooldown, :turret, :hull)", {'id': id, 'xp': 0, 'name': name, 'level': 'Recruit', 'emoji': ':Recruit:', 'premium': 'No', 'rank': 'https://i.imgur.com/tlyR0dt.png', 'coins': 10000, 'containers': 0, 'wins': 0, 'losts': 0, 'premleft': 0, 'tankinick': None, 'voted': False, 'license': False, 'redcrystals': 0, 'reputations': 0, 'repcooldown': 0, 'turret': 'Firebird m0', 'hull': 'Wasp m0'})
		await db.commit()
		await cursor.close()
		cursor = await db.execute("INSERT INTO containers VALUES (:id, :name, :amount, :common, :uncommon, :rare, :epic, :legendary, :exotic, :firstaid, :armor, :damage, :nitro, :mine, :gold, :battery, :turret, :hull, :rarepaint, :epicpaint, :legendarypaint)", {'id': id, 'name': name, 'amount': 0, 'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'exotic': 0, 'firstaid': 0, 'armor': 0, 'damage': 0, 'nitro': 0, 'mine': 0, 'gold': 0, 'battery': 0, 'turret': 0, 'hull': 0, 'rarepaint': 0, 'epicpaint': 0, 'legendarypaint': 0})
		await db.commit()
		await cursor.close()
		cm.remove(where('command') == id)
		listt.remove(id)
	return
