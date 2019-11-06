import dbl
import discord
from discord.ext import commands
import aiohttp
import asyncio
import logging




class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQwODQzOTAzNzc3MTM4Mjc5NCIsImJvdCI6dHJ1ZSwiaWF0IjoxNTI1NjE4NDQxfQ.xuhOXbpC6ToW8qZsrBs0iot3J_eanseNdWxFpN2qHvE'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, loop=bot.loop)
        self.bot.loop.create_task(self.update_stats())

    def owner_only():
        def predicate(ctx):
            return ctx.message.author.id == "175680857569230848"
        return commands.check(predicate)

    async def update_stats(self):
            while True:
                logger.info('attempting to post server count')
                try:
                    await self.dblpy.post_server_count()
                    logger.info('posted server count ({})'.format(len(self.bot.servers)))
                except Exception as e:
                    logger.exception('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
                await asyncio.sleep(1800)


    # @commands.command(pass_context = True)
    # async def voted(self, ctx, user: discord.Member):
    #     url = "https://discordbots.org/api/bots/408439037771382794/check?userId={}".format(user.id)
    #     async with aiohttp.ClientSession() as session:
    #         headers = {"Authorization": self.token}
    #         async with session.get(url, headers=headers) as resp:
    #             asd = await resp.json()
    #             vote = asd['voted']
    #         if vote == 1:
    #             await self.bot.say('Has voted')
    #         else:
    #             await self.bot.say("Hasn't voted!")

def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))
