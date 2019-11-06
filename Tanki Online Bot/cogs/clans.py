import discord
import string
import time
import json
import asyncio
import random
import aiosqlite
from discord.ext import commands
import data.checks as checks
from data.checks import blacklist_check
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete,increment
from general import ConvertSectoDay

cm = TinyDB('commands.json')
Commands = Query()


ts = time.time()

class Clans:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @checks.blacklist_check()
    async def clan(self, ctx):
        try:
            if cm.contains(Commands.command == 'clan'):
                cm.update(increment('usage'), Commands.command == 'clan')
            else:
                cm.insert({'command': "clan", 'usage': 1})
        except:
            await self.bot.say(":x: An error occurred while executing the command.")
        if ctx.invoked_subcommand is None:
            await self.bot.say("**Use:** `>help clan`")

    @clan.command(pass_context=True, aliases="lb")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def leaderboard(self, ctx):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT clans.tag, clans.name, users.name,  sum(users.coins) FROM clans INNER JOIN users ON clans.memberid = users.id GROUP BY clans.clanid ORDER BY sum(users.coins) DESC')
            clans = await cursor.fetchall()
            await cursor.close()
        print(clans)
        counter = 0
        embed = discord.Embed(title="Clan Leaderboard", colour=discord.Colour(0x42d9f4), url="https://discord.gg/qBHXyWd")
        for i in clans[:10]:
            counter += 1
            embed.add_field(name=f"{counter}. [{i[:10][0]}] {i[:10][1]}", value=f"Crystals: {i[:10][3]:,}",inline=False)
        await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="create")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _create(self, ctx):
        print("1")
        chat_filter = ["pornhub", "fuck", "discord.gg", "fack", "gay", "cancer", "bastard", "porn", "fcuk", "suck me", "suck my", "sack my", "sack me", "suckme", "sackme", "fvck", "sex", "blowjob", "dick", "pussy", "pusy", "bitch", "cunt", "nigga", "fuk", "jizz", "xnxx", "xxx", "chaturbate"]
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is not None:
            embed=discord.Embed(title="{}, you arleady have a clan.".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        dataa = await checks.database_check(self, ctx.message.author.id)
        if dataa is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        license = dataa[14]
        owner = dataa[2]
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM clans')
            test = await cursor.fetchall()
            await cursor.close()
        clanTags = []
        clanNames = []
        for x in test:
            clanTags.append(x[4])
            clanNames.append(x[3])
        if license:
            clanid = ''.join([random.choice(string.digits) for n in range(6)])
            await self.bot.say("Choose your clan name.")
            nameClan = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if nameClan.content in clanNames:
                embed=discord.Embed(title="{} that clan name is taken!\nExiting...".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if any(badword in nameClan.content for badword in chat_filter):
                embed=discord.Embed(title="{}, insults are not allowed!".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if len(nameClan.content) > 20:
                return await self.bot.say("Your clan name must be less than 20 characters!")
            elif len(nameClan.content) < 4:
                return await self.bot.say("Your clan name must be more than 4 characters!")
            await self.bot.say("Choose your clan tag.")
            tagClan = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if tagClan.content in clanTags:
                embed=discord.Embed(title="{} that clan tag is taken!\nExiting...".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if any(badword in tagClan.content for badword in chat_filter):
                embed=discord.Embed(title="{}, insults are not allowed!".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if len(tagClan.content) > 5:
                return await self.bot.say("Your clan tag must be less than 5 characters!")
            elif len(tagClan.content) < 2:
                return await self.bot.say("Your clan tag must be more than 2 characters!")
            await self.bot.say("Choose your clan description.")
            descClan = await self.bot.wait_for_message(timeout=20, author=ctx.message.author)
            if any(badword in descClan.content for badword in chat_filter):
                embed=discord.Embed(title="{}, insults are not allowed!".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if len(descClan.content) > 500:
                return await self.bot.say("Your clan description must be less than 500 characters!")
            await checks.clan_create(self, clanid, ctx.message.author.id, owner, nameClan.content, tagClan.content, owner, ctx.message.author.id, 1, 5, descClan.content, ts, "Owner", "https://i.imgur.com/vbpKqh8.png")
            await self.bot.say("Your clan has been created!")
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET clanlicense = :clanlicense WHERE id = :id", {'clanlicense': None, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
        else:
            return await self.bot.say("You need a Clan License to create a clan!")

    @clan.command(pass_context=True, name="profile", aliases=["p"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _profile(self, ctx, user: discord.Member=None):
        ts = time.time()
        asd = "{}, this user isn't in any clan."
        if user is None:
            user = ctx.message.author
            asd = "{}, you are not in any clan."
        clancheck = await checks.clan_check(self, user.id)
        if clancheck is None:
            embed=discord.Embed(title=asd.format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = clancheck[1]
        userdata = await checks.clan_members(self, ownerid)
        members = []
        for x in userdata:
            members.append(x[6])
        totalcrystals = 0
        totalwins = 0
        totallosts = 0
        totalredcry = 0
        for i in members:
            userdata = await checks.database_check(self, i)
            totalcrystals += userdata[7]
            totalwins += userdata[9]
            totallosts += userdata[10]
            totalredcry += userdata[15]
        ownerClan = clancheck[2]
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanowner = await checks.clan_check(self, ownerid)
        created = clanowner[10]
        idd = clanowner[0]
        created = ts - created
        created = ConvertSectoDay(int(created))
        membercount = clanowner[7]
        clanslots = clanowner[8]
        logo = clanowner[12]
        desc = clanowner[9]
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT clans.clanid,  clans.tag, clans.name, users.name,  sum(users.coins) FROM clans INNER JOIN users ON clans.memberid = users.id GROUP BY clans.clanid ORDER BY sum(users.coins) DESC')
            clans = await cursor.fetchall()
            await cursor.close()
        counter = 0
        place = []
        for i in clans:
            counter += 1
            if i[0] == idd:
                place.append(counter)
        embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0x00ffff)
        embed.add_field(name=f"[{tagClan}] {nameClan}", value=f"**Owner:** {ownerClan}")
        embed.add_field(name=f"Members:", value=f"{membercount}/{clanslots}")
        embed.add_field(name=f"Statistics:", value=f"**Leaderboard place:** {place[0]}\n**Crystals:** {totalcrystals:,} | **Red Crystals:** {totalredcry:,}\n**Wins** {totalwins:,} | **Losses:** {totallosts:,}",inline=False)
        embed.add_field(name=f"Description:", value=desc,inline=False)
        embed.set_footer(text=f"Clan created {created} ago")
        embed.set_thumbnail(url=logo)
        await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="members")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _members(self, ctx, user: discord.Member=None):
        asd = "{}, this user isn't in any clan."
        if user is None:
            user = ctx.message.author
            asd = "{}, this user isn't in any clan."
        clancheck = await checks.clan_check(self, user.id)
        if clancheck is None:
            embed=discord.Embed(title=asd.format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = clancheck[1]
        userdata = await checks.clan_members(self, ownerid)
        members = []
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        ownerid = clancheck[1]
        clanowner = await checks.clan_check(self, ownerid)
        logo = clanowner[12]
        for x in userdata:
            members.append(x[6])
        names = []
        crystals = []
        wins = []
        losts = []
        redcrystals = []
        ranks = []
        memberlist = []
        for i in members:
            userdata = await checks.database_check(self, i)
            data = await checks.clan_check(self, i)
            names.append(userdata[2])
            crystals.append(userdata[7])
            wins.append(userdata[9])
            losts.append(userdata[10])
            redcrystals.append(userdata[15])
            ranks.append(data[11])
        counter = 0
        for name, rank in zip(names, ranks):
            counter += 1
            memberlist.append(f"**{counter}) {name}** ({rank})")
        embed=discord.Embed(title="Tanki Online",url="http://www.tankionlinebot.com", color=0x00ffff)
        embed.add_field(name=f"[{tagClan}] {nameClan}", value="Members")
        embed.set_thumbnail(url=logo)
        embed.add_field(name="\u200b", value="\n".join(memberlist),inline=False)
        return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="upgrade")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _upgrade(self, ctx):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        redcry = data[15]
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanowner = await checks.clan_check(self, ownerid)
        clanslots = clanowner[8]
        if clanslots == 10:
            embed=discord.Embed(title="{}, your clan has reached max slots!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        if ownerid == ctx.message.author.id:
            if clanslots == 10:
                embed=discord.Embed(title="{}, your clan has reached max slots!".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            if redcry < 600:
                embed=discord.Embed(title=f"{ctx.message.author.display_name} you don't have enough red crystals! You need {600 - redcry} more.", color=0x00ffff)
                return await self.bot.say(embed=embed)
            embed=discord.Embed(title=f"{ctx.message.author.display_name} are you sure you want to increase clan slots for 600 Red Crystals?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals - 600 WHERE id = :id", {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET clanslots = :clanslots WHERE id = :id", {'clanslots': 10, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f"{ctx.message.author.display_name}, increased clan slots to 10!", color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title="Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="leave")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _leave(self, ctx):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        memberid = clancheck[6]
        if ownerid == ctx.message.author.id:
            embed=discord.Embed(title="You can't leave your clan. If you would like to delete it use `>clan delete` command.", color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, are you sure you want to leave [{tagClan}] {nameClan} clan?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                await checks.clan_kick(self, memberid)
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET membercount = membercount - 1 WHERE id = :id",
                        {'id': ownerid})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f"You left [{tagClan}] {nameClan} clan.", color=0x00ffff)
                await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title='Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="demote")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _demote(self, ctx, user: discord.Member=None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        userdata = await checks.database_check(self, user.id)
        if userdata is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, {user.display_name} is not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanid = clancheck[0]
        owner = clancheck[2]
        memberid = clancheck[6]
        if ownerid == ctx.message.author.id:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} are you sure you would like to demote {user.display_name}?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET rank = :rank WHERE memberid = :memberid", {'rank': "Member", 'memberid': user.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f"{ctx.message.author.display_name} demoted {user.display_name}!", color=0x00ffff)
                await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title='Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Invalid response. Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)


    @clan.command(pass_context=True, name="promote")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _promote(self, ctx, user: discord.Member=None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        userdata = await checks.database_check(self, user.id)
        if userdata is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, {user.display_name} is not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanid = clancheck[0]
        owner = clancheck[2]
        memberid = clancheck[6]
        if ownerid == ctx.message.author.id:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} are you sure you would like to promote {user.display_name} to Officer rank? He will be able to invite members in your clan.\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET rank = :rank WHERE memberid = :memberid", {'rank': "Officer", 'memberid': user.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f"{ctx.message.author.display_name} promoted {user.display_name} to Officer rank!", color=0x00ffff)
                await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title='Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Invalid response. Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)


    @clan.command(pass_context=True, name="kick")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _kick(self, ctx, user: discord.Member=None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        kickedid = await checks.clan_check(self, user.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        userdata = await checks.database_check(self, user.id)
        if userdata is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, {user.display_name} is not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanid = clancheck[0]
        owner = clancheck[2]
        memberid = kickedid[6]
        if ownerid == ctx.message.author.id:
            data = await checks.clan_check(self, user.id)
            if data is None:
                embed=discord.Embed(title=f'{user.display_name}, {ctx.message.author.display_name} is not in your clan!', color=0x00ffff)
                return await self.bot.say(embed=embed)

            embed=discord.Embed(title=f"{ctx.message.author.display_name}, are you sure you want to kick {user.display_name} from your clan?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                await checks.clan_kick(self, memberid)
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET membercount = membercount - 1 WHERE id = :id",
                        {'id': ownerid})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f'{ctx.message.author.display_name}, kicked {user.display_name} from his clan!', color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title='Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)

        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)


    @clan.command(pass_context=True, name="invite", aliases=["add"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _invite(self, ctx, user: discord.Member=None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        userdata = await checks.database_check(self, user.id)
        if userdata is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, {user.display_name} is not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        clanowner = await checks.clan_check(self, ownerid)
        username = userdata[2]
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanid = clancheck[0]
        clanslots = clanowner[8]
        owner = clancheck[2]
        rank = clancheck[11]
        print(rank)
        membercount = clanowner[7]
        if rank == "Owner":
            data = await checks.clan_check(self, user.id)
            if membercount == clanslots:
                embed=discord.Embed(title=f'{ctx.message.author.display_name}, your clan is full.\nConsider upgrading your clan slots by using `>clan upgrade` command.', color=0x00ffff)
                return await self.bot.say(embed=embed)
            if data is None:
                embed=discord.Embed(title=f'{user.display_name}, {ctx.message.author.display_name} is inviting you to "{nameClan}" clan.\n• Accept\n• Deny', color=0x00ffff)
                await self.bot.say(embed=embed)
                msg = await self.bot.wait_for_message(timeout=15, author=user)
                if msg is None:
                    return await self.bot.say(f"{user.display_name} you took long to respond.")
                elif msg.content.lower() == "accept":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE clans SET membercount = membercount + 1 WHERE id = :id",
                            {'id': ownerid})
                        await db.commit()
                        await cursor.close()
                    await checks.clan_invite(self, clanid, ctx.message.author.id, owner, nameClan, tagClan, username, user.id, "-", "-", "-", "-","Member", None)
                    embed=discord.Embed(title=f'{user.display_name} has joined "{nameClan}" clan.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif msg.content.lower() == "deny":
                    embed=discord.Embed(title=f'{ctx.message.author.display_name}, {user.display_name} rejected your invitation to your clan.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    embed=discord.Embed(title=f'{user.display_name}, invalid response.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title=f"{user.display_name} is already in a clan!", color=0x00ffff)
                return await self.bot.say(embed=embed)
        elif rank == "Officer":
            data = await checks.clan_check(self, user.id)
            if membercount == clanslots:
                embed=discord.Embed(title=f'{ctx.message.author.display_name}, your clan is full.\nConsider upgrading your clan slots by using `>clan upgrade` command.', color=0x00ffff)
                return await self.bot.say(embed=embed)
            if data is None:
                embed=discord.Embed(title=f'{user.display_name}, {ctx.message.author.display_name} is inviting you to "{nameClan}" clan.\n• Accept\n• Deny', color=0x00ffff)
                await self.bot.say(embed=embed)
                msg = await self.bot.wait_for_message(timeout=15, author=user)
                if msg is None:
                    return await self.bot.say(f"{user.display_name} you took long to respond.")
                elif msg.content.lower() == "accept":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE clans SET membercount = membercount + 1 WHERE id = :id",
                            {'id': ownerid})
                        await db.commit()
                        await cursor.close()
                    await checks.clan_invite(self, clanid, ownerid, owner, nameClan, tagClan, username, user.id, "-", "-", "-", "-","Member", None)
                    embed=discord.Embed(title=f'{user.display_name} has joined "{nameClan}" clan.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif msg.content.lower() == "deny":
                    embed=discord.Embed(title=f'{ctx.message.author.display_name}, {user.display_name} rejected your invitation to your clan.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    embed=discord.Embed(title=f'{ctx.message.author.display_name}, invalid response.', color=0x00ffff)
                    return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title=f"{user.display_name} is already in a clan!", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="description", aliases=["desc", "setdescription", "setdesc"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _description(self, ctx, *, desc = None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        if desc is None:
            return await self.bot.say("You didnt enter a description. Correct usage: `>clan description Hello guys blah blah`")
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        redcry = data[15]
        if ownerid == ctx.message.author.id:
            if len(desc) > 500:
                return await self.bot.say("Your clan description must be less than 500 characters!")
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE clans SET desc = :desc WHERE id = :id", {'desc': desc, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you set your clans description to: _{desc}_", color=0x00ffff)
            return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="logo")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _logo(self, ctx, link = None):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        data = await checks.database_check(self, ctx.message.author.id)
        redcry = data[15]
        if link is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you didn't provide an image link.\n**Correct usage:** Upload your logo to https://imgur.com/ Right click on image then click 'Copy image URL or adress' and then run the command\n`>clan logo [link]`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        if "https://i.imgur.com/" not in link:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you didn't provide an image link.\n**Correct usage:** Upload your logo to https://imgur.com/ Right click on image then click 'Copy image URL or adress' and then run the command\n`>clan logo [link]`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        if data is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        if ownerid == ctx.message.author.id:
            if redcry < 100:
                embed=discord.Embed(title=f"{ctx.message.author.display_name} you don't have enough red crystals! You need {100 - redcry} more.", color=0x00ffff)
                return await self.bot.say(embed=embed)
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, are you sure you want to change your clan logo?\n**Price:** 100 Red Crystals\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                logo = clancheck[12]
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET logo = :logo WHERE id = :id", {'logo': link, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals - 100 WHERE id = :id", {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f"{ctx.message.author.display_name} you have successfully changed your clan logo!", color=0x00ffff)
                await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="rename")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _rename(self, ctx):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        redcry = data[15]
        ownerid = str(clancheck[1])
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        clanowner = await checks.clan_check(self, ownerid)
        clanslots = clanowner[8]
        if ownerid == ctx.message.author.id:
            if redcry < 100:
                embed=discord.Embed(title=f"{ctx.message.author.display_name} you don't have enough red crystals! You need {100 - redcry} more.", color=0x00ffff)
                return await self.bot.say(embed=embed)
            embed=discord.Embed(title=f"{ctx.message.author.display_name} What would you like to rename? 100 Red Crystals\n• Name\n• Tag\n• Cancel", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
            elif msg.content.lower() == "name":
                embed=discord.Embed(title=f"{ctx.message.author.display_name} Please enter your new clan name.", color=0x00ffff)
                await self.bot.say(embed=embed)
                msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
                if msg is None:
                    return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET name = :name WHERE id = :id", {'name': msg.content, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals - 100 WHERE id = :id", {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f'{ctx.message.author.display_name}, you have successfully changed your clan name to [{msg.content}]', color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content.lower() == "tag":
                embed=discord.Embed(title=f"{ctx.message.author.display_name} Please enter your new clan tag.", color=0x00ffff)
                await self.bot.say(embed=embed)
                msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
                if msg is None:
                    return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE clans SET tag = :tag WHERE id = :id", {'tag': msg.content, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals - 100 WHERE id = :id", {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title=f'{ctx.message.author.display_name}, you have successfully changed your clan tag to [{msg.content}]', color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content.lower() == "cancel":
                embed=discord.Embed(title="Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                embed=discord.Embed(title="Invalid response. Exiting...", color=0x00ffff)
                return await self.bot.say(embed=embed)
        else:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not the clan owner!", color=0x00ffff)
            return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="delete")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _delete(self, ctx):
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        if clancheck is None:
            embed=discord.Embed(title="You are not in any clan!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title=f"{ctx.message.author.display_name} you are not registered!", color=0x00ffff)
            return await self.bot.say(embed=embed)
        ownerid = str(clancheck[1])
        clanid = clancheck[0]
        nameClan = clancheck[3]
        tagClan = clancheck[4]
        print(clanid)
        if ownerid == ctx.message.author.id:
            embed=discord.Embed(title=f"{ctx.message.author.display_name}, are your sure you would like to delete your clan?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{user.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                await checks.clan_delete(self, clanid)
                embed=discord.Embed(title=f"{ctx.message.author.display_name}, You have successfully deleted [{tagClan}] {nameClan} clan.", color=0x00ffff)
                await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title=f'Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)

    @clan.command(pass_context=True, name="license")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _license(self, ctx):
        print("1")
        data = await checks.database_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        redcry = data[15]
        print("2")
        licensecheck = data[14]
        if licensecheck:
            return await self.bot.say("You already have a clan license. Start creating a clan using `>clan create` command.")
        clancheck = await checks.clan_check(self, ctx.message.author.id)
        print("3")
        if clancheck is not None:
            await self.bot.say("You must leave your current clan.")
        else:
            print("6")
            if redcry < 1000:
                print("5")
                embed=discord.Embed(title=f"{ctx.message.author.display_name} you don't have enough red crystals! You need {1000 - redcry} more.", color=0x00ffff)
                return await self.bot.say(embed=embed)
            embed=discord.Embed(title=f"{ctx.message.author.display_name} are you sure you want to buy a clan license for 1,000 Red Crystals?\n• Yes\n• No", color=0x00ffff)
            await self.bot.say(embed=embed)
            print("6")
            msg = await self.bot.wait_for_message(timeout=15, author=ctx.message.author)
            if msg is None:
                return await self.bot.say(f"{ctx.message.author.display_name} you too long to respond.")
            elif msg.content.lower() == "yes":
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET redcrystals = redcrystals - 1000 WHERE id = :id", {'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET clanlicense = :clanlicense WHERE id = :id", {'clanlicense': 1, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title='You have purchased clan license. Start creating one using `>clan create` command.', color=0x00ffff)
                return await self.bot.say(embed=embed)
            elif msg.content.lower() == "no":
                embed=discord.Embed(title=f'Exiting...', color=0x00ffff)
                return await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Clans(bot))
