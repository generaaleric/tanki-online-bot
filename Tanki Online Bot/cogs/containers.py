import discord
import datetime
import random
import asyncio
from data.ranks import ranks
import aiosqlite
import numpy
from data.containers_data import item_list, containeradd, colors
import data.checks as checks
from discord.ext import commands
from data.ranks import ranks
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete,increment

cm = TinyDB('commands.json')
Commands = Query()


class Containers:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['cont', 'Cont', 'c', 'C', 'Container', 'контейнер'] )
    @checks.blacklist_check()
    async def container(self, ctx):
        if cm.contains(Commands.command == 'container'):
            cm.update(increment('usage'), Commands.command == 'container')
        else:
            cm.insert({'command': "container", 'usage': 1})


    @container.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                data = await checks.database_container_check(self, ctx.message.author.id)
                if data is None:
                    embed=discord.Embed(title="You are not registered!\nUse `>register`", color=0x00ffff)
                    return await self.bot.say(embed=embed)
                amount = data[2]
                dataa = await checks.database_check(self, ctx.message.author.id)
                naame = dataa[2]
                clancheck = await checks.clan_check(self, ctx.message.author.id)
                if clancheck is None:
                    tagClan = "   ‍   "
                else:
                    tagClan = clancheck[4]
                    tagClan = f"[{tagClan}]"
                common_item = data[3]
                uncommon_item = data[4]
                rare_item = data[5]
                epic_item = data[6]
                legendary_item = data[7]
                exotic_item = data[8]
                embed=discord.Embed(title="Tanki Online",url="https://discord.gg/pXjDfHF", color=0x00ffff)
                embed.add_field(name=f"{tagClan} {naame}", value="**Containers opened: {}**\n\n**Common**: {}\n**Uncommon:** {}\n**Rare:** {}\n**Epic:** {}\n**Legendary:** {}\n**Exotic:** {}".format(amount, common_item, uncommon_item, rare_item, epic_item, legendary_item, exotic_item))
                return await self.bot.say(embed=embed)
            else:
                dataa = await checks.database_container_check(self, user.id)
                if dataa is None:
                    embed=discord.Embed(title="{} They are not registered!".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                amount = dataa[2]
                common_item = dataa[3]
                uncommon_item = dataa[4]
                data = await checks.database_check(self, user.id)
                naame = data[2]
                clancheck = await checks.clan_check(self, user.id)
                if clancheck is None:
                    tagClan = "   ‍   "
                else:
                    tagClan = clancheck[4]
                    tagClan = f"[{tagClan}]"
                rare_item = dataa[5]
                epic_item = dataa[6]
                legendary_item = dataa[7]
                exotic_item = dataa[8]
                embed=discord.Embed(title="Tanki Online",url="https://discord.gg/pXjDfHF", color=0x00ffff)
                embed.add_field(name=f"{tagClan} {naame}", value="**Containers opened: {}**\n\n**Common**: {}\n**Uncommon:** {}\n**Rare:** {}\n**Epic:** {}\n**Legendary:** {}\n**Exotic:** {}".format(amount, common_item, uncommon_item, rare_item, epic_item, legendary_item, exotic_item))
                return await self.bot.say(embed=embed)
        except:
            await self.bot.say(":x: An error occurred while executing the command.")

    # @container.command(pass_context=True, aliases=['shop'])
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def buy(self, ctx):
    #     data = await checks.database_container_check(self, ctx.message.author.id)
    #     if data is None:
    #         embed=discord.Embed(title="You are not registered!\nUse `>register`", color=0x00ffff)
    #         return await self.bot.say(embed=embed)
    #     dataa = await checks.database_check(self, ctx.message.author.id)
    #     coins = dataa[7]
    #     x = await self.bot.say("```md\nContainer Shop\n================\n1. <1 Container> 10,000 Crystals\n2. <5 Containers> 50,000 Crystals\n3. <10 Containers> 100,000 Crystals\n4. <15 Containers> 150,000 Crystals\n5. <30 Containers> 300,000 Crystals\n6. <50 Containers> 500,000 Crystals\n\nType the appropriate number to buy from the shop menu!\n======================================================```")
    #     msg = await self.bot.wait_for_message(timeout=15, channel=ctx.message.channel, author=ctx.message.author)
    #     msgs = ["1","2","3","4","5","6"]
    #     if msg is None:
    #         embed=discord.Embed(title="{}, you took too long to respond.".format(ctx.message.author.display_name), color=0x00ffff)
    #         return await self.bot.say(embed=embed)
    #     elif msg.content not in msgs:
    #         embed=discord.Embed(title="{}, that's an invalid response. Exiting...".format(ctx.message.author.display_name), color=0x00ffff)
    #         return await self.bot.say(embed=embed)
    #         await asyncio.sleep(3)
    #         await self.bot.delete_message(ctx.message)
    #     else:
    #         if msg.content == "1":
    #             if coins < 10000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 1, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 10000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 1 container!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #
    #         elif msg.content == "2":
    #             if coins < 50000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 5, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 50000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 5 containers!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #
    #         elif msg.content == "3":
    #             if coins < 100000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 10, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 100000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 10 containers!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #
    #         elif msg.content == "4":
    #             if coins < 150000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 15, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 150000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 15 containers!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #
    #         elif msg.content == "5":
    #             if coins < 300000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 30, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 300000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 30 containers!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #
    #         elif msg.content == "6":
    #             if coins < 500000:
    #                 embed=discord.Embed(title="{}, you do not have enough crystals for this purchase!".format(ctx.message.author.display_name), color=0x00ffff)
    #                 return await self.bot.say(embed=embed)
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
    #                     {'containers': 50, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             async with aiosqlite.connect('database.db') as db:
    #                 cursor = await db.execute("UPDATE users SET coins = coins - :coins WHERE id = :id",
    #                     {'coins': 500000, 'id': ctx.message.author.id})
    #                 await db.commit()
    #                 await cursor.close()
    #             embed=discord.Embed(title="{}, you have successfully bought 50 containers!".format(ctx.message.author.display_name), color=0x00ffff)
    #             await self.bot.delete_message(x)
    #             return await self.bot.say(embed=embed)
    #         else:
    #             return

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, item=None, amount: int = None):
        if cm.contains(Commands.command == 'sell'):
            cm.update(increment('usage'), Commands.command == 'sell')
        else:
            cm.insert({'command': "sell", 'usage': 1})
        data = await checks.database_container_check(self, ctx.message.author.id)
        if data is None:
            embed=discord.Embed(title="You are not registered!\nUse `>register`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        if item == None:
            return await self.bot.say("What would you like to sell?\n• `>sell supplies` - will sell your supplies (Double Damage, Nitro etc)\n• `>sell paints` - will sell your paints\n• `>sell all` will sell all your items at once!")
        try:
            dataa = await checks.database_check(self, ctx.message.author.id)
            item = item.lower()
            coins = dataa[7]
            firstaid = data[9]
            armor = data[10]
            damage = data[11]
            nitro = data[12]
            mine = data[13]
            gold = data[14]
            battery = data[15]
            turret = data[16]
            hull = data[17]
            rarepaint = data[18]
            epicpaint = data[19]
            legendarypaint = data[20]
            firstaid_msg = ["firstaid", "first", "aid", "first_aid_kit", "first_aid", "firstaidkit", "aid_kit", "repair", "repair_kit", "kit", "repairkit"]
            armor_msg = ["armor", "doublearmor", "double_armor", "double-armor", "armors"]
            damage_msg = ["damage", "doubledamage", "double_damage", "double-damage", "damages"]
            nitro_msg = ["nitro", "nitros", "speed", "speedboost", "speed_boost", "speed-boost"]
            mine_msg = ["mine", "mines"]
            gold_msg = ["gold", "golds", "goldbox", "gold_box", "gold-box", "goldboxes", "gold_boxes", "gold-boxes"]
            battery_msg = ["battery", "batteries"]
            turret_msg = ["turret", "turrets", "xtturets", "turretsxt", "turrets_xt", "turrets-xt", "xt_turrets", "xt-turrets", "xtturet", "turretxt", "turret_xt", "turret-xt", "xt_turret", "xt-turret"]
            hull_msg = ["hull", "hulls", "xthulls", "hullsxt", "hulls_xt", "hulls-xt", "xt_hulls", "xt-hulls", "xthull", "hullxt", "hull_xt", "hull-xt", "xt_hull", "xt-hull"]
            rarepaint_msg = ["rare", "rarepaint", "rarepaints", "rarepaint", "rare_paints", "rare-paints", "rare_paint", "rare-paint", "paintrare", "paintsrare", "paint-rare", "paints-rare", "paint_rare", "paints_rare"]
            epicpaint_msg = ["epic", "epicpaint", "epicpaints", "epicpaint", "epic_paints", "epic-paints", "epic_paint", "epic-paint", "paintepic", "paintsepic", "paint-epic", "paints-epic", "paint_epic", "paints_epic"]
            legendarypaint_msg = ["legendary", "legend", "legendarypaint", "legendarypaints", "legendarypaint", "legendary_paints", "legendary-paints", "legendary_paint", "legendary-paint", "paintlegendary", "paintslegendary", "paint-legendary", "paints-legendary", "paint_legendary", "paints_legendary"]

            if item in firstaid_msg:
                if amount is None:
                    amount = firstaid
                coinsamount = amount * 30
                if firstaid <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > firstaid:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = firstaid - :firstaid WHERE id = :id",
                            {'firstaid': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Repair Kits for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item == "paints":
                lol = rarepaint+epicpaint+legendarypaint
                rprice = random.randint(9999, 15001)
                eprice = random.randint(49999, 90001)
                lprice = random.randint(124999, 200001)
                rarep = rarepaint * rprice
                epicp = epicpaint * eprice
                legendp = legendarypaint * lprice
                allitems = rarep + epicp + legendp
                if lol <= 0:
                    embed=discord.Embed(title="{}, you don't have any paints to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET rarepaint = :rarepaint WHERE id = :id",
                        {'rarepaint': 0, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET epicpaint = :epicpaint WHERE id = :id",
                        {'epicpaint': 0, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET legendarypaint = :legendarypaint WHERE id = :id",
                        {'legendarypaint': 0, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                        {'coins': allitems, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                embed=discord.Embed(title="{}, you have successfully sold {} paints for {:,} crystals!".format(ctx.message.author.display_name, lol, allitems), color=0x00ffff)
                return await self.bot.say(embed=embed)


            elif item == "supplies":
                lol = armor+damage+nitro+mine+gold+battery
                allsupplies = armor * 20 + damage * 20 + nitro * 20 + mine * 20
                god = gold * 850
                firstkit = firstaid * 30
                batt = battery * 125
                allitems = allsupplies + firstkit + god + batt
                if lol <= 0:
                    embed=discord.Embed(title="{}, you don't have anything to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = :armor WHERE id = :id",
                            {'armor': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = :damage WHERE id = :id",
                            {'damage': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = :nitro WHERE id = :id",
                            {'nitro': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = :mine WHERE id = :id",
                            {'mine': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET gold = :gold WHERE id = :id",
                            {'gold': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = :firstaid WHERE id = :id",
                            {'firstaid': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = :battery WHERE id = :id",
                            {'battery': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': allitems, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} supplies for {:,} crystals!".format(ctx.message.author.display_name, lol, allitems), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item == "all":
                lol = armor+damage+nitro+mine+gold+firstaid+battery+turret+hull+rarepaint+epicpaint+legendarypaint
                allsupplies = armor * 20 + damage * 20 + nitro * 20 + mine * 20
                god = gold * 850
                firstkit = firstaid * 30
                batt = battery * 125
                turhul = turret * 500000
                turhul1 = hull * 500000
                rprice = random.randint(9999, 15001)
                eprice = random.randint(49999, 90001)
                lprice = random.randint(124999, 200001)
                rarep = rarepaint * rprice
                epicp = epicpaint * eprice
                legendp = legendarypaint * lprice
                allitems = allsupplies + firstkit + god + batt + turhul + turhul1 + rarep + epicp + legendp
                if lol <= 0:
                    embed=discord.Embed(title="{}, you don't have anything to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = :armor WHERE id = :id",
                            {'armor': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = :damage WHERE id = :id",
                            {'damage': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = :nitro WHERE id = :id",
                            {'nitro': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = :mine WHERE id = :id",
                            {'mine': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET gold = :gold WHERE id = :id",
                            {'gold': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = :firstaid WHERE id = :id",
                            {'firstaid': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = :battery WHERE id = :id",
                            {'battery': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET turret = :turret WHERE id = :id",
                            {'turret': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET hull = :hull WHERE id = :id",
                            {'hull': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET rarepaint = :rarepaint WHERE id = :id",
                            {'rarepaint': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET epicpaint = :epicpaint WHERE id = :id",
                            {'epicpaint': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET legendarypaint = :legendarypaint WHERE id = :id",
                            {'legendarypaint': 0, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': allitems, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} items for {:,} crystals!".format(ctx.message.author.display_name, lol, allitems), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in armor_msg:
                if amount is None:
                    amount = armor
                coinsamount = amount * 20
                if armor <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > armor:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = armor - :armor WHERE id = :id",
                            {'armor': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Double Armors for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in nitro_msg:
                if amount is None:
                    amount = nitro
                coinsamount = amount * 20
                if nitro <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > nitro:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = nitro - :nitro WHERE id = :id",
                            {'nitro': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Speed Boosts for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in damage_msg:
                if amount is None:
                    amount = damage
                coinsamount = amount * 20
                if damage <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > damage:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = damage - :damage WHERE id = :id",
                            {'damage': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Double Damages for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in mine_msg:
                if amount is None:
                    amount = mine
                coinsamount = amount * 20
                if mine <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > mine:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = mine - :mine WHERE id = :id",
                            {'mine': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Mines for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in gold_msg:
                if amount is None:
                    amount = gold
                coinsamount = amount * 850
                if gold <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > gold:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET gold = gold - :gold WHERE id = :id",
                            {'gold': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Golds for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in battery_msg:
                if amount is None:
                    amount = battery
                coinsamount = amount * 125
                if battery <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > battery:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = battery - :battery WHERE id = :id",
                            {'battery': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Batteries for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in turret_msg:
                if amount is None:
                    amount = turret
                coinsamount = amount * 500000
                if turret <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > turret:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET turret = turret - :turret WHERE id = :id",
                            {'turret': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} XT Turret for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in hull_msg:
                if amount is None:
                    amount = hull
                coinsamount = amount * 500000
                if hull <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > hull:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET hull = hull - :hull WHERE id = :id",
                            {'hull': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} XT Hull for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in rarepaint_msg:
                if amount is None:
                    amount = rarepaint
                price = random.randint(9999, 15001)
                coinsamount = amount * price
                if rarepaint <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > rarepaint:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET rarepaint = rarepaint - :rarepaint WHERE id = :id",
                            {'rarepaint': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Rare Paints for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in epicpaint_msg:
                if amount is None:
                    amount = epicpaint
                price = random.randint(49999, 90001)
                coinsamount = amount * price
                if epicpaint <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > epicpaint:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET epicpaint = epicpaint - :epicpaint WHERE id = :id",
                            {'epicpaint': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Epic Paints for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)
            elif item in legendarypaint_msg:
                if amount is None:
                    amount = legendarypaint
                price = random.randint(124999, 200001)
                coinsamount = amount * price
                if legendarypaint <= 0:
                    embed=discord.Embed(title="{}, you don't have any of this item to sell.".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                elif amount > legendarypaint:
                    embed=discord.Embed(title="{}, you do not have that much of this item to sell. ".format(ctx.message.author.display_name), color=0x00ffff)
                    return await self.bot.say(embed=embed)
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET legendarypaint = legendarypaint - :legendarypaint WHERE id = :id",
                            {'legendarypaint': amount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': coinsamount, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    embed=discord.Embed(title="{}, you have successfully sold {} Legendary Paints for {:,} crystals!".format(ctx.message.author.display_name, amount, coinsamount), color=0x00ffff)
                    return await self.bot.say(embed=embed)

            # if item < 0:
        except:
            await self.bot.say(":x: An error occurred while executing the command.")




    @commands.command(pass_context=True, aliases=['inv'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def inventory(self, ctx):
        if cm.contains(Commands.command == 'inventory'):
            cm.update(increment('usage'), Commands.command == 'inventory')
        else:
            cm.insert({'command': "inventory", 'usage': 1})
        try:
            data = await checks.database_container_check(self, ctx.message.author.id)
            if data is None:
                embed=discord.Embed(title="You are not registered!\nUse `>register`", color=0x00ffff)
                return await self.bot.say(embed=embed)
            dataa = await checks.database_check(self, ctx.message.author.id)
            lvl = dataa[3]
            for rank in ranks[lvl]:
                nextRank = ranks[lvl]["next"]
                nextXp = ranks[lvl]["xp_next"]
                image = ranks[lvl]["image"]
                premium_image = ranks[lvl]["premium_image"]
            xp = dataa[1]
            containers = dataa[8]
            rank = dataa[6]
            redcry = dataa[15]
            next = nextXp - xp
            premium = dataa[5]
            coins = dataa[7]
            firstaid = data[9]
            armor = data[10]
            damage = data[11]
            naame = dataa[2]
            nitro = data[12]
            mine = data[13]
            gold = data[14]
            battery = data[15]
            turret = data[16]
            hull = data[17]
            rarepaint = data[18]
            epicpaint = data[19]
            legendarypaint = data[20]
            clancheck = await checks.clan_check(self, ctx.message.author.id)
            if clancheck is None:
                tagClan = "   ‍   "
            else:
                tagClan = clancheck[4]
                tagClan = f"[{tagClan}]"
            if premium == "Yes":
                img = premium_image
                clr = 0xffff00
            else:
                img = image
                clr = 0x00ffff
            embed=discord.Embed(title=f"Displaying {tagClan} {naame} profile",url="https://discord.gg/pXjDfHF", color=clr)
            # embed.add_field(name=f"{ctx.message.author.display_name}", value="\u200b", inline=False)
            embed.add_field(name="__Profile__", value="**Rank:** {}\n**Crystals:** {:,}\n**Red Crystals:** {:,}\n**Containers:** {:,}\n**Experience:** {:,}\n{:,}xp left".format(lvl, coins, redcry, containers, xp, next))
            embed.add_field(name="__Supplies__", value="**Repair kit** {:,}\n**Double armor:** {:,}\n**Double damage:** {:,}\n**Nitro:** {:,}\n**Mine:** {:,}\n**Golds:** {:,}\n**Batteries:** {:,}".format(firstaid,armor,damage,nitro,mine,gold,battery))
            embed.add_field(name="__Paints__", value="**Rare paints** {:,}\n**Epic paints** {:,}\n**Legendary paints** {:,}".format(rarepaint,epicpaint,legendarypaint))
            embed.add_field(name="__Exotic items__", value="**XT Turrets** {:,}\n**XT Hulls** {:,}".format(turret,hull))
            embed.set_thumbnail(url=img)
            # await self.bot.say("Crystals: {}, First Aid: {}, Double Armor: {}, Double Damage: {}, Nitro: {}, Mines: {}, Golds: {}, Batteries: {}, XT Turrets: {}, XT Hulls: {}, Rare Paints: {}, Epic Paints: {}, Legendary Paints: {}".format(coins, firstaid,armor,damage,nitro,mine,gold,battery,turret,hull,rarepaint,epicpaint,legendarypaint))
            return await self.bot.say(embed=embed)
        except:
            await self.bot.say(":x: An error occurred while executing the command.")

    @commands.command(pass_context=True, aliases=['открыть'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def open(self, ctx):
        if cm.contains(Commands.command == 'containers'):
            cm.update(increment('usage'), Commands.command == 'containers')
        else:
            cm.insert({'command': "containers", 'usage': 1})
        try:
            containeradd() ## Doulevei mono me ta 2 teleftea lines
            probabilities = [0.46,0.26,0.15,0.09,0.03,0.01]
            # if ctx.message.author.id == "175680857569230848":
            #     probabilities = [0.01,0.26,0.15,0.09,0.03,0.46]
            rarity = numpy.random.choice(list(item_list.keys()), p=probabilities)
            numb = random.randint(0, 20)
            if numb == 13:
                tips = random.choice(["Did you know that you can get banned for using auto typers to open containers?",
                                    "Did you know that you can get free premium account, loads of crystals/red crystals and containers by using `>rewards` command?",
                                    "You can sell items you obtain from containers using `>container sell all` and earn more crystals!",
                                    "Did you know an XT item costs 500k Crystals?",
                                    "Did you know that preimum account gives you double crystals on rank up and when using `>daily`, `>hourly`, `>rewards` commands. Don't forget double XP! Thats also important!",
                                    "Join the Support server to follow bot status and updates! I've heard they also do giveaways! What are you waiting for? Get an invite link to the server using `>info` command",
                                    "Check out our website! www.tankionlinebot.com"])
                embed=discord.Embed(title="Handy Tips!",description=tips, color=0x00ffff)
                await self.bot.say(embed=embed)
            item = random.choice(list(item_list[rarity].keys()))
            dataa = await checks.database_check(self, ctx.message.author.id)
            if dataa is None:
                embed=discord.Embed(title="{}, you are not registered!\nUse `>register`".format(ctx.message.author.display_name), color=0x00ffff)
                return await self.bot.say(embed=embed)
            premium = dataa[5]
            containers = dataa[8]
            customnick = dataa[2]
            if containers < 1:
                embed=discord.Embed(title="{}, you do not have any containers!\n**Use:** `>buy <amount>`".format(customnick), color=0x00ffff)
                return await self.bot.say(embed=embed)
            data = await checks.database_container_check(self, ctx.message.author.id)
            common_item = data[3] + 1
            amount = data[2] + 1
            uncommon_item = data[4] + 1
            rare_item = data[5] + 1
            epic_item = data[6] + 1
            legendary_item = data[7] + 1
            exotic_item = data[8] + 1
            # print(rarity)
            # print(item)
            # print(item_list[rarity][item])
            # print(item_list[rarity][item]['xp'])
            # print(item_list[rarity][item]['image'])
            turrets = ["Firebird <:Icon_XT_skin:545734382682636288>", "Smoky <:Icon_XT_skin:545734382682636288>", "Thunder <:Icon_XT_skin:545734382682636288>", "Railgun <:Icon_XT_skin:545734382682636288>", "Vulcan <:Icon_XT_skin:545734382682636288>", "Freeze <:Icon_XT_skin:545734382682636288>", "Shaft <:Icon_XT_skin:545734382682636288>", "Twins <:Icon_XT_skin:545734382682636288>", "Isida <:Icon_XT_skin:545734382682636288>", "Ricochet <:Icon_XT_skin:545734382682636288>"]
            hulls = ["Wasp <:Icon_XT_skin:545734382682636288>", "Titan <:Icon_XT_skin:545734382682636288>", "Viking <:Icon_XT_skin:545734382682636288>", "Hornet <:Icon_XT_skin:545734382682636288>", "Mammoth <:Icon_XT_skin:545734382682636288>", "Dictator <:Icon_XT_skin:545734382682636288>"]
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE containers SET amount = :amount WHERE id = :id",
                    {'amount': amount, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET containers = containers - :containers WHERE id = :id",
                    {'containers': 1, 'id': ctx.message.author.id})
                await db.commit()
                await cursor.close()
            if item in list(item_list["a common"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET common = :common WHERE id = :id",
                        {'common': common_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "125 Double Armor":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = armor + :armor WHERE id = :id",
                            {'armor': 125, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "125 Double Damage":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = damage + :damage WHERE id = :id",
                            {'damage': 125, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "125 Speed Boost":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = nitro + :nitro WHERE id = :id",
                            {'nitro': 125, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "125 Mine":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = mine + :mine WHERE id = :id",
                            {'mine': 125, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "3,500 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 3500, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            elif item in list(item_list["an uncommon"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET uncommon = :uncommon WHERE id = :id",
                        {'uncommon': uncommon_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "125 Repair Kits":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = firstaid + :firstaid WHERE id = :id",
                            {'firstaid': 125, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "50 Batteries":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = battery + :battery WHERE id = :id",
                            {'battery': 50, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "10,000 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 10000, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "100 of all Supplies":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = firstaid + :firstaid WHERE id = :id",
                            {'firstaid': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = armor + :armor WHERE id = :id",
                            {'armor': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = damage + :damage WHERE id = :id",
                            {'damage': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = nitro + :nitro WHERE id = :id",
                            {'nitro': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = mine + :mine WHERE id = :id",
                            {'mine': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = battery + :battery WHERE id = :id",
                            {'battery': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "5 Gold Boxes":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET gold = gold + :gold WHERE id = :id",
                            {'gold': 5, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            elif item in list(item_list["a rare"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET rare = :rare WHERE id = :id",
                        {'rare': rare_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "10 Gold Boxes":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET gold = gold + :gold WHERE id = :id",
                            {'gold': 10, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "25,000 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 25000, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "250 of all Supplies":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET firstaid = firstaid + :firstaid WHERE id = :id",
                            {'firstaid': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET armor = armor + :armor WHERE id = :id",
                            {'armor': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET damage = damage + :damage WHERE id = :id",
                            {'damage': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET nitro = nitro + :nitro WHERE id = :id",
                            {'nitro': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET mine = mine + :mine WHERE id = :id",
                            {'mine': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "150 Batteries":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET battery = battery + :battery WHERE id = :id",
                            {'battery': 150, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item in item_list["a rare"]:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET rarepaint = rarepaint + :rarepaint WHERE id = :id",
                            {'rarepaint': 1, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            elif item in list(item_list["an epic"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET epic = :epic WHERE id = :id",
                        {'epic': epic_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "100,000 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 100000, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "100 Red Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                            {'redcrystals': 100, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item in item_list["an epic"]:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET epicpaint = epicpaint + :epicpaint WHERE id = :id",
                            {'epicpaint': 1, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            elif item in list(item_list["a legendary"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET legendary = :legendary WHERE id = :id",
                        {'legendary': legendary_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "300,000 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 300000, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "250 Red Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                            {'redcrystals': 250, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item in item_list["a legendary"]:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET legendarypaint = legendarypaint + :legendarypaint WHERE id = :id",
                            {'legendarypaint': 1, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            elif item in list(item_list["an exotic"]):
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE containers SET exotic = :exotic WHERE id = :id",
                        {'exotic': exotic_item, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if premium == "Yes":
                    asd = item_list[rarity][item]['xp'] * 2
                else:
                    asd = item_list[rarity][item]['xp']
                async with aiosqlite.connect('database.db') as db:
                    cursor = await db.execute("UPDATE users SET xp = xp + :common WHERE id = :id",
                        {'common': asd, 'id': ctx.message.author.id})
                    await db.commit()
                    await cursor.close()
                if item == "1,000,000 Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                            {'coins': 1000000, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item == "500 Red Crystals":
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                            {'redcrystals': 500, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                elif item in turrets:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET turret = turret + :turret WHERE id = :id",
                            {'turret': 1, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
                else:
                    async with aiosqlite.connect('database.db') as db:
                        cursor = await db.execute("UPDATE containers SET hull = hull + :hull WHERE id = :id",
                            {'hull': 1, 'id': ctx.message.author.id})
                        await db.commit()
                        await cursor.close()
            clancheck = await checks.clan_check(self, ctx.message.author.id)
            if clancheck is None:
                tagClan = "   ‍   "
            else:
                tagClan = clancheck[4]
                tagClan = f"[{tagClan}]"
            amount = data[2]
            embed=discord.Embed(title="Tanki Online", url="https://discordbots.org/bot/408439037771382794", description="**You found {} item:** {}".format(rarity, item), color=colors[rarity])
            embed.set_thumbnail(url=item_list[rarity][item]['image'])
            member = ctx.message.author
            amount = amount + 1
            embed.set_footer(text="| {} {}    ‍      ‍      ‍      ‍      ‍   +{:,}xp".format(tagClan, customnick, asd), icon_url=f"{member.avatar_url}")
            return await self.bot.say(embed=embed)
        except:
            await self.bot.say(":x: An error occurred while executing the command.")

    # @container.command(pass_context = True, aliases=['leaderboard', 'lb'])
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def top(self, ctx):
    #     await self.bot.say(":x: **| This command has been removed in the latest update!** There were too many unnecessary leaderboards so I decided to keep just one. `>leaderboard`")
        # async with aiosqlite.connect('database.db') as db:
        #     cursor = await db.execute('SELECT * FROM containers ORDER BY amount DESC')
        #     allusers = await cursor.fetchall()
        #     await cursor.close()
        # counter = 0
        # place = []
        # for i in allusers:
        #     counter += 1
        #     if i[0] == ctx.message.author.id:
        #         place.append(counter)
        # counter = 0
        # embed = discord.Embed(title="Most containers opened!", colour=discord.Colour(0x42d9f4), url="https://discord.gg/qBHXyWd")
        # for i in allusers[:10]:
        #     counter += 1
        #     embed.add_field(name=f"{counter}. {i[1]}", value=f"Containers: {i[2]:,}",inline=False)
        # embed.set_footer(text=f"Your place is {place[0]}")
        # await self.bot.say(embed=embed)


    # @container.command(pass_context = True, aliases=['leaderboard', 'lb'])
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def top(self, ctx):
    #     try:
    #         data = []              #blank list
    #         async with aiosqlite.connect('database.db') as db:
    #             cursor = await db.execute('SELECT * FROM containers')
    #             dataa = await cursor.fetchall()
    #             await cursor.close()
    #         for asd in dataa:
    #             data.append([asd[2], asd[1]])
    #         data = sorted(data, key=lambda x: x[0])[::-1]
    #         embed = discord.Embed(title="Most containers opened!", colour=discord.Colour(0x42d9f4), url="https://discord.gg/qBHXyWd", timestamp=datetime.datetime.utcnow())
    #         embed.set_thumbnail(url="https://i.imgur.com/4SKYtfq.png")
    #         embed.set_author(name="Leaderboard", url="https://discordapp.com", icon_url="https://i.imgur.com/4SKYtfq.png")
    #         embed.set_footer(text="Tanki Online", icon_url="https://i.imgur.com/4SKYtfq.png")
    #         xp = data[0][0]
    #         id = data[0][1]
    #         embed.add_field(name=":first_place: **{}**".format(id), value="   ‍    ‍      ‍    ‍      ‍      ‍       {:,} containers".format(xp), inline = False)
    #         xp = data[1][0]
    #         id = data[1][1]
    #         embed.add_field(name=":second_place: **{}**".format(id), value="   ‍    ‍      ‍    ‍      ‍      ‍       {:,} containers".format(xp), inline = False)
    #         xp = data[2][0]
    #         id = data[2][1]
    #         embed.add_field(name=":third_place: **{}**".format(id), value="   ‍      ‍      ‍   ‍      ‍      ‍      {:,} containers".format(xp), inline = False)
    #         xp = data[3][0]
    #         id = data[3][1]
    #         embed.add_field(name="   ‍   4. {}".format(id), value="   ‍      ‍      ‍     ‍       ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[4][0]
    #         id = data[4][1]
    #         embed.add_field(name="   ‍   5. {}".format(id), value="   ‍      ‍      ‍      ‍      ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[5][0]
    #         id = data[5][1]
    #         embed.add_field(name="   ‍   6. {}".format(id), value="   ‍      ‍      ‍     ‍       ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[6][0]
    #         id = data[6][1]
    #         embed.add_field(name="   ‍   7. {}".format(id), value="   ‍      ‍      ‍      ‍      ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[7][0]
    #         id = data[7][1]
    #         embed.add_field(name="   ‍   8. {}".format(id), value="   ‍      ‍      ‍       ‍     ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[8][0]
    #         id = data[8][1]
    #         embed.add_field(name="   ‍   9. {}".format(id), value="   ‍      ‍        ‍    ‍      ‍   {:,} containers".format(xp), inline = False)
    #         xp = data[9][0]
    #         id = data[9][1]
    #         embed.add_field(name="   ‍   10. {}".format(id), value="   ‍      ‍      ‍     ‍       ‍   {:,} containers".format(xp), inline = False)
    #         data.clear()
    #         await self.bot.say(embed=embed)
    #     except:
    #         await self.bot.say(":x: An error occurred while executing the command.")



def setup(bot):
    bot.add_cog(Containers(bot))
