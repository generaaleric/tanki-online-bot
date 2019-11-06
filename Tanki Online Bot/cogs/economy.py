import discord
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
from data.checks import blacklist_check
from general import ConvertSectoDay
from data.shop_items import hulls, turrets, test

cm = TinyDB('commands.json')
Commands = Query()

promo = []
promouses = []

def get_sec(amount):
    if 'd' in amount:
        ti = int(amount[:-1]) * 86400
        msg = "{} day(s)".format(amount[:-1])
        return ti, msg
    elif 'h' in amount:
        ti = int(amount[:-1]) * 3600
        msg = "{} hour(s)".format(amount[:-1])
        return ti, msg
    elif 'm' in amount:
        ti = int(amount[:-1]) * 60
        msg = "{} minute(s)".format(amount[:-1])
        return ti, msg

def generate_random_string(len_sep, no_of_blocks):
    random_string = ''
    random_str_seq = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(0,len_sep*no_of_blocks):
        if i % len_sep == 0 and i != 0:
            random_string += '-'
        random_string += str(random_str_seq[random.randint(0, len(random_str_seq) - 1)])
    return random_string

def battle_script(att, defe):
    logo = []
    attacker_hp = 100
    defender_hp = 100
    ra = random.randint(1,100)
    if ra < 50:
        while attacker_hp > 0 and defender_hp > 0:
            l1 = random.randint(1,100)
            attacker_hp -= l1
            if l1 >79:
                asd11 = "{} does critical<:critical:492246910103715840>{} damage".format(defe, l1)
                if l1 > 99:
                    asd11 = "{} has made a super kill<:superkill:492248534561718272>{} damage".format(defe, l1)
            else:
                asd11 = "{} does<:normal:492246910120493056>{} damage".format(defe, l1)
            asd1 = ("***{} health: {}***\n".format(att, max(0,attacker_hp)))
            logo.append(asd11)
            logo.append(asd1)
            if attacker_hp <=0:
                break
            l2 = random.randint(1,100)
            defender_hp -= l2
            if l2 > 79:
                asd22 = "{} does critical<:critical:492246910103715840>{} damage".format(att, l2)
                if l2 > 99:
                    asd22 = "{} has made a super kill<:superkill:492248534561718272>{} damage".format(att, l2)
            else:
                asd22 = "{} does<:normal:492246910120493056>{} damage".format(att, l2)
            asd2 = ("***{} health: {}***\n".format(defe, max(0,defender_hp)))
            logo.append(asd22)
            logo.append(asd2)
            if defender_hp <=0:
               break
        if attacker_hp <= 0:
            return False, logo
        elif defender_hp <= 0:
            return True, logo
    else:
        while attacker_hp > 0 and defender_hp > 0:
            l2 = random.randint(1,100)
            defender_hp -= l2
            if l2 > 79:
                asd22 = "{} does critical<:critical:492246910103715840>{} damage".format(att, l2)
                if l2 > 99:
                    asd22 = "{} has made a super kill<:superkill:492248534561718272>{} damage".format(att, l2)
            else:
                asd22 = "{} does<:normal:492246910120493056>{} damage".format(att, l2)
            asd2 = ("***{} health: {}***\n".format(defe, max(0,defender_hp)))
            logo.append(asd22)
            logo.append(asd2)
            if defender_hp <=0:
               break
            l1 = random.randint(1,100)
            attacker_hp -= l1
            if l1 >79:
                asd11 = "{} does critical<:critical:492246910103715840>{} damage".format(defe, l1)
                if l1 > 99:
                    asd11 = "{} has made a super kill<:superkill:492248534561718272>{} damage".format(defe, l1)
            else:
                asd11 = "{} does<:normal:492246910120493056>{} damage".format(defe, l1)
            asd1 = ("***{} health: {}***\n".format(att, max(0,attacker_hp)))
            logo.append(asd11)
            logo.append(asd1)
            if attacker_hp <=0:
                break
        if attacker_hp <= 0:
            return False, logo
        elif defender_hp <= 0:
            return True, logo

class Economy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @checks.blacklist_check()
    async def drop(self, ctx):
        if cm.contains(Commands.command == 'drop'):
            cm.update(increment('usage'), Commands.command == 'drop')
        else:
            cm.insert({'command': "drop", 'usage': 1})
        print("1")
        async with aiosqlite.connect('database.db') as db:
            data = await checks.database_container_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(user.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        golds = data[14]
        if golds < 1:
            embed=discord.Embed(title="{}, you don't have any golds to drop!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE containers SET gold = gold - 1 WHERE id = :id",
                {'id': ctx.message.author.id})
            await db.commit()
            await cursor.close()
        embed=discord.Embed(title="Gold Box will be dropped soon!\n*By {}*".format(ctx.message.author.display_name), color=0x00ffff)
        await self.bot.say(embed=embed)
        await asyncio.sleep(5)
        embed=discord.Embed(title="\u200b", color=0x00ffff)
        embed.set_image(url="http://i.imgur.com/OZHGyIM.png")
        await self.bot.say(embed=embed)
        def check(msg):
            if msg.author.id == "408439037771382794":
                return False
            else:
                return True
        msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, check=check)
        if msg is None:
            embed=discord.Embed(title="Looks like no one wants your gold {}. You can take it back.".format(ctx.message.author.display_name), color=0x00ffff)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE containers SET gold = gold + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            return await self.bot.say(embed=embed)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM containers WHERE id=:id', {'id': msg.author.id})
            dataa = await cursor.fetchone()
            await cursor.close()
        if dataa is None:
            embed=discord.Embed(title="{}, you are not registered! Use `>register`\n{} takes the gold back.".format(msg.author.display_name, ctx.message.author.display_name), color=0x00ffff)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE containers SET gold = gold + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            return await self.bot.say(embed=embed)

        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET coins = coins + 1000 WHERE id = :id",
                {'id': msg.author.id})
            await db.commit()
            await cursor.close()
        embed=discord.Embed(title="{} has taken the gold box!".format(msg.author.display_name), color=0x00ffff)
        embed.set_thumbnail(url="http://i.imgur.com/HlFzEJl.png")
        return await self.bot.say(embed=embed)

    @commands.command(pass_context = True, aliases = ["level", "p", "balance", "bal"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, user: discord.Member = None):
        if cm.contains(Commands.command == 'level'):
            cm.update(increment('usage'), Commands.command == 'level')
        else:
            cm.insert({'command': "level", 'usage': 1})
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM users ORDER BY coins DESC')
            allusers = await cursor.fetchall()
            await cursor.close()
        if user is None:
            counter = 0
            place = []
            for i in allusers:
                counter += 1
                if i[0] == ctx.message.author.id:
                    place.append(counter)
            data = await checks.database_check(self, ctx.message.author.id)
            if data is None:
                embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            lvl = data[3]
            containers = data[8]
            coins = data[7]
            for rank in ranks[lvl]:
                nextRank = ranks[lvl]["next"]
                nextXp = ranks[lvl]["xp_next"]
                image = ranks[lvl]["image"]
                premium_image = ranks[lvl]["premium_image"]
            xp = data[1]
            rank = data[6]
            next = nextXp - xp
            naame = data[2]
            premium = data[5]
            reps = data[16]
            eqturret = data[18]
            eqhull = data[19]
            premleftsec = data[11]
            ctxWins = data[9]
            ctxLosses = data[10]
            totalbatts = ctxWins + ctxLosses
            clancheck = await checks.clan_check(self, ctx.message.author.id)
            redcry = data[15]
            if clancheck is None:
                tagClan = "   ‍   "
            else:
                tagClan = clancheck[4]
                tagClan = f"[{tagClan}]"
            try:
                ratee = ctxWins / totalbatts
                rex = int(ratee *100)
            except:
                rex = 0
            ts = time.time()
            premleftsec = premleftsec - ts
            dff = ConvertSectoDay(int(premleftsec))
            # lol = time.time()
            # ty = premleftsec
            # dff = time.strftime("%A, %d %b %Y  %H:%M:%S GMT", time.gmtime(ty))
            if premium == "Yes":
                embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0xffff00)
                embed.set_thumbnail(url=premium_image)
                embed.add_field(name='{} {}'.format(tagClan, naame), value="**Rank:** {}\n**Crystals:** {:,}\n**Red Crystals:** {:,}\n**Containers:** {:,}\n**Experience:** {:,}\n({:,}xp left)\n**Leaderboard place:** {}".format(lvl, coins, redcry, containers, xp, next, place[0]), inline=False)
                embed.add_field(name="Premium expires in:", value="{}".format(dff), inline=False)
                embed.add_field(name="Equipped Combo", value="**Turret:** {} **Hull:** {}".format(eqturret, eqhull), inline=False)
                embed.add_field(name="Battles", value="**Wins:** {} **Losses:** {} **Win Rate:** {}%".format(ctxWins, ctxLosses, rex), inline=False)
                embed.add_field(name="Reputation Points", value="{:,}".format(reps), inline=True)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0x00ffff)
                embed.set_thumbnail(url=image)
                embed.add_field(name='{} {}'.format(tagClan, naame), value="**Rank:** {}\n**Crystals:** {:,}\n**Red Crystals:** {:,}\n**Containers:** {:,}\n**Experience:** {:,}\n({:,}xp left)\n**Leaderboard place:** {}".format(lvl, coins, redcry, containers, xp, next, place[0]), inline=False)
                embed.add_field(name="Equipped Combo", value="**Turret:** {} **Hull:** {}".format(eqturret, eqhull), inline=False)
                embed.add_field(name="Battles", value="**Wins:** {} **Losses:** {} **Win Rate:** {}%".format(ctxWins, ctxLosses, rex), inline=False)
                embed.add_field(name="Reputation Points", value="{:,}".format(reps), inline=True)
                return await self.bot.say(embed=embed)
        else:
            counter = 0
            place = []
            for i in allusers:
                counter += 1
                if i[0] == user.id:
                    place.append(counter)
            data = await checks.database_check(self, user.id)
            if data is None:
                embed=discord.Embed(title="{}, they are not registered!".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            lvl = data[3]
            containers = data[8]
            coins = data[7]
            for rank in ranks[lvl]:
                nextRank = ranks[lvl]["next"]
                nextXp = ranks[lvl]["xp_next"]
                image = ranks[lvl]["image"]
                premium_image = ranks[lvl]["premium_image"]
            xp = data[1]
            rank = data[6]
            next = nextXp - xp
            premium = data[5]
            uwins = data[9]
            reps = data[16]
            eqturret = data[18]
            eqhull = data[19]
            ulosses = data[10]
            premleftsec = data[11]
            clancheck = await checks.clan_check(self, user.id)
            naame = data[2]
            redcry = data[15]
            if clancheck is None:
                tagClan = "   ‍   "
            else:
                tagClan = clancheck[4]
                tagClan = f"[{tagClan}]"
            try:
                totalbattles = uwins + ulosses
                winratee = uwins / totalbattles
                werr = int(winratee *100)
            except:
                werr = 0
            ts = time.time()
            premleftsec = premleftsec - ts
            dff = ConvertSectoDay(int(premleftsec))
            if premium == "Yes":
                embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0xffff00)
                embed.set_thumbnail(url=premium_image)
                embed.add_field(name='{} {}'.format(tagClan, naame), value="**Rank:** {}\n**Crystals:** {:,}\n**Red Crystals:** {:,}\n**Containers:** {:,}\n**Experience:** {:,}\n({:,}xp left)\n**Leaderboard place:** {}".format(lvl, coins, redcry, containers, xp, next, place[0]), inline=False)
                embed.add_field(name="Premium expires in:", value="{}".format(dff), inline=False)
                embed.add_field(name="Equipped Combo", value="**Turret:** {} **Hull:** {}".format(eqturret, eqhull), inline=False)
                embed.add_field(name="Battles", value="**Wins:** {} **Losses:** {} **Win Rate:** {}%".format(uwins, ulosses, werr), inline=False)
                embed.add_field(name="Reputation Points", value="{:,}".format(reps), inline=True)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0x00ffff)
                embed.set_thumbnail(url=image)
                embed.add_field(name='{} {}'.format(tagClan, naame), value="**Rank:** {}\n**Crystals:** {:,}\n**Red Crystals:** {:,}\n**Containers:** {:,}\n**Experience:** {:,}\n({:,}xp left)\n**Leaderboard place:** {}".format(lvl, coins, redcry, containers, xp, next, place[0]), inline=False)
                embed.add_field(name="Equipped Combo", value="**Turret:** {} **Hull:** {}".format(eqturret, eqhull), inline=False)
                embed.add_field(name="Battles", value="**Wins:** {} **Losses:** {} **Win Rate:** {}%".format(uwins, ulosses, werr), inline=False)
                embed.add_field(name="Reputation Points", value="{:,}".format(reps), inline=True)
                return await self.bot.say(embed=embed)


    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def register(self, ctx):
        if cm.contains(Commands.command == 'register'):
            cm.update(increment('usage'), Commands.command == 'register')
        else:
            cm.insert({'command': "register", 'usage': 1})
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            number = random.randint(1000, 9999)
            embed=discord.Embed(title="Hello {}!\nTo confirm, type: `{}`".format(ctx.message.author.display_name, number), color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, author=ctx.message.author)
            msgs = f"{number}"
            if msg is None:
                embed=discord.Embed(title="{}, you took too long to respond.".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content not in msgs:
                embed=discord.Embed(title="{}, that's an invalid response. Exiting...".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
                await asyncio.sleep(3)
                await self.bot.delete_message(ctx.message)
            else:
                await checks.add_user(self, ctx.message.author.id, ctx.message.author.display_name)
                await checks.add_garage(self, ctx.message.author.id, ctx.message.author.display_name)
                await checks.add_user_containers(self, ctx.message.author.id, ctx.message.author.display_name)
                embed=discord.Embed(title="{}, you have been successfully registered.\nUse `>level` to see your current level.".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title="{}, you are already registered!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)


    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def _battle(self, ctx, user: discord.Member = None):
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
        if dataa is None:
            embed=discord.Embed(title="{}, they are not registered!`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        uwins = dataa[9]
        ulosses = dataa[10]
        text1=discord.Embed(title="{}, {} challenges you for a fight!\n>accept\n>deny".format(user.display_name, ctx.message.author.display_name), color=0x00ffff)
        await self.bot.say(embed=text1)
        msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, author=user)
        if msg is None:
            embed=discord.Embed(title="Seems like {}, is afraid to accept the fight! Next time!".format(user.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        if msg.content == ">accept":
            embed=discord.Embed(title="{}, accepted the fight!".format(user.display_name), color=0x00ffff)
            await self.bot.say(embed=embed)
            await asyncio.sleep(3)
            text2=discord.Embed(title="A fight between {} and {} is about to begin!".format(ctx.message.author.display_name, user.display_name), color=0x00ffff)
            await self.bot.say(embed=text2)
            await asyncio.sleep(3)
        elif msg.content == ">deny":
            embed=discord.Embed(title="{} doesn't want to fight with you {}.".format(user.display_name, ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title="{}, that's an invalid response! Exiting...".format(user.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)

        result, logo = battle_script(ctx.message.author.display_name, user.display_name)
        logo  = "\n".join(logo)
        if result == True:
            embed = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            embed.set_thumbnail(url="https://i.imgur.com/4SKYtfq.png")
            embed.add_field(name="<:battlelog:492254072607342593>Battle log", value=logo, inline = False)
            embed.add_field(name=f":tada: {ctx.message.author.display_name} wins!", value="\u200b", inline=False)
            embed.add_field(name=f"{ctx.message.author.display_name}", value="**Wins:** {} **Losses:** {}".format(ctxWins+1, ctxLosses), inline=True)
            embed.add_field(name=f"{user.display_name}", value="**Wins:** {} **Losses:** {}".format(uwins, ulosses+1), inline=True)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET wins = wins + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET losts = losts + 1 WHERE id = :id",
                    {'id': user.id})
                await db.commit()
                await cursor.close()
            return await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title="Tanki Online", colour=discord.Colour(0x42d9f4), url="http://www.tankionlinebot.com")
            embed.set_thumbnail(url="https://i.imgur.com/4SKYtfq.png")
            embed.add_field(name="<:battlelog:492254072607342593>Battle log", value=logo, inline = False)
            embed.add_field(name=f":tada: {user.display_name} wins!", value="\u200b", inline=False)
            embed.add_field(name=f"{ctx.message.author.display_name}", value="**Wins:** {} **Losses:** {}".format(ctxWins, ctxLosses+1), inline=True)
            embed.add_field(name=f"{user.display_name}", value="**Wins:** {} **Losses:** {}".format(uwins+1, ulosses), inline=True)
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET losts = losts + 1 WHERE id = :id",
                    {'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET wins = wins + 1 WHERE id = :id",
                    {'id': user.id})
                await db.commit()
                await cursor.close()
            return await self.bot.say(embed=embed)



    @commands.command(pass_context = True, aliases=["lb"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def leaderboard(self, ctx):
        if cm.contains(Commands.command == 'leaderboard'):
            cm.update(increment('usage'), Commands.command == 'leaderboard')
        else:
            cm.insert({'command': "leaderboard", 'usage': 1})
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        xp = data[1]
        cry = data[7]
        redcry = data[15]
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM users ORDER BY coins DESC')
            allusers = await cursor.fetchall()
            await cursor.close()
        counter = 0
        place = []
        for i in allusers:
            counter += 1
            if i[0] == ctx.message.author.id:
                place.append(counter)
        counter = 0
        embed = discord.Embed(title="Most Crystals earned!", colour=discord.Colour(0x42d9f4), url="https://discord.gg/qBHXyWd")
        for i in allusers[:10]:
            counter += 1
            embed.add_field(name=f"{counter}. {i[2]}", value=f"Crystals: {i[7]:,}",inline=False)
        embed.set_footer(text=f"Your place is {place[0]:,} with {cry:,} crystals")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def unregister(self, ctx):
        if cm.contains(Commands.command == 'unregister'):
            cm.update(increment('usage'), Commands.command == 'unregister')
        else:
            cm.insert({'command': "unregister", 'usage': 1})
        embed=discord.Embed(title='{}, are you sure you would like to unregister? You will lose all our data!\nReply with Yes or No'.format(ctx.message.author.display_name), color=0x00ffff)
        await self.bot.say(embed=embed)
        msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
        if msg.content.lower() == "yes":
            data = await checks.database_check(self, ctx.message.author.id)
            if data is None:
                embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            await checks.delete_user(self, ctx.message.author.id)
            embed=discord.Embed(title='{}, you have been successfully unregistered. Thanks for being with us! Hope you come back someday.'.format(ctx.message.author.display_name), color=0x00ffff)
            await self.bot.say(embed=embed)
        elif msg.content.lower() == "no":
            embed=discord.Embed(title='{}, exiting menu'.format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title='{}, invalid response.'.format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    @checks.blacklist_check()
    async def reset(self, ctx):
        if cm.contains(Commands.command == 'reset'):
            cm.update(increment('usage'), Commands.command == 'reset')
        else:
            cm.insert({'command': "reset", 'usage': 1})
        number = random.randint(1000, 9999)
        embed=discord.Embed(title="{}, are you sure you wanna start from zero? You will lose all your xp and you will be set back to Recruit rank.\nTo comfirm, type: `{}`".format(ctx.message.author.display_name, number), color=0x00ffff)
        await self.bot.say(embed=embed)
        msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, author=ctx.message.author)
        msgs = "{}".format(number)
        if msg is None:
            embed=discord.Embed(title="{}, you took too long to respond.".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        elif msg.content not in msgs:
            embed=discord.Embed(title="{}, that's an invalid response. Exiting...".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
            await asyncio.sleep(3)
        else:
            data = await checks.database_check(self, ctx.message.author.id)
            if data is None:
                embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            await checks.delete_user(self, ctx.message.author.id)
            await checks.add_user(self, ctx.message.author.id, ctx.message.author.display_name)
            await checks.add_user_containers(self, ctx.message.author.id, ctx.message.author.display_name)
            embed=discord.Embed(title="{}, you have been successfully reseted.".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)

    @commands.command(pass_context = True, aliases=['promo','activate'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def promocode(self, ctx, promocode = None):
        data = await checks.database_container_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(user.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        if promocode is None:
            return await self.bot.say("Please enter a promocode")
        if promouses:
            await self.bot.say("The promocode you have entered is either incorrect or expired!")
        else:
            if promocode in promo:
                promo.clear()
                await self.bot.say("{} You received 5 containers from the promocode!".format(ctx.message.author.display_name))
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET containers = containers + 5 WHERE id = :id",
                        {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
            else:
                await self.bot.say("The promocode you have entered is either incorrect or expired!")

    @commands.command(pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.owner_only()
    async def generatepromo(self, ctx):
        randompromo = (generate_random_string(4,4))
        promo.append(randompromo)
        await self.bot.say("New promocode has been generated!")
        await self.bot.send_message(ctx.message.author, randompromo)



    # @commands.command(pass_context = True)
    # async def lol(self, ctx):
    #     url = "https://discordbots.org/api/bots/408439037771382794/check?userId={}".format(ctx.message.author.id)
    #     async with aiohttp.ClientSession() as session:
    #         headers = {"Authorization": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE'}
    #         async with session.get(url, headers=headers) as resp:
    #             asd = await resp.json()
    #             vote = asd['voted']
    #         if vote == 1:
    #             await self.bot.say("Sup dude!")
    #         else:
    #             await self.bot.say("You need to vote in oder to use this command!")

    @commands.command(pass_context = True)
    async def voted(self, ctx):
        if cm.contains(Commands.command == 'voted'):
            cm.update(increment('usage'), Commands.command == 'voted')
        else:
            cm.insert({'command': "voted", 'usage': 1})
        headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE"}
        async def fetch(session, url):
            async with session.get(url, headers=headers) as response:
                return await response.text()
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://discordbots.org/api/bots/408439037771382794/check?userId={}'.format(ctx.message.author.id))
            vote = html[9]
            if vote == '1':
                await self.bot.say('You have voted.')
            else:
                await self.bot.say("You haven't voted. Use `>vote` command to get a link to the vote website. If you already voted but you still cant use it then try again in 1 minute")

    @commands.command(pass_context = True, aliases=["reward"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def rewards(self, ctx):
        if cm.contains(Commands.command == 'rewards'):
            cm.update(increment('usage'), Commands.command == 'rewards')
        else:
            cm.insert({'command': "rewards", 'usage': 1})
        headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE"}
        async def fetch(session, url):
            async with session.get(url, headers=headers) as response:
                return await response.text()
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://discordbots.org/api/bots/408439037771382794/check?userId={}'.format(ctx.message.author.id))
            vote = html[9]
            print(vote)
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            return await self.bot.say("You are not registered.\nUse `>register`")
        voted = data[13]
        if voted == "Claimed":
            return await self.bot.say("You already claimed your rewards!")
        else:
            pass
        print
        if vote == "1":
            print("I voted")
            ts = time.time()
            premium = data[5]
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET voted = :voted WHERE id = :id",
                    {'voted': "Claimed", 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            if premium == "Yes":
                premleft = data[11]
                async with aiosqlite.connect('database.db') as db:
                    totaltime, msg = get_sec("3h")
                    totaltimee = premleft + totaltime
                    cursor = await db.execute("UPDATE users SET premleft = :premleft WHERE id = :id",
                        {'premleft': totaltimee, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
                        {'containers': 30, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                        {'coins': 100000, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                        {'redcrystals': 100, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title="{}, You have received the following items:".format(ctx.message.author.display_name), description="• 3 hours of premium account\n• 30 containers\n • 100,000 Crystals\n • 100 Red Crystals", color=0xffff00)
                return await self.bot.say(embed=embed)
            else:
                premleft = data[11]
                async with aiosqlite.connect('database.db') as db:
                    totaltime, msg = get_sec("1h")
                    print(ConvertSectoDay(totaltime))
                    totaltimee = totaltime + ts
                    print(ConvertSectoDay(totaltimee))
                    cursor = await db.execute("UPDATE users SET premleft = :premleft WHERE id = :id",
                        {'premleft': totaltimee, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
                        {'containers': 15, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                        {'coins': 50000, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET premium = :premium WHERE id = :id",
                        {'premium': "Yes", 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                        {'redcrystals': 50, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title="{}, You have received the following items:".format(ctx.message.author.display_name), description="• 1 hour of premium account\n• 15 containers\n • 50,000 Crystals\n • 50 Red Crystals", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            await self.bot.say("You haven't voted. Use `>vote` command to get a link to the vote website. If you already voted but you still cant use it then try again in 1 minute")


    async def on_message(self, message):
        if message.author.bot:
            return
        server = message.server
        # if message.content.lower().startswith("blload"):
        #     print(f'"{message.author.display_name}": {message.content} commmand in "{message.server.name}" server.\n--------------------------------------------------------------')
        if message.content.upper().startswith(">"):
            if server is None:
                print(f'"{message.author}" used {message.content} commmand in DM.\n--------------------------------------------------------------')
            else:
                # await self.bot.send_message(message.channel, "Unexpected downtime in 1 minute. Bug fix requires bot restart.")
                print(f'"{message.author}" used {message.content} commmand in "{message.server.name}" server.\n--------------------------------------------------------------')
        id = message.author.id
        data = await checks.database_check(self, message.author.id)
        if data is None:
            return
        ts = time.time()
        premleft = data[11]

        # else:
        xp = data[1]
        premium = data[5]
        #     if premium =="Yes":
        #         amt = 2
        #     else:
        #         amt = 1
        #     async with aiosqlite.connect('database.db') as db:
        #         cursor = await db.execute("UPDATE users SET xp = xp + :amt WHERE id = :id",
        #             {'amt': amt, 'id': message.author.id})
        #         await db.commit()
        #         await cursor.close()
        player = data[0]
        currentRank = data[3]

        if player == message.author.id:
            for rank in ranks[currentRank]:
                nextRank = ranks[currentRank]["next"]
                rankid = ranks[currentRank]["id"]
                nextImage = ranks[nextRank]["image"]
                premium_image = ranks[nextRank]["premium_image"]
                rankcoins = ranks[nextRank]["coins"]
                premiumcoins = ranks[nextRank]["coins"] * 2

            if xp >= ranks[nextRank]["xp"]:
                unlockeditems = []
                for x in hulls.values():
                    asd = x["id"]
                    if rankid+1 == asd:
                        print(asd)
                        print(rankid)
                        item = x["name"]
                        unlockeditems.append(item)
                    else:
                        pass
                for x in turrets.values():
                    asd = x["id"]
                    if rankid+1 == asd:
                        print(asd)
                        print(rankid)
                        item = x["name"]
                        unlockeditems.append(item)
                    else:
                        pass
                rankTitle = "Tanki Online"
                rankText = ":sparkles: Rank up! :sparkles:"
                if premium == "Yes":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET level = :level WHERE id = :id",
                            {'level': nextRank, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET emoji = :emoji WHERE id = :id",
                            {'emoji': nextRank, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET rank = :rank WHERE id = :id",
                            {'rank': premium_image, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title=rankTitle, url="http://www.tankionlinebot.com", color=0x00ffff)
                    embed.set_thumbnail(url=premium_image)
                    embed.add_field(name=rankText, value="Congratulations **{}**! Your rank is now **{}**\n+{:,}:gem:".format(message.author.display_name, nextRank, rankcoins))
                    try:
                        embed.add_field(name="Unlocked items:", value=", ".join(unlockeditems), inline = False)
                    except:
                        print("No items unlocked!")
                    await self.bot.send_message(message.channel, embed=embed)
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': premiumcoins, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    return
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET level = :level WHERE id = :id",
                            {'level': nextRank, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET rank = :rank WHERE id = :id",
                            {'rank': nextImage, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title=rankTitle, url="http://www.tankionlinebot.com", color=0x00ffff)
                    embed.set_thumbnail(url=nextImage)
                    embed.add_field(name=rankText, value="Congratulations **{}**! Your rank is now **{}**\n+{:,}:gem:".format(message.author.display_name, nextRank, rankcoins))
                    try:
                        embed.add_field(name="Unlocked items:", value=", ".join(unlockeditems), inline = False)
                    except:
                        print("No items unlocked!")
                    await self.bot.send_message(message.channel, embed=embed)
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': rankcoins, 'id': message.author.id})
                        await db.commit()
                        await cursor.close()
                    return
        if premleft <= ts:
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET premium = 'No' WHERE id = :id", {'id': message.author.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET rank = :rank WHERE id = :id", {'rank': nextImage, 'id': message.author.id})
                await db.commit()
                await cursor.close()
        # url = "https://discordbots.org/api/bots/408439037771382794/check?userId={}".format(message.author.id)
        headers = {"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE"}
        async def fetch(session, url):
            async with session.get(url, headers=headers) as response:
                return await response.text()

        async with aiohttp.ClientSession() as session:
            html = await fetch(session, 'https://discordbots.org/api/bots/408439037771382794/check?userId={}'.format(message.author.id))
            #print(html[9])
            voted = html[9]
        # async with aiohttp.ClientSession() as session:
        #     headers = {"Authorization": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE'}
        #     async with session.get(url, headers=headers) as resp:
        #         asd = await resp.json()
        #         vote = asd['voted']
        if voted == '0':
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET voted = :voted WHERE id = :id", {'voted': False, 'id': message.author.id})
                await db.commit()
                await cursor.close()
                # elif vote == 1:

        if message.content.upper().startswith(">C INV"):
            await self.bot.send_message(message.channel, ":x: **| This command has been renamed to `>inventory` in the latest update!** Please use `>updates` to see the changelog.")
        if message.content.upper().startswith(">C OPEN"):
            await self.bot.send_message(message.channel, ":x: **| This command has been renamed to `>open` in the latest update!** Please use `>updates` to see the changelog.")
        if message.content.upper().startswith(">C SELL"):
            await self.bot.send_message(message.channel, ":x: **| This command has been renamed to `>sell` in the latest update!** Please use `>updates` to see the changelog.")
        if message.content.upper().startswith(">C BUY"):
            await self.bot.send_message(message.channel, ":x: **| This command has been renamed to `>shop` in the latest update!** Please use `>updates` to see the changelog.")
        if message.content.upper().startswith(">C TOP"):
            await self.bot.send_message(message.channel, ":x: **| This command has been removed in the latest update!** There were too many unnecessary leaderboards so I decided to keep just one. `>leaderboard`")
def setup(bot):
    bot.add_cog(Economy(bot))
