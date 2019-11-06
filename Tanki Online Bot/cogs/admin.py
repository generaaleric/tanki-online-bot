import discord
import json
import time
import asyncio
import aiosqlite
from discord.ext import commands
import data.checks as checks
from data.checks import blacklist_check
from tinydb import TinyDB, Query
from tinydb import where
from tinydb.operations import delete
from economy import get_sec
from general import ConvertSectoDay

cm = TinyDB('data/blacklist.json')
Commands = Query()


class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def reset_user(self, ctx, user: discord.Member):
        data = await checks.database_check(self, user.id)
        if data is None:
            embed=discord.Embed(title="{}, they are not registered!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        await checks.delete_user(self, user.id)
        await checks.add_user(self, user.id, user.display_name)
        embed=discord.Embed(title="{} has been reseted!".format(user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def ban_user(self, ctx, user: discord.Member):
        data = await checks.database_check(self, user.id)
        if data is None:
        	embed=discord.Embed(title="{}, they are not registered!".format(ctx.message.author.display_name), color=0x00ffff)
        	return await self.bot.say(embed=embed)
        await checks.delete_user(self, user.id)
        await checks.ban_check(self, user.id, user.display_name)
        embed=discord.Embed(title="{} has been banned!".format(user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def unban_user(self, ctx, user: discord.Member):
        data = await checks.database_check(self, user.id)
        if data is None:
            embed=discord.Embed(title="{}, they are not registered!".format(ctx.message.author.display_name), color=0x00ffff)
            return await self.bot.say(embed=embed)
        await checks.delete_user(self, user.id)
        await checks.unban_check(self, user.id, user.display_name)
        embed=discord.Embed(title="{} has been unbanned!".format(user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def freepremium(self, ctx):
        await self.bot.say("Free premium has ended.".format(ctx.message.author.mention))
        # ts = time.time()
        # data = await checks.database_check(self, ctx.message.author.id)
        # premium = data[5]
        # totaltime, msg = get_sec("1d")
        # totaltime = ts + totaltime
        # if data is None:
        #     return await self.bot.say("{}, you are not registered!\nUse `>register`".format(ctx.message.author.mention))
        # if premium == "Yes":
        #     return await self.bot.say("You are already in premium users.".format(ctx.message.author.mention))
        # async with aiosqlite.connect('database.db') as db:
        #     cursor = await db.execute("UPDATE users SET premleft = :premleft WHERE id = :id",
        #     {'premleft': totaltime, 'id': ctx.message.author.id})
        #     await db.commit()
        #     await cursor.close()
        # async with aiosqlite.connect('database.db') as db:
        #     cursor = await db.execute("UPDATE users SET premium = :premium WHERE id = :id",
        #         {'premium': "Yes", 'id': ctx.message.author.id})
        #     await db.commit()
        #     await cursor.close()
        #     await self.bot.say("**You have obtained 1 day of free account!**\nIf you would like to extend it you can do it with just 1$/ Month. Use `>feedback I would like to extened my premium account` ".format(ctx.message.author.mention))

    @commands.command(pass_context = True)
    @checks.owner_only()
    async def addpremium(self, ctx, user: discord.Member, amount):
        ts = time.time()
        data = await checks.database_check(self, user.id)
        if data is None:
            return await self.bot.say("{}, they are not registered!\nUse `>register`".format(ctx.message.author.mention))
        premium = data[5]
        if premium == "Yes":
            premleft = data[11]
            async with aiosqlite.connect('database.db') as db:
                totaltime, msg = get_sec(amount)
                totaltimee = premleft + totaltime
                cursor = await db.execute("UPDATE users SET premleft = :premleft WHERE id = :id",
                    {'premleft': totaltimee, 'id': user.id})
                await db.commit()
                await cursor.close()
            dff = ConvertSectoDay(int(totaltime))
            return await self.bot.say("**{} Your premium has been increased by {}**".format(user.mention, dff))
        else:
            totaltime, msg = get_sec(amount)
            totaltime = totaltime + ts
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET premium = :premium WHERE id = :id",
                    {'premium': "Yes", 'id': user.id})
                await db.commit()
                await cursor.close()
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET premleft = :premleft WHERE id = :id",
                    {'premleft': totaltime, 'id': user.id})
                await db.commit()
                await cursor.close()
            return await self.bot.say("**Successfully added {} of premium to {}!**".format(msg, user.mention))


    @commands.command(pass_context = True)
    @checks.owner_only()
    async def removepremium(self, ctx, user: discord.Member = None):
        data = await checks.database_check(self, user.id)
        if data is None:
            return await self.bot.say("{}, you are not registered!\nUse `>register`".format(ctx.message.author.mention))
        premium = data[5]
        if premium == "No":
            return await self.bot.say("{} is not in premium users.".format(user.mention))
        else:
            async with aiosqlite.connect('database.db') as db:
                cursor = await db.execute("UPDATE users SET premium = :premium WHERE id = :id",
                    {'premium': "No", 'id': user.id})
                await cursor.close()
                await db.commit()
            return await self.bot.say("{}, has been removed from premium users!".format(user.mention))

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def addcontainer(self, ctx, user: discord.Member, amount: int):
        data = await checks.database_container_check(self, user.id)
        if data is None:
            embed=discord.Embed(title="User is not registered!\nUse `>register`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET containers = containers + :containers WHERE id = :id",
                {'containers': amount, 'id': user.id})
            await db.commit()
            await cursor.close()
        embed=discord.Embed(title="Successfully added {} containers to {} account!".format(amount, user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def addcry(self, ctx, user: discord.Member, amount: int):
        data = await checks.database_container_check(self, user.id)
        if data is None:
            embed=discord.Embed(title="User is not registered!\nUse `>register`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET coins = coins + :coins WHERE id = :id",
                {'coins': amount, 'id': user.id})
            await db.commit()
            await cursor.close()
        embed=discord.Embed(title="Successfully added {:,} crystals to {} account!".format(amount, user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @checks.owner_only()
    async def addredcry(self, ctx, user: discord.Member, amount: int):
        data = await checks.database_container_check(self, user.id)
        if data is None:
            embed=discord.Embed(title="User is not registered!\nUse `>register`", color=0x00ffff)
            return await self.bot.say(embed=embed)
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("UPDATE users SET redcrystals = redcrystals + :redcrystals WHERE id = :id",
                {'redcrystals': amount, 'id': user.id})
            await db.commit()
            await cursor.close()
        embed=discord.Embed(title="Successfully added {:,} red crystals to {} account!".format(amount, user.display_name), color=0x00ffff)
        return await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))
