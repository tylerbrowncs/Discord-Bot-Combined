import discord, config, datetime, math, os, asyncio
from discord.ext import commands
from bot import db


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def leaderboard(self, ctx, sub=None):

        if sub==None:
        
            top = db.leaderboard("users", "messages")

            text = """"""

            for i in top:
                user = await self.bot.fetch_user(i[0])
                text = text + (f"{user.name} - {str(i[1])} message/s\n")

            embed = discord.Embed(title="Leaderboard")
            embed.add_field(name="Messages sent", value=text)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboard(bot))