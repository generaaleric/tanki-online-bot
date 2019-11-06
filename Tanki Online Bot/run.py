import asyncio
import aiohttp
import discord
import sys
import datetime
import json
import threading
from data import config
from data.checks import owner_only, blacklist_check
import traceback
import requests
import time
sys.path.insert(0, "cogs")
from discord.ext import commands
import discord.enums
import logging
from discord import ChannelType
from tinydb.operations import delete,increment
from discord.ext.commands import CommandNotFound
import os
import psutil
import traceback


tu = datetime.datetime.now()
bot = commands.Bot(command_prefix=">")
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged in!')
    print("Starting up...")
    cogs = ["tanki",
			"economy",
            "containers",
			"DiscordBotsOrgAPI",
			"help",
            "general",
            "admin",
            "clans",
            "shop"]
    for cog in cogs:
        bot.load_extension(cog)
        print(f"- {cog} has been loaded.")

async def my_background_task():
    await bot.wait_until_ready()
    print("Starting up...")
    cogs = ["tanki",
			"economy",
            "containers",
			"DiscordBotsOrgAPI",
			"help",
            "general",
            "admin",
            "clans"]
    for cog in cogs:
        bot.load_extension(cog)
        print(f"- {cog} has been loaded.")
    print('------')


async def status_task():
    await bot.wait_until_ready()
    while True:
        sum = 0
        servers = bot.servers
        for server in servers:
            sum += server.member_count
        serversin = (len(bot.servers))
        await bot.change_presence(game=discord.Game(name=">help | By Blload", type=2))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name="{:,} users | {:,} servers".format(sum, serversin), type=3))
        await asyncio.sleep(10)



class Bot(commands.Bot):
    def run(self, *args, cooldown_info_path="cd.pkl", **kwargs):
        import os, pickle

        if os.path.exists(cooldown_info_path):  # on the initial run where "cd.pkl" file hadn't been created yet
            with open(cooldown_info_path, 'rb') as f:
                d = pickle.load(f)
                for name, func in self.commands.items():
                    if name in d:  # if the Command name has a CooldownMapping stored in file, override _bucket
                        self.commands[name]._buckets = d[name]
        try:
            super().run(*args, **kwargs)
        finally:
            with open(cooldown_info_path, 'wb') as f:
                # dumps a dict of command name to CooldownMapping mapping
                pickle.dump({name: func._buckets for name, func in self.commands.items()}, f)


@bot.event
async def on_server_join(server):
    channel = bot.get_channel("452212542517805066")
    embed=discord.Embed(title="Tanki Online", url="https://discordbots.org/bot/408439037771382794", description="**The bot has just joined a new server! :tada:**\n **Server name:** {}\n **Total members:** {:,}\n**Server Owner:** {}".format(server.name,len(server.members),server.owner), color=0x53f442)
    embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
    return await bot.send_message(channel, embed=embed)

@bot.event
async def on_server_remove(server):
    channel = bot.get_channel("452212542517805066")
    embed=discord.Embed(title="Tanki Online", url="https://discordbots.org/bot/408439037771382794", description="**The bot has just left a server! :cry:**\n **Server name:** {}\n **Total members:** {:,}\n**Server Owner:** {}".format(server.name,len(server.members), server.owner), color=0xff0000)
    embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
    return await bot.send_message(channel, embed=embed)




@bot.command(pass_context = True)
@owner_only()
async def status(ctx, command = None):
	cpu = round(psutil.cpu_percent())
	ram = round(psutil.virtual_memory()[2])
	await bot.say("**Using** `{}%` **CPU**\n**Using** `{}%` **RAM**".format(cpu, ram))


@bot.command(pass_context=True)
@owner_only()
async def say(ctx, *, args):
    await bot.delete_message(ctx.message)
    return await bot.say(args)


@bot.command(pass_context=True)
@commands.cooldown(1, 3, commands.BucketType.user)
@blacklist_check()
async def ping(ctx):
    t1 = time.perf_counter()
    await bot.send_typing(ctx.message.channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title=":ping_pong: {}ms".format(round((t2-t1)*1000)), color=0x00ffff)
    await bot.say(embed=embed)
    if cm.contains(Commands.command == 'ping'):
        cm.update(increment('usage'), Commands.command == 'ping')

    else:
        cm.insert({'command': "ping", 'usage': 1})




@bot.command(pass_context = True)
@commands.cooldown(1, 5, commands.BucketType.user)
@blacklist_check()
async def uptime(ctx):
    global tu
    await bot.say(timedelta_str(datetime.datetime.now() - tu))
    if cm.contains(Commands.command == 'uptime'):
        cm.update(increment('usage'), Commands.command == 'uptime')

    else:
        cm.insert({'command': "uptime", 'usage': 1})


def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)



@bot.command()
@owner_only()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
@owner_only()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@bot.command()
@owner_only()
async def reload(extension_name : str):
    """Reloads an extension."""
    bot.unload_extension(extension_name)
    bot.load_extension(extension_name)
    await bot.say("{} reloaded.".format(extension_name))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(error, ctx):
    print(error)
    error = getattr(error, 'original', error)
    print(error)
    channel = ctx.message.channel
#     if isinstance(error, CommandNotFound):
#         msg = await bot.send_message(ctx.message.channel, f"Command `{ctx.message.content}` not found.")
#         await asyncio.sleep(3)
#         await bot.delete_message(msg)
    if isinstance(error, commands.CommandOnCooldown):
        time = error.retry_after
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        x = await bot.send_message(ctx.message.channel, content="**You can use the command again in %d hours, %d minutes, and %d seconds**" % (hour, minutes, seconds))
        await asyncio.sleep(3)
        await bot.delete_message(x)
    if isinstance(error, commands.CheckFailure):
        await bot.send_message(channel, "**|:exclamation:|  You dont have permission to use this command!**")

#bot.loop.create_task(status_task())
#bot.loop.create_task(my_background_task())
bot.run(config.token)
