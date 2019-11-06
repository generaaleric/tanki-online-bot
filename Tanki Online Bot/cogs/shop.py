import discord
import re
import datetime
import time
import random
import asyncio
import aiosqlite
import aiohttp
import numpy
from discord.ext import commands
from data.ranks import ranks
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete,increment
import data.checks as checks
from data.ranks import ranks
from data.checks import blacklist_check
from general import ConvertSectoDay
from data.shop_items import hulls, turrets, test
import sqlite3

cm = TinyDB('commands.json')
Commands = Query()


class Shop:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.owner_only()
    async def add_row(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(f"ALTER TABLE users ADD turret TEXT DEFAULT 'Firebird m0' NOT NULL")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(f"ALTER TABLE users ADD hull TEXT DEFAULT 'Wasp m0' NOT NULL")
            await db.commit()
        await cursor.close()
        print("Done!")


    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.owner_only()
    async def qwee(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET wins = 0")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET losts = 0")
            await db.commit()
        await cursor.close()
        print("Done!")

    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.owner_only()
    async def create_table(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("CREATE TABLE garage AS SELECT id, name FROM users")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD wasp INT DEFAULT 0 NOT NULL")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD firebird INT DEFAULT 0 NOT NULL")
            await db.commit()

        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD hornet INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD hunter INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD viking INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD dictator INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD titan INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD mammoth INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD freeze INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD isida INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD hammer INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD twins INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD ricochet INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD smoky INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD striker INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD vulcan INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD thunder INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD railgun INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD magnum INT")
            await db.commit()
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("ALTER TABLE garage ADD shaft INT")
            await db.commit()
        await cursor.close()
        print("Done!")



    @commands.command(pass_context = True, aliases=["eq"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def equip(self, ctx, *, item = None):
        if cm.contains(Commands.command == 'equip'):
            cm.update(increment('usage'), Commands.command == 'equip')
        else:
            cm.insert({'command': "equip", 'usage': 1})
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM garage WHERE id = :id', {'id': ctx.message.author.id})
        data = cur.fetchone()
        items = data.keys()
        lel = list(hulls) + list(turrets)
        itemName = (item.split(' ')[0].lower())
        asd = test[itemName]
        mod = items[asd[itemName]]
        itemmm = data[mod]
        if item.lower() not in lel:
            return await self.bot.say("This item doesn't exist or you didn't specify a modification (M0, M1, M2, M3).")
        elif item.lower() in hulls.keys():
            iteminfo = hulls[item.lower()]
            key = "hull"
        elif item.lower() in turrets.keys():
            iteminfo = turrets[item.lower()]
            key = "turret"
        name = iteminfo["name"]
        # print(item[-1:])
        # print(itemmm)
        if itemmm != int(item[-1:]):
            asd = f"{mod} m{item[-1]}"
            return await self.bot.say(f"You dont have {asd.title()}")
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(f"UPDATE users SET {key} = :item WHERE id = :id", {'id': ctx.message.author.id, 'item': name})
            await db.commit()
            await cursor.close()
        await self.bot.say(f"Equipped {name}")

    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def buy(self, ctx, *, item = None):
        if cm.contains(Commands.command == 'buy'):
            cm.update(increment('usage'), Commands.command == 'buy')
        else:
            cm.insert({'command': "buy", 'usage': 1})
        if item == None:
            await self.bot.say("Please use `>help shop` for more information!")
        con = sqlite3.connect("database.db")
        print("1")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM garage WHERE id = :id', {'id': ctx.message.author.id})
        data = cur.fetchone()
        userdata = await checks.database_check(self, ctx.message.author.id)
        equipedTurret = userdata[18]
        equipedHull = userdata[19]
        print("2")
        userRank = userdata[3]
        coins = userdata[7]
        userRankID = ranks[userRank]["id"]
        print("3")
        lel = list(hulls) + list(turrets)
        print("4")
        print(data)
        items = data.keys()
        print("5")
        try:
            itemName = (item.split(' ')[0].lower())
            asd = test[itemName]
            mod = items[asd[itemName]]
            itemmm = data[mod]
            if itemmm is None:
                itemmm = -1
            itemm = f"{mod} M{itemmm}"
        except:
            pass
        if item.lower() in hulls.keys():
            iteminfo = hulls[item.lower()]
            name = iteminfo["name"]
            price = iteminfo["price"]
            rank = iteminfo["rank"]
            image = iteminfo["image"]
            armor = iteminfo["armor"]
            rankID = iteminfo["id"]
            rankName = iteminfo["rank"]
            em = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            em.set_thumbnail(url=image)
            em.add_field(name=name, value=f"Are you sure you want to buy {name}?\n**Type:** Yes or No", inline = False)
            em.add_field(name="Stats", value=f"**Price:** {price:,} crystals\n**Required rank:** {rank.split(' ')[0]}\n**Armor:** {armor:,}hp", inline = False)
        elif item.lower() in turrets.keys():
            iteminfo = turrets[item.lower()]
            name = iteminfo["name"]
            price = iteminfo["price"]
            rank = iteminfo["rank"]
            image = iteminfo["image"]
            max_damage = iteminfo["max_damage"]
            min_damage = iteminfo["min_damage"]
            rankID = iteminfo["id"]
            rankName = iteminfo["rank"]
            em = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            em.set_thumbnail(url=image)
            em.add_field(name=name, value=f"Are you sure you want to buy {name}?\n**Type:** Yes or No", inline = False)
            em.add_field(name="Stats", value=f"**Price:** {price:,} crystals\n**Required rank:** {rank.split(' ')[0]}\n**Maximum damage:** {max_damage:,}\n**Minimum damage:** {min_damage:,}", inline = False)
        elif item.lower() not in lel: # buy container
            try:
                amount = int(re.sub("[^0-9]", "", item))
            except:
                amount = False
            if amount == False:
                return await self.bot.say("This item doesn't exist or you didn't specify a modification (M0, M1, M2, M3).")# <== sepcfy mod
            cost = amount * 10000
            data = await checks.database_container_check(self, ctx.message.author.id)
            if data is None:
                embed=discord.Embed(title="You are not registered!\nUse `>register`", color=0x00ffff)
                return await self.bot.say(embed=embed)
            if amount > 1000:
                embed=discord.Embed(title=f"{ctx.message.author.display_name}, you can buy up to 1,000 containers.", color=0x00ffff)
                return await self.bot.say(embed=embed)
            embed=discord.Embed(title=f"{ctx.message.author.display_name} are you sure that you would like to buy {amount:,} containers for {cost:,} crystals?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                if coins < cost:
                    embed=discord.Embed(title=f"{ctx.message.author.display_name}, you do not have enough crystals for this purchase! You need {cost - coins:,} more crystals", color=0x00ffff)
                    return await self.bot.say(embed=embed)
                pass
            elif msg.content.lower() == "no":
                embed=discord.Embed(title="Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Invalid response. Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id", {'containers': amount, 'id': ctx.message.author.id})
                await db.commit()
                cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id", {'coins': cost, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, you have successfully bought {amount:,} containers for {cost:,} crystals!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        if item.lower() not in lel:
            return await self.bot.say("This item doesn't exist or you didn't specify a modification (M0, M1, M2, M3).")# <== sepcfy mod
        if int(itemmm) > int(item[-1:]):
            return await self.bot.say(f"You already have a higher modification of {name[:-2].lower()}.")
        elif int(item[-1:]) == itemmm:
            return await self.bot.say(f"You already have {name[:-1]}{itemmm}.")
        elif int(item[-1:]) != int(itemmm) + 1:
            return await self.bot.say(f"You need to buy {name[:-1]}{itemmm+1} first.")
        await self.bot.say(embed=em)
        msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
        if msg is None:
            return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
        elif msg.content.lower() == "yes":
            if userRankID < rankID:
                return await self.bot.say(f"{ctx.message.author.display_name} you do not have the required rank to make this purchase!\nRequired rank: {rankName}")
            if coins < price:
                embed=discord.Embed(title=f"{ctx.message.author.display_name}, you do not have enough crystals for this purchase! You need {price - coins:,} more crystals", color=0x00ffff)
                return await self.bot.say(embed=embed)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id", {'coins': price, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            pass
        elif msg.content.lower() == "no":
            embed=discord.Embed(title="Exiting...", color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title="Invalid response. Exiting...", color=0x00ffff)
            return await self.bot.say(embed=embed)

        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute(f"UPDATE garage SET {item[:-3].lower()} = {item[-1:]} WHERE id = {ctx.message.author.id}")
            await db.commit()
            await cursor.close()

        embed = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
        embed.set_thumbnail(url=image)
        embed.add_field(name="Purchased", value=f"You bought {name}", inline = False)
        if itemName == equipedTurret.split(' ')[0].lower():
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute(f"UPDATE users SET turret = :item WHERE id = :id", {'id': ctx.message.author.id, 'item': name})
                await db.commit()
                await cursor.close()
        elif itemName == equipedHull.split(' ')[0].lower():
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute(f"UPDATE users SET hull = :item WHERE id = :id", {'id': ctx.message.author.id, 'item': name})
                await db.commit()
                await cursor.close()
        return await self.bot.say(embed=embed)



    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def garage(self, ctx):
        if cm.contains(Commands.command == 'garage'):
            cm.update(increment('usage'), Commands.command == 'garage')
        else:
            cm.insert({'command': "garage", 'usage': 1})
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM garage WHERE id = :id', {'id': ctx.message.author.id})
        data = cur.fetchone()
        turrets = ["firebird", "freeze", "isida", "hammer", "twins", "ricochet", "smoky", "striker", "vulcan", "thunder", "railgun", "magnum", "shaft"]
        hulls = ["wasp", "hornet", "hunter", "viking", "dictator", "titan", "mammoth"]
        userdata = await checks.database_check(self, ctx.message.author.id) # <======= ADD CHECK IF USER exists
        equipedTurret = userdata[18]
        equipedHull = userdata[19]

        items = []
        for i in data.keys():
            items.append(i)
        items = items[2:]
        tur = []
        hul = []
        for item in items:
            print(item)
            asd = f"{item} m{data[item]}"
            if asd[:-3] in hulls:
                if data[item] is not None:
                    hul.append(asd.title())
                else:
                    pass
            else:
                if data[item] is not None:
                    tur.append(asd.title())
                else:
                    pass
        tur = sorted(tur, key=lambda x: int(x[-1]))
        tur = tur[::-1]
        hul = sorted(hul, key=lambda x: int(x[-1]))
        hul = hul[::-1]
        print(hul)
        naame = userdata[2]
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            tagClan = "   ‍   "
        else:
            tagClan = clancheck[4]
            tagClan = f"[{tagClan}]"
        embed=discord.Embed(title=f"{tagClan} {naame}'s Garage", description="Currently equipped", color=0x00ffff)
        embed.set_author(name="Tanki Online")
        embed.add_field(name="Turret", value=f"{equipedTurret}", inline=True)
        embed.add_field(name="Hull", value=f"{equipedHull}", inline=True)
        hulls = ' **|** '.join(hul)
        turrets = ' **|** '.join(tur)
        embed.add_field(name="Storage", value=f"**Turrets:** {turrets}\n**Hulls:** {hulls}", inline=False)
        await self.bot.say(embed=embed)


    @commands.command(pass_context = True, aliases=["bt"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def battle(self, ctx, user: discord.Member = None):
        if cm.contains(Commands.command == 'battle'):
            cm.update(increment('usage'), Commands.command == 'battle')
        else:
            cm.insert({'command': "battle", 'usage': 1})
        if user is None:
            embed=discord.Embed(title="{}, Please mention someone to battle with!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        elif user is ctx.message.author:
            embed=discord.Embed(title="{}, you can't battle with yourself!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        ctxWins = data[9]
        ctxLosses = data[10]
        dataa = await checks.database_check(self, user.id)
        nicka = data[2]
        if dataa is None:
            embed=discord.Embed(title="{}, they are not registered!`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        nickd = dataa[2]
        uwins = dataa[9]
        ulosses = dataa[10]
        text1=discord.Embed(title="{}, {} wants to battle with you!\n>accept\n>deny".format(nickd, nicka), color=0x00ffff)
        await self.bot.say(embed=text1)
        msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, author=user)
        if msg is None:
            embed=discord.Embed(title="Seems like {}, is afraid to accept the battle! Next time!".format(nickd), color=0x00ffff)
            return await self.bot.say(embed=embed)
        if msg.content == ">accept":
            embed=discord.Embed(title="{}, accepted the battle!".format(nickd), color=0x00ffff)
            await self.bot.say(embed=embed)
            await asyncio.sleep(3)
            text2=discord.Embed(title="A battle between {} and {} is about to begin!".format(nicka, nickd), color=0x00ffff)
            await self.bot.say(embed=text2)
            await asyncio.sleep(3)
        elif msg.content == ">deny":
            embed=discord.Embed(title="{} doesn't want to battle with you {}.".format(nickd, nicka), color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title="{}, that's an invalid response! Exiting...".format(nickd), color=0x00ffff)
            return await self.bot.say(embed=embed)
        Turret = data[18]
        Hull = data[19]
        userTurret = dataa[18]
        userHull = dataa[19]

        iteminfo = turrets[Turret.lower()]
        damage_MIN = iteminfo["min_damage"]
        damage_MAX = iteminfo["max_damage"]
        iteminfo = hulls[Hull.lower()]
        armor = iteminfo["armor"]

        attacker_hp = armor
        attacker_dmg = random.randint(damage_MIN, damage_MAX)

        iteminfo = turrets[userTurret.lower()]
        damage_MIN = iteminfo["min_damage"]
        damage_MAX = iteminfo["max_damage"]
        iteminfo = hulls[userHull.lower()]
        armor = iteminfo["armor"]

        defender_hp = armor
        defender_dmg = random.randint(damage_MIN, damage_MAX)
        arounds = 0
        drounds = 0
        logs = []
        while attacker_hp > 0 and defender_hp > 0:
            miss = random.randint(1, 10)
            if miss == 7:
                logs.append("Missed")
                pass
            else:
                defender_hp -= attacker_dmg
            arounds += 1
            logs.append(f"{nicka}, does {attacker_dmg} damage \n{nickd} {defender_hp} hp")
            if defender_hp <= 0:
               break

            miss = random.randint(1, 10)
            if miss == 7:
                logs.append("Missed")
                pass
            else:
                attacker_hp -= defender_dmg
            drounds += 1
            logs.append(f"{nickd}, does {defender_dmg} damage \n{nicka} {attacker_hp} hp")
            if attacker_hp <=0:
                break
        if attacker_hp <= 0:
            embed = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name=f":tada: {nickd} wins in {drounds} rounds!", value="\u200b", inline=False)
            embed.add_field(name=f"{nicka}", value="**Wins:** {} **Losses:** {}".format(ctxWins, ctxLosses+1), inline=True)
            embed.add_field(name=f"{nickd}", value="**Wins:** {} **Losses:** {}".format(uwins+1, ulosses), inline=True)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET wins = wins + 1 WHERE id = :id",
                    {'id': user.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET losts = losts + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            await self.bot.say(embed=embed)
            #await self.bot.say(f"{ctx.message.author.display_name}, you lost!\n{user.display_name}, wins in {drounds} rounds!")
            #await self.bot.say("\n".join(logs))
        elif defender_hp <= 0:
            embed = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.add_field(name=f":tada: {nicka} wins in {arounds} rounds!", value="\u200b", inline=False)
            embed.add_field(name=f"{nicka}", value="**Wins:** {} **Losses:** {}".format(ctxWins+1, ctxLosses), inline=True)
            embed.add_field(name=f"{nickd}", value="**Wins:** {} **Losses:** {}".format(uwins, ulosses+1), inline=True)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET losts = losts + 1 WHERE id = :id",
                    {'id': user.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET wins = wins + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            await self.bot.say(embed=embed)
            #await self.bot.say(f"{user.display_name}, you lost!\n{ctx.message.author.display_name}, wins! in {arounds} rounds!")
            #await self.bot.say("\n".join(logs))


    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stats(self, ctx, *, arg = None):
        if cm.contains(Commands.command == 'stats'):
            cm.update(increment('usage'), Commands.command == 'stats')
        else:
            cm.insert({'command': "stats", 'usage': 1})
        turs = list(turrets)
        huls = list(hulls)
        iteem = arg.lower()
        if arg is None:
            await self.bot.say("Please enter an item.\nUsage: `>stats Wasp m2`")
        elif iteem in huls:
            iteminfo = hulls[arg.lower()]
            name = iteminfo["name"]
            price = iteminfo["price"]
            rank = iteminfo["rank"]
            image = iteminfo["image"]
            armor = iteminfo["armor"]
            em = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            em.set_thumbnail(url=image)
            em.add_field(name="Stats", value=f"**Price:** {price:,} crystals\n**Required rank:** {rank.split(' ')[0]}\n**Armor:** {armor:,}hp", inline = False)
            await self.bot.say(embed=em)
        elif iteem in turs:
            iteminfo = turrets[arg.lower()]
            name = iteminfo["name"]
            price = iteminfo["price"]
            rank = iteminfo["rank"]
            image = iteminfo["image"]
            max_damage = iteminfo["max_damage"]
            min_damage = iteminfo["min_damage"]
            em = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            em.set_thumbnail(url=image)
            em.add_field(name="Stats", value=f"**Price:** {price:,} crystals\n**Required rank:** {rank.split(' ')[0]}\n**Maximum damage:** {max_damage:,}\n**Minimum damage:** {min_damage:,}", inline = False)
            await self.bot.say(embed=em)



    @commands.group(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, ctx):
        if cm.contains(Commands.command == 'shop'):
            cm.update(increment('usage'), Commands.command == 'shop')
        else:
            cm.insert({'command': "shop", 'usage': 1})
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Welcome to Tanki Online shop!", description="What would you like to buy?", color=0x00ffff)
            embed.set_author(name="Tanki Online")
            embed.add_field(name="Categories:", value="`>shop turrets`\n`>shop hulls`\n`>shop containers`", inline=True)
            embed.set_footer(text="For more information about shop use >help shop")
            await self.bot.say(embed=embed)


    @shop.command(pass_context=True, name="containers", aliases=["c", "container"])
    async def _container(self, ctx):
        embed=discord.Embed(title="Welcome to Tanki Online container shop category!", description="How many containers would you like to buy?", color=0x00ffff)
        embed.set_author(name="Tanki Online")
        embed.add_field(name="1 container", value="10,000 crystals", inline=True)
        embed.add_field(name="5 container", value="50,000 crystals", inline=True)
        embed.add_field(name="15 container", value="150,000 crystals", inline=True)
        embed.add_field(name="30 container", value="300,000 crystals", inline=True)
        embed.add_field(name="50 container", value="500,000 crystals", inline=True)
        embed.add_field(name="100 container", value="1,000,000 crystals", inline=True)
        embed.add_field(name="Custom amount?", value=">buy <amount>", inline=True)
        embed.set_footer(text="For more information about shop use >help shop")
        await self.bot.say(embed=embed)




    @shop.command(pass_context=True, name="turrets")
    async def _turrets(self, ctx, number = None):
        embed=discord.Embed(title="Welcome to Tanki Online turret shop category!", description="What turret would you like to buy?", color=0x00ffff)
        embed.set_author(name="Tanki Online")
        asd = [None, "1"]
        if number in asd:
            turret_info = turrets["firebird m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["firebird m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["firebird m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["freeze m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["freeze m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["freeze m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["freeze m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["isida m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["isida m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["isida m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["isida m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["hammer m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)
            embed.set_footer(text="Next page | >shop turrets 2")

        elif number == "2":
            turret_info = turrets["hammer m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["hammer m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["hammer m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["twins m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["twins m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["twins m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["twins m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["ricochet m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["ricochet m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["ricochet m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["ricochet m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["smoky m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["smoky m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["smoky m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["smoky m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)
            embed.set_footer(text="Next page | >shop turrets 3")

        elif number == "3":
            turret_info = turrets["striker m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["striker m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["striker m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["striker m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["vulcan m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["vulcan m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["vulcan m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["vulcan m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["thunder m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["thunder m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["thunder m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["thunder m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)
            embed.set_footer(text="Next page | >shop turrets 4")

        elif number == "4":
            turret_info = turrets["railgun m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["railgun m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["railgun m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["railgun m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["magnum m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["magnum m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["magnum m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["magnum m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["shaft m0"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["shaft m1"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["shaft m2"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            turret_info = turrets["shaft m3"]
            name = turret_info["name"]
            price = turret_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)
            embed.set_footer(text="Last Page")
        else:
            return await self.bot.say("There's no such page!")

        await self.bot.say(embed=embed)

    @shop.command(pass_context=True, name="hulls")
    async def _hulls(self, ctx, number = None):
        embed=discord.Embed(title="Welcome to Tanki Online hull shop category!", description="What hull would you like to buy?", color=0x00ffff)
        embed.set_author(name="Tanki Online")
        asd = [None, "1"]
        if number in asd:
            hull_info = hulls["wasp m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["wasp m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["wasp m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hornet m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hornet m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hornet m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hornet m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hunter m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hunter m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hunter m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["hunter m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["viking m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            embed.set_footer(text="Next page | >shop hulls 2")
        elif number == "2":
            hull_info = hulls["viking m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["viking m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["viking m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["dictator m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["dictator m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["dictator m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["dictator m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["titan m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["titan m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["titan m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["titan m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["mammoth m0"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            embed.set_footer(text="Next page | >shop hulls 3")

        elif number == "3":
            hull_info = hulls["mammoth m1"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["mammoth m2"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            hull_info = hulls["mammoth m3"]
            name = hull_info["name"]
            price = hull_info["price"]
            embed.add_field(name=name, value=f"{price:,} crystals", inline=True)

            embed.set_footer(text="Last page")
        else:
            return await self.bot.say("There's no such page!")

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Shop(bot))
