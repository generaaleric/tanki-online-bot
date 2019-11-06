import aiohttp
import discord
import json
import random
import aiosqlite
from num2words import num2words
import num2words as n2w
import itertools as it
import re
import asyncio
from discord.ext import commands
import logging
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete,increment
from data.hulls_turrets import turret_id, hull_id, paint_id
import data.checks as checks
from data.checks import blacklist_check

with open('data/ratings.json', encoding='utf-8') as file:
    ratings_normal = json.load(file)
with open('data/ratings_premium.json', encoding='utf-8') as file:
    ratings_premium = json.load(file)

cm = TinyDB('commands.json')
Commands = Query()

class Tanki:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top(self, ctx):
        if cm.contains(Commands.command == 'top'):
            cm.update(increment('usage'), Commands.command == 'top')

        else:
            cm.insert({'command': "top", 'usage': 1})
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Top Command <==```\n**Description:** Displays the top players of the week.\n\n**Command:** `>top`\n\n**Usage:** \n`>top crystals`\n`>top golds`\n`>top score`\n`>top efficiency`\n\n**Example:** `>top crystals`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)



    @commands.command(pass_context=True)
    @checks.blacklist_check()
    async def gamemodes(self, ctx, nickname: str = None):
        if cm.contains(Commands.command == 'gamemodes'):
            cm.update(increment('usage'), Commands.command == 'gamemodes')
        else:
            cm.insert({'command': "gamemodes", 'usage': 1})
        link = "https://ratings.tankionline.com/api/eu/profile/?user={}&lang=en"
        if nickname is None:
            data = await checks.database_check(self, ctx.message.author.id)
            tankinick = data[12]
            if tankinick is None:
                embed=discord.Embed(title="{}".format("You didn't give me a nickname or you haven't linked your profile with your Tanki Online account. Link it by using the >set [nickname]."), color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                url = link.format(tankinick)
        else:
            url = link.format(nickname)

        if cm.contains(Commands.command == 'gamemodes'):
            cm.update(increment('usage'), Commands.command == 'gamemodes')

        else:
            cm.insert({'command': "gamemodes", 'usage': 1})
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    nick = response["name"]
                    await self.bot.send_typing(ctx.message.channel)
                    modesplayed = response["modesPlayed"]
                    #==================================#
                    deathmatch = modesplayed[0]
                    dm = deathmatch["name"]
                    dmscore = deathmatch["scoreEarned"]
                    dmtime = deathmatch["timePlayed"]
                    dmtime = int(dmtime)
                    dmhours = dmtime/3600000
                    #==================================#
                    teamdeathmatch = modesplayed[1]
                    tdm = teamdeathmatch["name"]
                    tdmscore = teamdeathmatch["scoreEarned"]
                    tdmtime = teamdeathmatch["timePlayed"]
                    tdmtime = int(tdmtime)
                    tdmhours = tdmtime/3600000
                    #==================================#
                    capturetheflag = modesplayed[2]
                    ctf = capturetheflag["name"]
                    ctfscore = capturetheflag["scoreEarned"]
                    ctftime = capturetheflag["timePlayed"]
                    ctftime = int(ctftime)
                    ctfhours = ctftime/3600000
                    #==================================#
                    controlpoints = modesplayed[3]
                    cp = controlpoints["name"]
                    cpscore = controlpoints["scoreEarned"]
                    cptime = controlpoints["timePlayed"]
                    cptime = int(cptime)
                    cphours = cptime/3600000
                    #==================================#
                    assault = modesplayed[4]
                    ass = assault["name"]
                    assscore = assault["scoreEarned"]
                    asstime = assault["timePlayed"]
                    asstime = int(asstime)
                    asshours = asstime/3600000
                    #==================================#
                    embed = discord.Embed(title = "Tanki Online Ratings",
                      url = "http://www.tankionlinebot.com",\
                      description = "Gamemodes", color = 0x80ffff)
                    embed.add_field(name = "{}".format(dm), value = "**Mode:** {}\n**Score:** {:,}\n**Time:** {}".format(dm, dmscore, round(dmhours)))
                    embed.add_field(name = "{}".format(tdm), value = "**Mode:** {}\n**Score:** {:,}\n**Time:** {}".format(tdm, tdmscore, round(tdmhours)))
                    embed.add_field(name = "{}".format(ctf), value = "**Mode:** {}\n**Score:** {:,}\n**Time:** {}".format(ctf, ctfscore, round(ctfhours)))
                    embed.add_field(name = "{}".format(cp), value = "**Mode:** {}\n**Score:** {:,}\n**Time:** {}".format(cp, cpscore, round(cphours)))
                    embed.add_field(name = "{}".format(ass), value = "**Mode:** {}\n**Score:** {:,}\n**Time:** {}".format(ass, assscore, round(asshours)))
                    embed.add_field(name = "\u200b", value = "\u200b")
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Account does not exist.")



    @top.command(pass_context = True, aliases = ["cry"])
    async def crystals(self, ctx):
        if cm.contains(Commands.command == 'crystals'):
            cm.update(increment('usage'), Commands.command == 'crystals')

        else:
            cm.insert({'command': "crystals", 'usage': 1})
        url = "https://ratings.tankionline.com/api/eu/top/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    crystals = response["crystals"]
                    #===============================#
                    miden = crystals[0]
                    midenname = miden["uid"]
                    midencrystals = miden["value"]
                    #===============================#
                    ena = crystals[1]
                    enaname = ena["uid"]
                    enacrystals = ena["value"]
                    #===============================#
                    duo = crystals[2]
                    duoname = duo["uid"]
                    duocrystals = duo["value"]
                    #===============================#
                    tria = crystals[3]
                    trianame = tria["uid"]
                    triacrystals = tria["value"]
                    #===============================#
                    tesera = crystals[4]
                    teseraname = tesera["uid"]
                    teseracrystals = tesera["value"]
                    #===============================#
                    pente = crystals[5]
                    pentename = pente["uid"]
                    pentecrystals = pente["value"]
                    #===============================#
                    eksi = crystals[6]
                    eksiname = eksi["uid"]
                    eksicrystals = eksi["value"]
                    #===============================#
                    efta = crystals[7]
                    eftaname = efta["uid"]
                    eftacrystals = efta["value"]
                    #===============================#
                    oxto = crystals[8]
                    oxtoname = oxto["uid"]
                    oxtocrystals = oxto["value"]
                    #===============================#
                    enea = crystals[9]
                    eneaname = enea["uid"]
                    eneacrystals = enea["value"]
                    #===============================#
                    embed = discord.Embed(title = "Tanki Online Ratings",
                      url = "http://www.tankionlinebot.com",\
                      description = "Top 10 Players with the most crystals earned", color = 0x80ffff)
                    embed.add_field(name = "1. {}".format(midenname), value = "Crystals: {:,}".format(midencrystals),inline=False)
                    embed.add_field(name = "2. {}".format(enaname), value = "Crystals: {:,}".format(enacrystals),inline=False)
                    embed.add_field(name = "3. {}".format(duoname), value = "Crystals: {:,}".format(duocrystals),inline=False)
                    embed.add_field(name = "4. {}".format(trianame), value = "Crystals: {:,}".format(triacrystals),inline=False)
                    embed.add_field(name = "5. {}".format(teseraname), value = "Crystals: {:,}".format(teseracrystals),inline=False)
                    embed.add_field(name = "6. {}".format(pentename), value = "Crystals: {:,}".format(pentecrystals),inline=False)
                    embed.add_field(name = "7. {}".format(eksiname), value = "Crystals: {:,}".format(eksicrystals),inline=False)
                    embed.add_field(name = "8. {}".format(eftaname), value = "Crystals: {:,}".format(eftacrystals),inline=False)
                    embed.add_field(name = "9. {}".format(oxtoname), value = "Crystals: {:,}".format(oxtocrystals),inline=False)
                    embed.add_field(name = "10. {}".format(eneaname), value = "Crystals: {:,}".format(eneacrystals),inline=False)
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Tanki Online servers are not available right now.")


    @top.command(pass_context = True)
    async def golds(self, ctx):
        if cm.contains(Commands.command == 'golds'):
            cm.update(increment('usage'), Commands.command == 'golds')
        else:
            cm.insert({'command': "golds", 'usage': 1})
        url = "https://ratings.tankionline.com/api/eu/top/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    golds = response["golds"]
                    #===============================#
                    miden = golds[0]
                    midenname = miden["uid"]
                    midengolds = miden["value"]
                    #===============================#
                    ena = golds[1]
                    enaname = ena["uid"]
                    enagolds = ena["value"]
                    #===============================#
                    duo = golds[2]
                    duoname = duo["uid"]
                    duogolds = duo["value"]
                    #===============================#
                    tria = golds[3]
                    trianame = tria["uid"]
                    triagolds = tria["value"]
                    #===============================#
                    tesera = golds[4]
                    teseraname = tesera["uid"]
                    teseragolds = tesera["value"]
                    #===============================#
                    pente = golds[5]
                    pentename = pente["uid"]
                    pentegolds = pente["value"]
                    #===============================#
                    eksi = golds[6]
                    eksiname = eksi["uid"]
                    eksigolds = eksi["value"]
                    #===============================#
                    efta = golds[7]
                    eftaname = efta["uid"]
                    eftagolds = efta["value"]
                    #===============================#
                    oxto = golds[8]
                    oxtoname = oxto["uid"]
                    oxtogolds = oxto["value"]
                    #===============================#
                    enea = golds[9]
                    eneaname = enea["uid"]
                    eneagolds = enea["value"]
                    #===============================#
                    embed = discord.Embed(title = "Tanki Online Ratings",
                      url = "http://www.tankionlinebot.com",\
                      description = "Top 10 Players with the most golds caught", color = 0x80ffff)
                    embed.add_field(name = "1. {}".format(midenname), value = "Golds: {:,}".format(midengolds),inline=False)
                    embed.add_field(name = "2. {}".format(enaname), value = "Golds: {:,}".format(enagolds),inline=False)
                    embed.add_field(name = "3. {}".format(duoname), value = "Golds: {:,}".format(duogolds),inline=False)
                    embed.add_field(name = "4. {}".format(trianame), value = "Golds: {:,}".format(triagolds),inline=False)
                    embed.add_field(name = "5. {}".format(teseraname), value = "Golds: {:,}".format(teseragolds),inline=False)
                    embed.add_field(name = "6. {}".format(pentename), value = "Golds: {:,}".format(pentegolds),inline=False)
                    embed.add_field(name = "7. {}".format(eksiname), value = "Golds: {:,}".format(eksigolds),inline=False)
                    embed.add_field(name = "8. {}".format(eftaname), value = "Golds: {:,}".format(eftagolds),inline=False)
                    embed.add_field(name = "9. {}".format(oxtoname), value = "Golds: {:,}".format(oxtogolds),inline=False)
                    embed.add_field(name = "10. {}".format(eneaname), value = "Golds: {:,}".format(eneagolds),inline=False)
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Tanki Online servers are not available right now.")

    @top.command(pass_context = True, aliases = ["xp"])
    async def score(self, ctx):
        if cm.contains(Commands.command == 'score'):
            cm.update(increment('usage'), Commands.command == 'score')
        else:
            cm.insert({'command': "score", 'usage': 1})
        url = "https://ratings.tankionline.com/api/eu/top/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    score = response["score"]
                    #===============================#
                    miden = score[0]
                    midenname = miden["uid"]
                    midenscore = miden["value"]
                    #===============================#
                    ena = score[1]
                    enaname = ena["uid"]
                    enascore = ena["value"]
                    #===============================#
                    duo = score[2]
                    duoname = duo["uid"]
                    duoscore = duo["value"]
                    #===============================#
                    tria = score[3]
                    trianame = tria["uid"]
                    triascore = tria["value"]
                    #===============================#
                    tesera = score[4]
                    teseraname = tesera["uid"]
                    teserascore = tesera["value"]
                    #===============================#
                    pente = score[5]
                    pentename = pente["uid"]
                    pentescore = pente["value"]
                    #===============================#
                    eksi = score[6]
                    eksiname = eksi["uid"]
                    eksiscore = eksi["value"]
                    #===============================#
                    efta = score[7]
                    eftaname = efta["uid"]
                    eftascore = efta["value"]
                    #===============================#
                    oxto = score[8]
                    oxtoname = oxto["uid"]
                    oxtoscore = oxto["value"]
                    #===============================#
                    enea = score[9]
                    eneaname = enea["uid"]
                    eneascore = enea["value"]
                    #===============================#
                    embed = discord.Embed(title = "Tanki Online Ratings",
                      url = "http://www.tankionlinebot.com",\
                      description = "Top 10 Players with the most score earned", color = 0x80ffff)
                    embed.add_field(name = "1. {}".format(midenname), value = "Score: {:,}".format(midenscore),inline=False)
                    embed.add_field(name = "2. {}".format(enaname), value = "Score: {:,}".format(enascore),inline=False)
                    embed.add_field(name = "3. {}".format(duoname), value = "Score: {:,}".format(duoscore),inline=False)
                    embed.add_field(name = "4. {}".format(trianame), value = "Score: {:,}".format(triascore),inline=False)
                    embed.add_field(name = "5. {}".format(teseraname), value = "Score: {:,}".format(teserascore),inline=False)
                    embed.add_field(name = "6. {}".format(pentename), value = "Score: {:,}".format(pentescore),inline=False)
                    embed.add_field(name = "7. {}".format(eksiname), value = "Score: {:,}".format(eksiscore),inline=False)
                    embed.add_field(name = "8. {}".format(eftaname), value = "Score: {:,}".format(eftascore),inline=False)
                    embed.add_field(name = "9. {}".format(oxtoname), value = "Score: {:,}".format(oxtoscore),inline=False)
                    embed.add_field(name = "10. {}".format(eneaname), value = "Score: {:,}".format(eneascore),inline=False)
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Tanki Online servers are not available right now.")

    @top.command(pass_context = True)
    async def efficiency(self, ctx):
        if cm.contains(Commands.command == 'efficiency'):
            cm.update(increment('usage'), Commands.command == 'efficiency')

        else:
            cm.insert({'command': "efficiency", 'usage': 1})
        url = "https://ratings.tankionline.com/api/eu/top/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    efficiency = response["efficiency"]
                    #===============================#
                    miden = efficiency[0]
                    midenname = miden["uid"]
                    midenefficiency = miden["value"]
                    lol = 100
                    asd0 = midenefficiency/lol
                    #===============================#
                    ena = efficiency[1]
                    enaname = ena["uid"]
                    enaefficiency = ena["value"]
                    asd1 = enaefficiency/lol
                    #===============================#
                    duo = efficiency[2]
                    duoname = duo["uid"]
                    duoefficiency = duo["value"]
                    asd2 = duoefficiency/lol
                    #===============================#
                    tria = efficiency[3]
                    trianame = tria["uid"]
                    triaefficiency = tria["value"]
                    asd3 = triaefficiency/lol
                    #===============================#
                    tesera = efficiency[4]
                    teseraname = tesera["uid"]
                    teseraefficiency = tesera["value"]
                    asd4 = teseraefficiency/lol
                    #===============================#
                    pente = efficiency[5]
                    pentename = pente["uid"]
                    penteefficiency = pente["value"]
                    asd5 = penteefficiency/lol
                    #===============================#
                    eksi = efficiency[6]
                    eksiname = eksi["uid"]
                    eksiefficiency = eksi["value"]
                    asd6 = eksiefficiency/lol
                    #===============================#
                    efta = efficiency[7]
                    eftaname = efta["uid"]
                    eftaefficiency = efta["value"]
                    asd7 = eftaefficiency/lol
                    #===============================#
                    oxto = efficiency[8]
                    oxtoname = oxto["uid"]
                    oxtoefficiency = oxto["value"]
                    asd8 = oxtoefficiency/lol
                    #===============================#
                    enea = efficiency[9]
                    eneaname = enea["uid"]
                    eneaefficiency = enea["value"]
                    asd9 = eneaefficiency/lol
                    #===============================#
                    embed = discord.Embed(title = "Tanki Online Ratings",
                      url = "http://www.tankionlinebot.com",\
                      description = "Top 10 Most efficient players", color = 0x80ffff)
                    embed.add_field(name = "1. {}".format(midenname), value = "Efficiency: {:,}".format(round(asd0)),inline=False)
                    embed.add_field(name = "2. {}".format(enaname), value = "Efficiency: {:,}".format(round(asd1)),inline=False)
                    embed.add_field(name = "3. {}".format(duoname), value = "Efficiency: {:,}".format(round(asd2)),inline=False)
                    embed.add_field(name = "4. {}".format(trianame), value = "Efficiency: {:,}".format(round(asd3)),inline=False)
                    embed.add_field(name = "5. {}".format(teseraname), value = "Efficiency: {:,}".format(round(asd4)),inline=False)
                    embed.add_field(name = "6. {}".format(pentename), value = "Efficiency: {:,}".format(round(asd5)),inline=False)
                    embed.add_field(name = "7. {}".format(eksiname), value = "Efficiency: {:,}".format(round(asd6)),inline=False)
                    embed.add_field(name = "8. {}".format(eftaname), value = "Efficiency: {:,}".format(round(asd7)),inline=False)
                    embed.add_field(name = "9. {}".format(oxtoname), value = "Efficiency: {:,}".format(round(asd8)),inline=False)
                    embed.add_field(name = "10. {}".format(eneaname), value = "Efficiency: {:,}".format(round(asd9)),inline=False)
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Tanki Online servers are not available right now.")



    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def ratings(self, ctx, nickname: str = None):
        if cm.contains(Commands.command == 'ratings'):
            cm.update(increment('usage'), Commands.command == 'ratings')
        else:
            cm.insert({'command': "ratings", 'usage': 1})
        link = "https://ratings.tankionline.com/api/eu/profile/?user={}&lang=en"
        if nickname is None:
            data = await checks.database_check(self, ctx.message.author.id)
            tankinick = data[12]
            if tankinick is None:
                embed=discord.Embed(title="You didn't give me a nickname or you haven't linked your profile with your Tanki Online account. Link it by using the >set [nickname].", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                url = link.format(tankinick)
        else:
            url = link.format(nickname)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    #=====Main================================
                    nick = response["name"]
                    experience = response["score"]
                    next = response["scoreNext"]
                    crystals = response["earnedCrystals"]
                    gearScore = response["gearScore"]
                    kills = response["kills"]
                    level = response["rank"]
                    premium = response["hasPremium"]
                    golds = response["caughtGolds"]
                    deaths = response["deaths"]
                    if deaths != 0:
                        kd = kills/deaths
                    else:
                        kd = kills
                    #=====Supplies================================
                    q = response["suppliesUsage"][0]["usages"]
                    w = response["suppliesUsage"][1]["usages"]
                    e = response["suppliesUsage"][2]["usages"]
                    r = response["suppliesUsage"][3]["usages"]
                    t = response["suppliesUsage"][4]["usages"]
                    y = response["suppliesUsage"][5]["usages"]
                    u = response["suppliesUsage"][6]["usages"]
                    totalSupplies = q + w + e + r + t + y + u
                    #=====Playtime================================
                    modesplayed = response["modesPlayed"]
                    q = response["modesPlayed"][0]["timePlayed"]
                    w = response["modesPlayed"][1]["timePlayed"]
                    e = response["modesPlayed"][2]["timePlayed"]
                    r = response["modesPlayed"][3]["timePlayed"]
                    t = response["modesPlayed"][4]["timePlayed"]
                    y = response["modesPlayed"][5]["timePlayed"]
                    u = response["modesPlayed"][6]["timePlayed"]
                    timeSeconds = q + w + e + r + t + y + u
                    hours = int(timeSeconds) / 3600000

                    #=====Equipped================================
                    mounted_hull = response["mounted"]["armor"]
                    mounted_turret = response["mounted"]["weapon"]
                    mounted_paint = response["mounted"]["coloring"]
                    try:
                        mount_turr = turret_id[mounted_turret]
                        mount_hull = hull_id[mounted_hull]
                    except:
                        mount_turr = "404 Not Found"
                        mount_hull = "404 Not Found"
                    try:
                        linksplited = mounted_paint.split("/")
                        mount_paint = paint_id[linksplited[len(linksplited) - 2]]
                    except:
                        if linksplited != "26316675520427":
                            mount_paint = paint_id["26316675520427"]
                        else:
                            mount_paint = paint_id[linksplited[len(linksplited) - 2]]
                    #=====Checks================================
                    if level > 30:
                        flevel = level - 30
                        level = 31
                    else:
                        flevel = level
                    if premium:
                        for key, value in ratings_premium[str(level)].items():
                            rank = key.format(flevel)
                            if rank == "Legend 1":
                                rank = "Legend"
                            image= value
                            co = 0xf4e541
                    else:
                        for key, value in ratings_normal[str(level)].items():
                            rank = key.format(flevel)
                            if rank == "Legend 1":
                                rank = "Legend"
                            image= value
                            co = 0x42d9f4

                    embed=discord.Embed(title=f"Statistics for {nick}", color=co)
                    embed.set_thumbnail(url=f"{image}")
                    embed.add_field(name="Nickname", value=f"<:re:490871085466648576>{nick}", inline=True)
                    embed.add_field(name="Rank", value=f"{rank}", inline=True)
                    embed.add_field(name="Statistics", value=f"<:445:490871457337966593>**Experience:** {experience:,}xp | {experience - next}xp left\n:gear:**Gear Score:** {gearScore:,}\n<:cr:490871083797315607>**Crystals Obtained:** {crystals:,}\n<:gb:490871084258820096>**Gold Boxes caught:** {golds:,}\n<:88:490878529240825885>**Supplies used:** {totalSupplies:,}\n:clock1:**Hours in game:** {int(hours):,}", inline=False)
                    embed.add_field(name="<:equip_1:546497402777894912>Equipped", value=f"{mount_turr} | {mount_hull} | {mount_paint}\n\n<:Kills:490166554869104640>**Kills:** {kills:,}   <:Deaths:490166554630160405>**Deaths:** {deaths:,}   <:KD:490166554881687552>**KD:** {kd:.2f}", inline=True)
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Account does not exist.")

    @commands.command(descrption="Shows your XP", pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def xp(self, ctx, nickname: str = None):
        if cm.contains(Commands.command == 'xp'):
            cm.update(increment('usage'), Commands.command == 'xp')
        else:
            cm.insert({'command': "xp", 'usage': 1})
        link = "https://ratings.tankionline.com/api/eu/profile/?user={}&lang=en"
        if nickname is None:
            data = await checks.database_check(self, ctx.message.author.id)
            tankinick = data[12]
            if tankinick is None:
                embed=discord.Embed(title="Please give me a nickname!", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                url = link.format(tankinick)
        else:
            url = link.format(nickname)

        if cm.contains(Commands.command == 'xp'):
            cm.update(increment('usage'), Commands.command == 'xp')

        else:
            cm.insert({'command': "xp", 'usage': 1})

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    kills = response["kills"]
                    deaths = response["deaths"]
                    crystals = response["earnedCrystals"]
                    gold = response["caughtGolds"]
                    experience = response["score"]
                    premium = response["hasPremium"]
                    next = response["scoreNext"]
                    level = response["rank"]
                    nick = response["name"]
                    kd = kills/deaths
                    left = next - experience
                    if response['rank'] > 31:
                        number = level - 30
                    else:
                        number = level
                    if level > 31:
                        level = 31
                    if response["hasPremium"] == False:
                        for key, value in ratings_normal[str(level)].items():
                            rank = key.format(number)
                            ra= value
                        premium = "No"
                        co = 0x42d9f4
                    elif response["hasPremium"] == True:
                        for key, value in ratings_premium[str(level)].items():
                            rank = key.format(number)
                            ra= value
                        premium = "Yes"
                        co = 0xf4e541
                    embed=discord.Embed(title="XP Statistics", url="http://ratings.tankionline.com/en/user/{}/".format(nickname), \
                                        descrption="Tanki Online", color=co)
                    embed.set_thumbnail(url="{}".format(ra))
                    embed.add_field(name="Profile:", value="**Nickname:** \n{}\n\n**Rank:** {}\n{:,}/{:,}\n**Exp left for next rank:** {:,}".format(nick, rank, experience, next, left))
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Account does not exist.")



    # @commands.command(description = "Tanki Online Stats", pass_context = True)
    # @checks.blacklist_check()
    # async def stats(self, ctx):
    #     """Shows Statistics about Tanki online"""
    #     if cm.contains(Commands.command == 'stats'):
    #         cm.update(increment('usage'), Commands.command == 'stats')
    #
    #
    #     else:
    #         cm.insert({'command': "stats", 'usage': 1})
    #     await self.bot.send_typing(ctx.message.channel)
    #     url = "http://tankionline.com/s/status.js?rnd="
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url) as resp:
    #
    #             response = (await resp.json())["response"]
    #             nodes = (await resp.json())["nodes"]
    #             ######Total######
    #             Total = (await resp.json())["total"]
    #             ######Online######
    #             A1 = nodes["main.c1"]
    #             A2 = A1["online"]
    #             B1 = nodes["main.c2"]
    #             B2 = B1["online"]
    #             C1 = nodes["main.c3"]
    #             C2 = C1["online"]
    #             D1 = nodes["main.c4"]
    #             D2 = D1["online"]
    #             E1 = nodes["main.c5"]
    #             E2 = E1["online"]
    #             F1 = nodes["main.c6"]
    #             F2 = F1["online"]
    #             G1 = nodes["main.c7"]
    #             G2 = G1["online"]
    #             H1 = nodes["main.c8"]
    #             H2 = H1["online"]
    #             I1 = nodes["main.c9"]
    #             I2 = I1["online"]
    #             J1 = nodes["main.c10"]
    #             J2 = J1["online"]
    #             K1 = nodes["main.c10"]
    #             K2 = K1["online"]
    #             L1 = nodes["main.c11"]
    #             L2 = L1["online"]
    #             M1 = nodes["main.c12"]
    #             M2 = M1["online"]
    #             N1 = nodes["main.c13"]
    #             N2 = N1["online"]
    #             O1 = nodes["main.c14"]
    #             O2 = O1["online"]
    #             Q1 = nodes["main.c16"]
    #             Q2 = Q1["online"]
    #             R1 = nodes["main.c17"]
    #             R2 = R1["online"]
    #             S1 = nodes["main.c18"]
    #             S2 = S1["online"]
    #             W1 = nodes["main.c19"]
    #             W2 = W1["online"]
    #             Y1 = nodes["main.c20"]
    #             Y2 = Y1["online"]
    #             ######In Battles######
    #             AA1 = nodes["main.c1"]
    #             AA2 = AA1["inbattles"]
    #             BB1 = nodes["main.c2"]
    #             BB2 = BB1["inbattles"]
    #             CC1 = nodes["main.c3"]
    #             CC2 = CC1["inbattles"]
    #             DD1 = nodes["main.c4"]
    #             DD2 = DD1["inbattles"]
    #             EE1 = nodes["main.c5"]
    #             EE2 = EE1["inbattles"]
    #             FF1 = nodes["main.c6"]
    #             FF2 = FF1["inbattles"]
    #             GG1 = nodes["main.c7"]
    #             GG2 = GG1["inbattles"]
    #             HH1 = nodes["main.c8"]
    #             HH2 = HH1["inbattles"]
    #             II1 = nodes["main.c9"]
    #             II2 = II1["inbattles"]
    #             JJ1 = nodes["main.c10"]
    #             JJ2 = JJ1["inbattles"]
    #             KK1 = nodes["main.c10"]
    #             KK2 = KK1["inbattles"]
    #             LL1 = nodes["main.c11"]
    #             LL2 = LL1["inbattles"]
    #             MM1 = nodes["main.c12"]
    #             MM2 = MM1["inbattles"]
    #             NN1 = nodes["main.c13"]
    #             NN2 = NN1["inbattles"]
    #             OO1 = nodes["main.c14"]
    #             OO2 = OO1["inbattles"]
    #             QQ1 = nodes["main.c16"]
    #             QQ2 = QQ1["inbattles"]
    #             RR1 = nodes["main.c17"]
    #             RR2 = RR1["inbattles"]
    #             SS1 = nodes["main.c18"]
    #             SS2 = SS1["inbattles"]
    #             WW1 = nodes["main.c19"]
    #             WW2 = WW1["inbattles"]
    #             YY1 = nodes["main.c20"]
    #             YY2 = YY1["inbattles"]
    #             embed=discord.Embed(title="\u200b", url="http://tankionline.com//", \
    #                                 descrption="Statistics", color=0x42d9f4)
    #             embed.set_author(name="Tanki Online", url="https://discordapp.com", icon_url="https://i.imgur.com/4SKYtfq.png")
    #             embed.add_field(name = "Total players", value = "{:,}".format(Total))
    #             embed.add_field(name = "Players online", value = "{:,}".format(A2 + B2 + C2 + D2 + E2 + F2 + G2 + H2 + I2 + J2 + K2 + L2 + M2 + N2 + O2 + Q2 + R2 + S2 + W2))
    #             embed.add_field(name = "Players in Battles", value = "{:,}".format(AA2 + BB2 + CC2 + DD2 + EE2 + FF2 + GG2 + HH2 + II2 + JJ2 + KK2 + LL2 + MM2 + NN2 + OO2 + QQ2 + RR2 + SS2 + WW2))
    #             await self.bot.say(embed=embed)



    @commands.command(description = "Displays the amount of supplies used by a player", pass_context = True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def supplies(self, ctx, nickname: str = None):
        if cm.contains(Commands.command == 'supplies'):
            cm.update(increment('usage'), Commands.command == 'supplies')
        else:
            cm.insert({'command': "supplies", 'usage': 1})
        link = "https://ratings.tankionline.com/api/eu/profile/?user={}&lang=en"
        if nickname is None:
            data = await checks.database_check(self, ctx.message.author.id)
            tankinick = data[12]
            if tankinick is None:
                embed=discord.Embed(title="You didn't give me a nickname or you haven't linked your profile with your Tanki Online account. Link it by using the >set [nickname].", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                url = link.format(tankinick)
        else:
            url = link.format(nickname)

        if cm.contains(Commands.command == 'supplies'):
            cm.update(increment('usage'), Commands.command == 'supplies')
        else:
            cm.insert({'command': "supplies", 'usage': 1})

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    supplies = response["suppliesUsage"]
                    #==============================#
                    zero = supplies[0]
                    zerousages = zero["usages"]
                    zeroname = zero["name"]
                    #==============================#
                    first = supplies[1]
                    firstusages = first["usages"]
                    firstname = first["name"]
                    #==============================#
                    second = supplies[2]
                    secondusages = second["usages"]
                    secondname = second["name"]
                    #==============================#
                    third = supplies[3]
                    thirdusages = third["usages"]
                    thirdname = third["name"]
                    #==============================#
                    fourth = supplies[4]
                    fourthusages = fourth["usages"]
                    fourthname = fourth["name"]
                    #==============================#
                    fifth = supplies[5]
                    fifthusages = fifth["usages"]
                    fifthname = fifth["name"]
                    #==============================#
                    sixth = supplies[6]
                    sixthusages = sixth["usages"]
                    sixthname = sixth["name"]
                    #==============================#
                    total = firstusages + secondusages + thirdusages + fourthusages + fifthusages + zerousages + sixthusages
                    await self.bot.send_typing(ctx.message.channel)
                    embed = discord.Embed(title = "Ammount of supplies used by {}".format(nickname),
                    url = "http://ratings.tankionline.com/en/user/{}/".format(nickname),\
                    description = "Tanki Online", color = 0x80ffff)
                    embed.add_field(name = "{}".format(zeroname), value = "{:,}".format(zerousages))
                    embed.add_field(name = "{}".format(firstname), value = "{:,}".format(firstusages))
                    embed.add_field(name = "{}".format(secondname), value = "{:,}".format(secondusages))
                    embed.add_field(name = "{}".format(thirdname), value = "{:,}".format(thirdusages))
                    embed.add_field(name = "{}".format(fourthname), value = "{:,}".format(fourthusages))
                    embed.add_field(name = "{}".format(fifthname), value = "{:,}".format(fifthusages))
                    embed.add_field(name = "{}".format(sixthname), value = "{:,}".format(sixthusages))
                    embed.add_field(name = "Total supplies used", value = "{:,}".format(total))
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Account does not exist.")


    @commands.command(descrption="Shows weekly ratings of a player", pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    @checks.blacklist_check()
    async def weekly(self, ctx, nickname: str = None):
        if cm.contains(Commands.command == 'weekly'):
            cm.update(increment('usage'), Commands.command == 'weekly')
        else:
            cm.insert({'command': "weekly", 'usage': 1})
        link = "https://ratings.tankionline.com/api/eu/profile/?user={}&lang=en"
        if nickname is None:
            data = await checks.database_check(self, ctx.message.author.id)
            tankinick = data[12]
            if tankinick is None:
                embed=discord.Embed(title="You didn't give me a nickname or you haven't linked your profile with your Tanki Online account. Link it by using the >set [nickname].", color=0x00ffff)
                return await self.bot.say(embed=embed)
            else:
                url = link.format(tankinick)
        else:
            url = link.format(nickname)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                try:
                    response = (await resp.json())["response"]
                    await self.bot.send_typing(ctx.message.channel)
                    premium = response["hasPremium"]
                    level = response["rank"]
                    nick = response["name"]
                    ratings = response["rating"]
                    cry = ratings["crystals"]
                    cryplace = cry["position"]
                    cryvalue = cry["value"]
                    score = ratings["score"]
                    scoreplace = score["position"]
                    scorevalue = score["value"]
                    gold = ratings["golds"]
                    goldplace = gold["position"]
                    goldvalue = gold["value"]
                    eff = ratings["efficiency"]
                    effplace = eff["position"]
                    effvalue = eff["value"]

                    if response['rank'] == 1:
                        rank = 'Recruit'
                        ra = "https://i.imgur.com/3KICT5F.png"
                    elif response['rank'] == 2:
                        rank = 'Private'
                        ra = "https://i.imgur.com/PZ4ErZa.png"
                    elif response['rank'] == 3:
                        rank = 'Gefreiter'
                        ra = "https://i.imgur.com/20Sxoik.png"
                    elif response['rank'] == 4:
                        rank = 'Corporal'
                        ra = "https://i.imgur.com/HvKlEbw.png"
                    elif response['rank'] == 5:
                        rank = 'Master Corporal'
                        ra = "https://i.imgur.com/PQ8PSVp.png"
                    elif response['rank'] == 6:
                        rank = 'Seargent'
                        ra = "https://i.imgur.com/6yNBMtc.png"
                    elif response['rank'] == 7:
                        rank = 'Staff Seargent'
                        ra = "https://i.imgur.com/rJjRinL.png"
                    elif response['rank'] == 8:
                        rank = 'Master Seargent'
                        ra = "https://i.imgur.com/VLu2VJn.png"
                    elif response['rank'] == 9:
                        rank = 'First Seargent'
                        ra = "https://i.imgur.com/9S1H9fB.png"
                    elif response['rank'] == 10:
                        rank = 'Seargent-Major'
                        ra = "https://i.imgur.com/y2OOLal.png"
                    elif response['rank'] == 11:
                        rank = 'Warrant Officer 1'
                        ra = "https://i.imgur.com/pNLf5Pd.png"
                    elif response['rank'] == 12:
                        rank = 'Warrant Officer 2'
                        ra = "https://i.imgur.com/ezB5xz6.png"
                    elif response['rank'] == 13:
                        rank = 'Warrant Officer 3'
                        ra = "https://i.imgur.com/VQiJCjq.png"
                    elif response['rank'] == 14:
                        rank = 'Warrant Officer 4'
                        ra = "https://i.imgur.com/PGsL8nn.png"
                    elif response['rank'] == 15:
                        rank = 'Warrant Officer 5'
                        ra = "https://i.imgur.com/HqFTAmt.png"
                    elif response['rank'] == 16:
                        rank = 'Third Lieutenant'
                        ra = "https://i.imgur.com/PgxG1Yq.png"
                    elif response['rank'] == 17:
                        rank = 'Second Lieutenant'
                        ra = "https://i.imgur.com/S2MU80A.png"
                    elif response['rank'] == 18:
                        rank = 'First Lieutenant'
                        ra = "https://i.imgur.com/kkw9hpu.png"
                    elif response['rank'] == 19:
                        rank = 'Captain'
                        ra = "https://i.imgur.com/wjZFIFv.png"
                    elif response['rank'] == 20:
                        rank = 'Major'
                        ra = "https://i.imgur.com/HcqJv1C.png"
                    elif response['rank'] == 21:
                        rank = 'Lieutenant Colonel'
                        ra = "https://i.imgur.com/KZF0f6Y.png"
                    elif response['rank'] == 22:
                        rank = 'Colonel'
                        ra = "https://i.imgur.com/ygBsvda.png"
                    elif response['rank'] == 23:
                        rank = 'Brigadier'
                        ra = "https://i.imgur.com/SZ0iqFx.png"
                    elif response['rank'] == 24:
                        rank = 'Major General'
                        ra = "https://i.imgur.com/ymKsRRt.png"
                    elif response['rank'] == 25:
                        rank = 'Lieutenant General'
                        ra = "https://i.imgur.com/MwYo01t.png"
                    elif response['rank'] == 26:
                        rank = 'General'
                        ra = "https://i.imgur.com/hfAG1vE.png"
                    elif response['rank'] == 27:
                        rank = 'Marshal'
                        ra = "https://i.imgur.com/1QjbdpO.png"
                    elif response['rank'] == 28:
                        rank = 'Field Marshal'
                        ra = "https://i.imgur.com/shFvu9l.png"
                    elif response['rank'] == 29:
                        rank = 'Commander'
                        ra = "https://i.imgur.com/ASIfmvy.png"
                    elif response['rank'] == 30:
                        rank = 'Generalissimo'
                        ra = "https://i.imgur.com/MFJbp3f.png"
                    elif response['rank'] >= 31:
                        lev = level - 30
                        rank = 'Legend {}'.format(lev)
                        ra = "https://i.imgur.com/0hZ27iG.png"
                    if response["hasPremium"] == False:
                        premium = "No"
                        co = 0x42d9f4
                    elif response["hasPremium"] == True:
                        premium = "Yes"
                        co = 0xf4e541

                    ORDINAL_NUM_PATTERN = re.compile(r'(?P<numerical>\d+)(?P<suffix>[a-z]+)')


                    def group(iterable, n, fillvalue=None):
                        args = [iter(iterable)]*n
                        return it.zip_longest(*args, fillvalue=fillvalue)


                    def to_cson(cryplace):
                        ordinal = n2w.num2words(cryplace, to='ordinal_num')
                        match = ORDINAL_NUM_PATTERN.fullmatch(ordinal)
                        numerical = match.group('numerical')
                        suffix = match.group('suffix')
                        gs = group(numerical[::-1], 3, fillvalue='')
                        with_commas = (','.join(''.join(g) for g in gs))[::-1]
                        return f'{with_commas}{suffix}'

                    #================================#
                    if cry["position"] == -1:
                        cryplace = '-'
                    else:
                        cryplace = to_cson(cryplace)
                    if cry["value"] == -1:
                        cryvalue = '-'
                    else:
                        cryvalue = '{:,}'.format(cryvalue)
                    #================================#
                    if gold["position"] == -1:
                        goldplace = '-'
                    else:
                        goldplace = to_cson(goldplace)
                    if gold["value"] == -1:
                        goldvalue = '-'
                    else:
                        goldvalue = '{:,}'.format(goldvalue)
                    #================================#
                    if score["position"] == -1:
                        scoreplace = '-'
                    else:
                        scoreplace = to_cson(scoreplace)
                    if score["value"] == -1:
                        scorevalue = '-'
                    else:
                        scorevalue = '{:,}'.format(scorevalue)
                    #================================#
                    if eff["position"] == -1:
                        effplace = '-'
                    else:
                        effplace = to_cson(effplace)
                    if eff["value"] == -1:
                        effvalue = '-'
                    else:
                        lol = 100
                        effvalue = effvalue/lol
                        effvalue = round(effvalue)
                        effvalue = '{:,}'.format(effvalue)
                    #================================#
                    embed=discord.Embed(title="Weekly statistics for {}".format(nickname), url="https://ratings.tankionline.com/en/user/{}".format(nickname), \
                                        descrption="Tanki Online", color=co)
                    embed.set_thumbnail(url="{}".format(ra))
                    embed.add_field(name="Profile:", value="**Nickname:** \n{}\n\n**Experience:**\n__Place:__ {}\n__Value:__ {}\n\n**Gold Boxes:**\n__Place:__ {}\n__Value:__ {}\n\n**Crystals:**\n__Place:__ {}\n__Value:__ {}\n\n**Efficiency:**\n__Place:__ {}\n__Value:__ {}".format(nick, scoreplace, scorevalue, goldplace, goldvalue, cryplace, cryvalue, effplace, effvalue))
                    await self.bot.say(embed=embed)
                except:
                    await self.bot.say("Account does not exist.")
                if cm.contains(Commands.command == 'weekly'):
                    cm.update(increment('usage'), Commands.command == 'weekly')
                else:
                    cm.insert({'command': "weekly", 'usage': 1})


def setup(bot):
    bot.add_cog(Tanki(bot))
