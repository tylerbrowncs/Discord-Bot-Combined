from discord.ext import commands

from bot import db, get_prefix

import re, discord

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot running....")


    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            db.add_server(message.guild.id)
            db.add_user(message.author.id)
        except: pass


        if message.channel.type != discord.DMChannel:
            try:
                regex =  r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
                url = re.findall(regex, message.content)
                if len(url) > 0: 
                    userdata = db.get("users", message.author.id)
                    db.change("users", message.author.id, "attachments", userdata["attachments"]+len(url))

                elif len(message.attachments) > 0: 
                    userdata = db.get("users", message.author.id)
                    db.change("users", message.author.id, "attachments", userdata["attachments"]+len(message.attachments))

                elif len(message.embeds) > 0:
                    userdata = db.get("users", message.author.id)
                    db.change("users", message.author.id, "attachments", userdata["attachments"]+len(message.embeds))

                elif message.content[0] in [".", "-", "!", get_prefix(self.bot, message)]:
                    userdata = db.get("users", message.author.id)
                    db.change("users", message.author.id, "commands", userdata["commands"]+1)

                else:
                    userdata = db.get("users", message.author.id)
                    db.change("users", message.author.id, "messages", userdata["messages"]+1)
            except Exception as e:
                raise e

        #await self.bot.process_commands(message)


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await ctx.send("pong")

def setup(bot):
    bot.add_cog(events(bot))