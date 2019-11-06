import discord
from discord.ext import commands
import data.checks as checks
from data.checks import blacklist_check

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(description='>help category', pass_context=True)
    @checks.blacklist_check()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Tanki Online", color=0x00ffff)
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            embed.add_field(name=":gear: General", value=">help general", inline=True)
            embed.add_field(name="💰 Economy", value=">help economy", inline=True)
            embed.add_field(name=":shield: Clan", value=">help clan", inline=True)
            embed.add_field(name="🎮 Tanki Online", value=">help tanki", inline=True)
            embed.set_footer(text="Use >help <command> for more information about a command.")
            await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="general")
    async def _general(self, ctx):
        embed=discord.Embed(title=":gear: General Category", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Commands:", value=">info\n>updates\n>invite\n>credits\n>vote\n>usages\n>reputation", inline=True)
        embed.add_field(name="\u200b", value=">bitcoin\n>owner\n>feedback\n>report", inline=True)
        embed.set_footer(text="Use >help <command> for more information about a command.")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="economy")
    async def _economy(self, ctx):
        embed=discord.Embed(title="💰 Economy Category", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Commands:", value=">profile\n>inventory\n>leaderboard\n>open\n>sell\n>shop\n>buy\n>garage\n>equip\n>battle\n>stats", inline=True)
        embed.add_field(name="\u200b", value=">container stats\n>drop\n>rewards\n>records\n>nickname\n>daily\n>hourly\n>coinflip\n>reset\n>register\n>unregister", inline=True)
        embed.set_footer(text="Use >help <command> for more information about a command.")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="clan")
    async def _clan(self, ctx):
        embed=discord.Embed(title=":shield: Clan Category", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Commands:", value=">clan create\n>clan profile\n>clan leaderboard\n>clan members\n>clan upgrade\n>clan leave\n>clan demote\n>clan promote", inline=True)
        embed.add_field(name="\u200b", value=">clan kick\n>clan invite\n>clan description\n>clan logo\n>clan rename\n>clan delete\n>clan license", inline=True)
        embed.set_footer(text="Use >help clan <command> for more information about a command.")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="tanki", aliases=["tankionline", "to", "tank"])
    async def _tanki(self, ctx):
        embed=discord.Embed(title="🎮 Tanki Online Category", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Commands:", value=">ratings\n>xp\n>supplies\n>stars\n>weekly\n>gamemodes", inline=True)
        embed.add_field(name="\u200b", value=">top crystals\n>top score\n>top golds\n>top efficiency", inline=True)
        embed.set_footer(text="Use >help <command> for more information about a command.")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="clans")
    async def _clans(self, ctx, arg = None):
        if arg is None:
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> clan Command <==```\n**Subcommands:** \n`>clan license`\n`>clan create`\n`>clan profile`\n`>clan members`\n`>clan leave`\n`>clan upgrade`\n`>clan promote`\n`>clan demote`\n`>clan invite`\n`>clan kick`\n`>clan rename`\n`>clan description`\n`>clan logo`\n`>clan delete`\nIf you would to get more information about a command,\nuse `>help clan [subcommand]`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg == "license":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> License Command <==```\n**Description:** With a clan License you can create your own clan!\n**Price:** 1,000 Red Crystals\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="create":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Create Command <==```\n**Description:** Create your own Clan.\n**Requirements:** Clan License. Obtain one using the `>clan license` command.\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="profile":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Profile Command <==```\n**Description:** Will display your clan information or someone else clan if you mention somenoe.\n**Usage:**\n`>clan profile` - View your clan information\n`>clan profile @user` - View other people clan information.\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="members":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Members Command <==```\n**Description:** Will list your clan members by joindate.\nAlong with their personal information (Crystals, Red Crystals, Clan rank etc)**Usage:** `>clan members`\n\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="leave":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Leave Command <==```\n**Description:** Leave your current clan.\nThere's a comfirmation message.\n**Usage:** `>clan leave`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="upgrade":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Upgrade Command <==```\n**Description:** Increase your clan slots!\n**Price:** 500 Red Crystals\n**Usage:** `>clan upgrade`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="promote":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Promote Command <==```\n**Description:** Promote a clan member to Officer rank!\nThere's a comfirmation message.\n**Perks:** A member with Officer rank will be able to invite users to the clan.\n**Usage:** `>clan promote @user`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="demote":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Demote Command <==```\n**Description:** Demote a clan member back to Member rank!\nThere's a comfirmation message.\n**Usage:** `>clan demote @user`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="invite":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Invite Command <==```\n**Description:** Invite a someone to your clan!\nIt wil send an invitation to the user that they must answer in 15 seconds.\n**Usage:** `>clan invite @user`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="logo":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Invite Command <==```\n**Description:** Change your clan logo\n**Usage:** `>logo [Imgur link]`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="kick":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Kick Command <==```\n**Description:** Kick a clan member from your clan!\nThere's a comfirmation message.\n**Usage:** `>clan kick @user`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="rename":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Rename Command <==```\n**Description:** Rename your clan name/tag. The bot will ask you which would you like to rename clan or tag.\n**Price:** 500 Red Crystals\n**Usage:** `>clan rename`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="description":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Description Command <==```\n**Description:** Change your clan Description.\n**Usage:** `>clan description [descritpion]`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)
        elif arg =="delete":
            embed=discord.Embed(title="Tanki Online", url="http://www.tankionlinebot.com", description="```ml\n==> Delete Command <==```\n**Description:** Delete your clan!\nIn order to create a new one you will have to buy another Clan License.\nThere's a comfirmation message.\nOnly clan owner can delete a clan.\n**Usage:** `>clan delete`\n```fix\nRequested by {}```".format(ctx.message.author.display_name))
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            return await self.bot.say(embed=embed)


    @help.command(pass_context=True, name="info")
    async def _info(self, ctx):
        embed=discord.Embed(title="Info command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Info command is very useful as it has links about our support server in case you ever need help with anything, website link and an invite link to invite the bot to your server.\nYou can also check servers/users count.", inline=False)
        embed.add_field(name="Usage:", value=">info", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="updates", aliases=["update"])
    async def _updates(self, ctx):
        embed=discord.Embed(title="Update command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="This command is very useful as it keeps you updated about latest changes.", inline=False)
        embed.add_field(name="Usage:", value=">updates", inline=False)
        embed.add_field(name="Aliases:", value=">update", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="invite")
    async def _invite(self, ctx):
        embed=discord.Embed(title="Invite command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Want to invite the bot to your server?\nRun the command and you will receive an invite link.", inline=False)
        embed.add_field(name="Usage:", value=">invite", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="credits", aliases=["credit"])
    async def _credits(self, ctx):
        embed=discord.Embed(title="Credits command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays a list of users who helped make Tanki Online Bot possible!", inline=False)
        embed.add_field(name="Usage:", value=">credits", inline=False)
        embed.add_field(name="Aliases:", value=">credit", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="vote")
    async def _vote(self, ctx):
        embed=discord.Embed(title="Vote command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Gives you a link to a website where you can vote for Tanki Online Bot and get access to `>rewards` command!\n**Rewards:**\n• 1 Hour of premium account\n• 50,000 Crystals\n• 50 Red Crystals\n •15 Containers\n\nPremium users earn double!\nFor more information about premium accounts use `>premium`", inline=False)
        embed.add_field(name="Usage:", value=">vote", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="bitcoin")
    async def _bitcoin(self, ctx):
        embed=discord.Embed(title="Bitcoin command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="No idea why this command is here but anyway.\nBitcoin command displays the value of 1 Bitcoin in USD", inline=False)
        embed.add_field(name="Usage:", value=">bitcoin", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="usages")
    async def _usages(self, ctx):
        embed=discord.Embed(title="Usages command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Ever wondered how many commands have been executed in total?\nUse it and find out!", inline=False)
        embed.add_field(name="Usage:", value=">usages", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="reputation", aliases=["rep"])
    async def _reputation(self, ctx):
        embed=discord.Embed(title="Reputation command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Award someone with a reputation point!\nFun fact: The more you have, the more famous you are :eyes:", inline=False)
        embed.add_field(name="Usage:", value=">reputation", inline=False)
        embed.add_field(name="Aliases:", value=">rep", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="owner")
    async def _owner(self, ctx):
        embed=discord.Embed(title="Owner command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays information about my owner.", inline=False)
        embed.add_field(name="Usage:", value=">owner", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="feedback")
    async def _feedback(self, ctx):
        embed=discord.Embed(title="Feedback command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Will DM owner your feedback about the bot.\nAbusing it will get you banned from using it!", inline=False)
        embed.add_field(name="Usage:", value=">feedback [text]", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="report")
    async def _report(self, ctx):
        embed=discord.Embed(title="Report command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="You feel like someone is cheating?\nReport him!\nAbusing the command will get you banned from using it!", inline=False)
        embed.add_field(name="Usage:", value=">report [Offender ID ,Reason ,Server Invite ]", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)
#========================================================================#
                #Economy#
#========================================================================#

    @help.command(pass_context=True, name="profile", aliases=["level", "balance", "bal", "p"])
    async def _profile(self, ctx):
        embed=discord.Embed(title="Profile command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays your profile card or someone else if a user is mentioned.", inline=False)
        embed.add_field(name="Usage:", value=">profile @user", inline=False)
        embed.add_field(name="Aliases:", value=">level, >balance, >bal, >p", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="inventory", aliases=["inv"])
    async def _inventory(self, ctx):
        embed=discord.Embed(title="Inventory command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays items obtained from containers!", inline=False)
        embed.add_field(name="Usage:", value=">inventory", inline=False)
        embed.add_field(name="Aliases:", value=">inv", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="leaderboard", aliases=["lb"])
    async def _leaderboard(self, ctx):
        embed=discord.Embed(title="Leaderboard command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays top 10 users with the most crystals owned!\nIt also displays your place at the end of the embed too!", inline=False)
        embed.add_field(name="Usage:", value=">leaderboard", inline=False)
        embed.add_field(name="Aliases:", value=">lb", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="open")
    async def _open(self, ctx):
        embed=discord.Embed(title="Open command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Open containers and obtain items to increase your stats!", inline=False)
        embed.add_field(name="Usage:", value=">open", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="sell")
    async def _sell(self, ctx):
        embed=discord.Embed(title="Sell command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Sell items you obtain from containers to earn crystals!\nYou can sell all items at once using `>sell all` or by category `>sell supplies` or one by one `>sell mines`", inline=False)
        embed.add_field(name="Usage:", value=">sell [item]", inline=False)
        embed.add_field(name="Usage:", value=">sell all", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="container", aliases=["c"])
    async def _container(self, ctx, arg = None):
        if arg == None:
            return
        if arg == "stats":
            embed=discord.Embed(title="Container stats command", color=0x00ffff)
            embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
            embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
            embed.add_field(name="Description:", value="Check how many containers you opened at once and how many you have opened for each rarity.", inline=False)
            embed.add_field(name="Usage:", value=">container stats", inline=False)
            embed.add_field(name="Aliases:", value=">c stats", inline=False)
            embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
            await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="drop")
    async def _drop(self, ctx):
        embed=discord.Embed(title="Drop command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Drop a gold box in a channel.\n The gold box will drop 5 seconds after the `>drop` command the quickest to reply with any text catches the gold box worth of 1,000 crystals!", inline=False)
        embed.add_field(name="Usage:", value=">drop", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="rewards")
    async def _rewards(self, ctx):
        embed=discord.Embed(title="Rewards command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="The command is unlocked after voting for the bot on a website.\nYou can get the website link using `>vote`.\n**Command rewards you with the folowing items per vote:**\n   ‍      ‍   • 1 Hour of premium acount\n   ‍      ‍   • 15 Containers\n   ‍      ‍   • 50,000 Crystals\n   ‍      ‍   • 50 Red Crystals\nPremium users get these rewards double!\nFor more information about premium accounts use `>premium`", inline=False)
        embed.add_field(name="Usage:", value=">rewards", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="records")
    async def _records(self, ctx):
        embed=discord.Embed(title="Records command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays records set by users.\nNo prizes rewarded.\nHave a record you want to submit? DM Blload#6680", inline=False)
        embed.add_field(name="Usage:", value=">records", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="nickname")
    async def _nickname(self, ctx):
        embed=discord.Embed(title="Nickname command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Change your profile nickname with 50 Red Crystals", inline=False)
        embed.add_field(name="Usage:", value=">nickname [NewNickname]", inline=False)
        embed.add_field(name="Example:", value=">nickname Blload", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="daily")
    async def _daily(self, ctx):
        embed=discord.Embed(title="Daily command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Rewards you with 15,000 Crystals every 24 hours.\nPremium users earn double!\nFor more information about premium accounts use `>premium`", inline=False)
        embed.add_field(name="Usage:", value=">daily", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="hourly")
    async def _hourly(self, ctx):
        embed=discord.Embed(title="Hourly command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Rewards you with 5,000 Crystals every 1 hour.\nPremium users earn double!\nFor more information about premium accounts use `>premium`", inline=False)
        embed.add_field(name="Usage:", value=">hourly", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="coinflip")
    async def _coinflip(self, ctx):
        embed=discord.Embed(title="Coinflip command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Want to try your luck in gambling?\nMaximum bet: 500,000 Crystals", inline=False)
        embed.add_field(name="Usage:", value=">coinflip [amount]", inline=False)
        embed.add_field(name="Example:", value=">coinflip 1000", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="shop")
    async def _shop(self, ctx):
        embed=discord.Embed(title="Shop command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays all turrets and hulls you can buy.\nIf you would like to buy an item use `>buy` command\nFor example `>buy Wasp m2`", inline=False)
        embed.add_field(name="Usage:", value=">shop category page", inline=False)
        embed.add_field(name="Example:", value=">shop turrets 2", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="garage")
    async def _garage(self, ctx):
        embed=discord.Embed(title="Garage command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays your bought turrets/hulls and currently equipped combo.", inline=False)
        embed.add_field(name="Usage:", value=">garage", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="equip")
    async def _equip(self, ctx):
        embed=discord.Embed(title="Equip command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Change your equiped turret/hull", inline=False)
        embed.add_field(name="Usage:", value=">equip turret/hull", inline=False)
        embed.add_field(name="Example:", value=">equip Smoky m3", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="battle")
    async def _battle(self, ctx):
        embed=discord.Embed(title="Battle command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="You think you have the best combo?\nBattle with other users and find out!", inline=False)
        embed.add_field(name="Usage:", value=">battle @user", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="stats")
    async def _stats(self, ctx):
        embed=discord.Embed(title="Stats command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Check turret/hull statistcs.\nFor example how many damage a turret does and how much armor a hull has.", inline=False)
        embed.add_field(name="Usage:", value=">stats turret/hull", inline=False)
        embed.add_field(name="Usage:", value=">stats Shaft m2", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="reset")
    async def _reset(self, ctx):
        embed=discord.Embed(title="Reset command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Reset your profile for a fresh start!", inline=False)
        embed.add_field(name="Usage:", value=">reset", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="unregister")
    async def _unregister(self, ctx):
        embed=discord.Embed(title="Unregister command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Unregister from bot.\nNote: It deletes your profile.", inline=False)
        embed.add_field(name="Usage:", value=">unregister", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)
#========================================================================#
                #Tanki Online#
#========================================================================#

    @help.command(pass_context=True, name="ratings")
    async def _ratings(self, ctx):
        embed=discord.Embed(title="Ratings command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Check your in-game statistcs right from discord.\n\n**Tip**\nUse `>set [nickname]` command, this will save your nickname so next tiem you will just have to do `>rating` without adding your nickname.", inline=False)
        embed.add_field(name="Usage:", value=">ratings nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="xp")
    async def _xp(self, ctx):
        embed=discord.Embed(title="Xp command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Same as ratings command but this will show you just your Xp stats.\n\n**Tip**\nUse `>set [nickname]` command, this will save your nickname so next tiem you will just have to do `>xp` without adding your nickname.", inline=False)
        embed.add_field(name="Usage:", value=">xp nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="supplies")
    async def _supplies(self, ctx):
        embed=discord.Embed(title="Supplies command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Check your or someone else total supplies use.\n\n**Tip**\nUse `>set [nickname]` command, this will save your nickname so next tiem you will just have to do `>supplies` without adding your nickname.", inline=False)
        embed.add_field(name="Usage:", value=">supplies nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="stars")
    async def _stars(self, ctx):
        embed=discord.Embed(title="Stars command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Calculate how much time or how many battles are required to earn X amount of stars.\nNote: Time shown is playing Non-stop for an average player.", inline=False)
        embed.add_field(name="Usage:", value=">stars amount", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="weekly")
    async def _weekly(self, ctx):
        embed=discord.Embed(title="Weekly command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays player weekly statistics.\n\n**Tip**\nUse `>set [nickname]` command, this will save your nickname so next tiem you will just have to do `>weekly` without adding your nickname.", inline=False)
        embed.add_field(name="Usage:", value=">weekly nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="gamemodes")
    async def _gamemodes(self, ctx):
        embed=discord.Embed(title="Gamemodes command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="See gamemodes people have played, how many hours the spent on them and how much exp they gained in each gamemode!\n\n**Tip**\nUse `>set [nickname]` command, this will save your nickname so next tiem you will just have to do `>gamemodes` without adding your nickname.", inline=False)
        embed.add_field(name="Usage:", value=">gamemodes nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="top")
    async def _top(self, ctx):
        embed=discord.Embed(title="Top command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Displays top 10 players from each category\n(Crystals, Score, Golds, Efficiency)", inline=False)
        embed.add_field(name="Usage:", value=">top category", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)

    @help.command(pass_context=True, name="set")
    async def _set(self, ctx):
        embed=discord.Embed(title="Set command", color=0x00ffff)
        embed.set_author(name="Tanki Online",url="https://tankionlinebot.com/")
        embed.set_thumbnail(url="https://i.imgur.com/Y3mojRt.png")
        embed.add_field(name="Description:", value="Link your in-game account with discord so next time you want to view your account statistics you have have to type down your in-game nickname", inline=False)
        embed.add_field(name="Usage:", value=">set nickname", inline=False)
        embed.set_footer(text=f"| Requested by {ctx.message.author.display_name}", icon_url=f"{ctx.message.author.avatar_url}")
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
