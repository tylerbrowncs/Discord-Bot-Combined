import discord, config, os, asyncio,datetime
from discord.ext import commands

from database import Database

def get_prefix(bot, message):
    id = message.guild.id
    serverData = db.get("servers", id)
    return serverData["prefix"]

bot = commands.Bot(command_prefix=get_prefix)

bot.remove_command('help')


db = Database()

for i in os.listdir():
    if i.startswith("cog_") and i.endswith(".py"):
        try:   
            bot.load_extension(i[0:len(i)-3])
        except Exception as e:
            #raise e
            print(i + " failed to load")

@bot.command(pass_context=True)
async def listcog(ctx):
    cogs = ""
    for i in os.listdir():
        if i.startswith("cog_") and i.endswith(".py"):
            cogs = cogs + "\n" + i

    embed = discord.Embed(title="List of Cogs", description=cogs)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def load(ctx, cog):
    if ctx.author.id in config.devs:
        cog = f"cog.{cog}.py"
        try:   
            bot.load_extension(cog)
            embed=discord.Embed(title="Cog", description=f"Successfully loaded {cog[4:len(cog)]}.", color=0x2bff00)
            await ctx.send(embed=embed)
        except Exception as e: 
            #raise e 
            embed=discord.Embed(title="Cog", description=f"Failed to load {cog[4:len(cog)]}", color=0xff0000)
            await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def unload(ctx, cog):
    if ctx.author.id in config.devs:
        cog = f"cog.{cog}.py"
        try:   
            bot.unload_extension(cog)
            embed=discord.Embed(title="Cog", description=f"Successfully loaded {cog[4:len(cog)]}.", color=0x2bff00)
            await ctx.send(embed=embed)
        except Exception as e: 
            #raise e 
            embed=discord.Embed(title="Cog", description=f"Failed to load {cog[4:len(cog)]}", color=0xff0000)
            await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def reload(ctx, cog="All"):
    if ctx.author.id in config.devs:
        if cog.lower() == "all":
            for i in os.listdir():
                if i.startswith("cog_") and i.endswith(".py"):
                    try:   
                        bot.unload_extension(i[0:len(i)-3])
                        bot.load_extension(i[0:len(i)-3])
                        embed=discord.Embed(title="Cog", description=f"Successfully reloaded {i[4:len(i)-3]}.", color=0x2bff00)
                        await ctx.send(embed=embed)
                    except Exception as e: 
                        #raise e
                        embed=discord.Embed(title="Cog", description=f"Failed to reload {i[4:len(i)-3]}", color=0xff0000)
                        await ctx.send(embed=embed)
        else:
            cog = f"cog_{cog}"
            try:   
                bot.unload_extension(cog)
                bot.load_extension(cog)
                embed=discord.Embed(title="Cog", description=f"Successfully reloaded {cog[4:len(cog)]}.", color=0x2bff00)
                await ctx.send(embed=embed)
            except Exception as e: 
                #raise e 
                embed=discord.Embed(title="Cog", description=f"Failed to reload {cog[4:len(cog)]}", color=0xff0000)
                await ctx.send(embed=embed)

async def saveDB():
    await bot.wait_until_ready()

    while True:
        db.saveAll()
        user = await bot.fetch_user(config.devs[0])
        #await user.send("["+ datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S") + "] Database saved!")
        await asyncio.sleep(config.datebase_save_integral)

bot.loop.create_task(saveDB())

bot.run(config.token)