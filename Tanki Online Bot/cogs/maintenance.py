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



async def on_message(self, message):
    if message.author.bot:
        return
    server = message.server
    if message.content.upper().startswith(">"):
        if server is None:
            print(f'"{message.author}" used {message.content} commmand in DM.\n--------------------------------------------------------------')
        else:
            await self.bot.send_message(message.channel, ":notepad_spiral: **| Scheduled maintenance** Bot will be back shortly")
            print(f'"{message.author}" used {message.content} commmand in "{message.server.name}" server.\n--------------------------------------------------------------')

def setup(bot):
    bot.add_cog(Maintenance(bot))
