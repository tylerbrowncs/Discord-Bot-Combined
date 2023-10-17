import discord, typing

from discord.ext import commands
from bot import db

class Settings(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            #await ctx.send("INSERT SETTINGS HERE")
            serverdata = db.get("servers", ctx.message.guild.id)

            embed = discord.Embed(title=f"{ctx.message.guild.name} Settings",description=str(ctx.message.guild.id), color=0x2bff00)
            embed.add_field(name="Prefix:", value=f"{serverdata['prefix']}settings prefix")
            #embed.add_field(name="DJ Role:", value=f"{serverdata['prefix']}settings djrole")
            #embed.add_field(name="Admin Role:", value=f"{serverdata['prefix']}settings adminrole")
            await ctx.send(embed=embed)

    @settings.command(pass_context=True)
    async def prefix(self, ctx, prefix=None):
        if prefix is None:
            serverdata = db.get("servers", ctx.message.guild.id)
            embed = discord.Embed(title=f"Prefix: `{serverdata['prefix']}`", description="", color=0x2bff00)
        else:
            db.change("servers", ctx.message.guild.id, "prefix", prefix)
            embed = discord.Embed(title=f"Prefix change to `{prefix}`", description="", color=0x2bff00)
        await ctx.send(embed=embed)
            

    @settings.command(pass_context=True)
    async def djrole(self, ctx, role: typing.Union[discord.Role, str] = None):
        if role is None:
            serverdata = db.get("servers", ctx.message.guild.id)
            embed = discord.Embed(title=f"DJ Role: `{serverdata['dj_role']}`", description="", color=0x2bff00)

        elif isinstance(role, discord.Role):
            db.change("servers", ctx.message.guild.id, "dj_role", role.name)
            embed = discord.Embed(title=f"DJ Role change to `{role.name}`", description="", color=0x2bff00)

        else:
            embed = discord.Embed(title="Please tag a role", description="", color=0xff0000)

        await ctx.send(embed=embed)

    @settings.command(pass_context=True)
    async def adminrole(self, ctx, role: typing.Union[discord.Role, str] = None):
        if role is None:
            serverdata = db.get("servers", ctx.message.guild.id)
            embed = discord.Embed(title=f"Admin Role: `{serverdata['admin_role']}`", description="", color=0x2bff00)

        elif isinstance(role, discord.Role):
            db.change("servers", ctx.message.guild.id, "admin_role", role.name)
            embed = discord.Embed(title=f"Admin Role change to `{role.name}`", description="", color=0x2bff00)
        
        else:
            embed = discord.Embed(title="Please tag a role", description="", color=0xff0000)

        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Settings(bot))