import discord, config, datetime, math, os, asyncio
from discord.ext import commands
from bot import db

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, aliases=["botinfo"])
    async def bot(self, ctx):

        timestamp = datetime.datetime.timestamp(datetime.datetime.now())
        uptime = timestamp - config.starttime

        if uptime < 60:
            uptime_format = str(math.trunc(uptime)) + " seconds"
        elif uptime < 3600:
            uptime_format = str(math.trunc(uptime / 60)) + " minute/s"
        else:
            uptime_format = str(math.trunc(uptime / 3600)) + " hour/s"


        embed=discord.Embed(title="Bot Information", description=f"Made by @CriticalToxic#1137")
        embed.add_field(name="Uptime", value=uptime_format, inline=True)
        embed.add_field(name="Ping", value=f"{str(round(self.bot.latency*1000))} ms", inline=True)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)

        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def help(self, ctx):
        prefix = db.get("servers", ctx.guild.id)["prefix"]
        embed=discord.Embed(title="__**Command List**__", description="List of Commands")
        if ctx.author.id in config.devs:
            embed.add_field(name="__Developers__", value=f"{prefix}listcog\n{prefix}load (cog)\n{prefix}unload (cog)\n{prefix}reload (all/cog)\n{prefix}reboot <TURNS BOT OFF>\n", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="__General__", value=f"{prefix}user *(Tag User*)\n{prefix}scorebreakdown *(Tag User)*\n{prefix}bot", inline=True)
        embed.add_field(name="__Wynncraft__", value=f"{prefix}wstats *(Player)*\n{prefix}wclasses *(Player) [#]*", inline=True)
        embed.add_field(name="__Pokémon__", value=f"{prefix}pokemon (name/ID) [shiny/not]", inline=True)
        embed.add_field(name="__Music__", value=f"{prefix}play *(URL/ Search Term*)\n{prefix}skip\n{prefix}join\n{prefix}remove *(Song #)*\n{prefix}shuffle\n{prefix}queue", inline=False)
        embed.set_footer(text="*Bot created by @Critical_Toxic#1137*")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def user(self, ctx, user: discord.Member=None):
        if user is None:
            await ctx.send("You need to tag a user or yourself.")
        db.add_user(user.id)
        data = db.get("users", user.id)
        embed=discord.Embed()
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)

        totalscore = data["messages"] + data["commands"] + data["attachments"]
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Bot Score", value=totalscore, inline=True)
        #embed.add_field(name="Birthday", value=str(data["brithdate"]), inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["scorebreakdown"])
    async def score(self, ctx, user: discord.Member=None):
        if user == None:
            db.add_user(ctx.author.id)
            data = db.get("users", ctx.author.id)
        else:
            db.add_user(user.id)
            data = db.get("users", user.id)
        embed=discord.Embed()
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)

        totalscore = data["messages"] + data["commands"] + data["attachments"]
        embed.add_field(name="__**Total Score**__", value=totalscore, inline=False)
        embed.add_field(name="Messages", value=data["messages"], inline=True)
        embed.add_field(name="Commands", value=data["commands"], inline=True)
        embed.add_field(name="Attachments", value=data["attachments"], inline=True)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def reboot(self, ctx):

        if ctx.author.id in config.devs:
            await self.bot.change_presence(status=discord.Status.do_not_disturb)
            await ctx.send("Rebooting...")
            await asyncio.sleep(5)
            os.system("reboot")


def setup(bot):
    bot.add_cog(General(bot))