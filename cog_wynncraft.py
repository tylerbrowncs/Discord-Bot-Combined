import discord, config, requests, math

from bot import db

from discord.ext import commands

class Wynncraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["wynnstats", "wynncraftstats"])
    async def wstats(self, ctx, username:str):
        req = requests.get(f"https://api.wynncraft.com/v2/player/{username}/stats")
        data = req.json()
        if data["code"] == 200:
            data = data["data"][0]
            if data["guild"]["name"] == None:
                embed=discord.Embed(title=f"{username}'s stats. ({data['rank']})", description=f"{username} is not in a guild.", color=0xe2d78d)
            else:      
                embed=discord.Embed(title=f"{username}'s stats.  ({data['rank']})", description=f"{username} is a {data['guild']['rank'].lower()} of the {data['guild']['name']} guild.", color=0xe2d78d)

            uuid = data["uuid"].replace("-","")
            embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/350/{uuid}")

            embed.add_field(name="Rank", value=data["meta"]["tag"]["value"], inline=True)
            embed.add_field(name="Playtime", value="{} hours".format(math.floor(data['meta']['playtime']/60*4.7), inline=True))
            embed.add_field(name="Total Level", value=data["global"]["totalLevel"]["combined"], inline=True)
            embed.add_field(name="Chests Opened", value=data["global"]["chestsFound"], inline=True)
            embed.add_field(name="Mobs Killed", value=data["global"]["mobsKilled"], inline=True)
            embed.add_field(name="Deaths", value=data["global"]["deaths"], inline=True)

            
            
            await ctx.channel.send(embed=embed)
        elif data["code"] == 400:
            await ctx.channel.send("A player with that username was not found")

    @commands.command(pass_context=True, aliases=["wynnclasses", "wynncraftclasses"])
    async def wclasses(self, ctx, username, classNum:int=None):
        req = requests.get(f"https://api.wynncraft.com/v2/player/{username}/stats")
        data = req.json()
        server = db.get("servers", ctx.guild.id)
        prefix = server["prefix"]
        if data["code"] == 200:

            
            if classNum == None:
                data = data["data"][0]
                stri = f"""Type ``{prefix}wynnclasses {username} (Number)`` to get more information on each class."""
                for i in range(len(data["classes"])):
                    name = ''.join([i for i in data["classes"][i]["name"] if not i.isdigit()])
                    name = name.title()
                    stri = stri + f"""\n[{i+1}] {name} (Lvl: {data["classes"][i]['level']})"""
                embed=discord.Embed(title=f"{username}'s classes.", color=0xe2d78d)
                embed.add_field(name="Classes", value=stri)

                uuid = data["uuid"].replace("-","")
                embed.set_thumbnail(url=f"https://visage.surgeplay.com/bust/350/{uuid}")
                await ctx.send(embed=embed)


            else:
                data = data["data"][0]["classes"]
                if  0 < classNum < len(data)+1:

                    gamemodes = ""
                    if data[classNum-1]["gamemode"]["hardcore"] == True:
                        gamemodes = gamemodes + "Hardcore "
                    if data[classNum-1]["gamemode"]["hunted"] == True:
                        gamemodes = gamemodes + "Hunted "
                    if data[classNum-1]["gamemode"]["ironman"] == True:
                        gamemodes = gamemodes + "Iron Man "
                    if data[classNum-1]["gamemode"]["craftsman"] == True:
                        gamemodes = gamemodes + "Craftsman "
                            
                    
                    embed = discord.Embed(title="{}'s Class [{}/{}]".format(username, classNum, len(data)), description=gamemodes, color=0xe2d78d)
                    data = data[classNum-1]
                    name = ''.join([i for i in data["name"] if not i.isdigit()])
                    name = name.title()
                    embed.add_field(name="Class", value=name, inline=True)
                    embed.add_field(name="Total Level", value=data["level"], inline=True)
                    embed.add_field(name="Discoveries", value=str(data["discoveries"]), inline=True)
                    embed.add_field(name="Quests Completed", value=str(data["quests"]["completed"]) + "/259", inline=True)
                    embed.add_field(name="Playtime", value=str(math.floor(data["playtime"]/60*4.7)) + " hours", inline=True)
                    embed.add_field(name="Mobs Killed", value=data["mobsKilled"], inline=True)
                    
                    if name == "Skyseer":
                        name = "shaman"
                    if name == "Hunter":
                        name = "archer"
                    if name == "Ninja":
                        name = "assassin"
                    if name =="Knight":
                        name = "warrior"
                        
                    skills=data["skills"]


                    embed.set_thumbnail(url=f"https://cdn.wynncraft.com/img/stats/classes/{name.lower()}.png")
                    profs = data["professions"]

                    profsLevels = """**Combat:** {} [*{}%*]\n""".format(profs["combat"]["level"],profs["combat"]["xp"])
                    
                    profsLevels += """**Farming:** {} [*{}%*]\n""".format(profs["farming"]["level"],profs["farming"]["xp"])
                    profsLevels += """**Mining:** {} [*{}%*]\n""".format(profs["mining"]["level"],profs["mining"]["xp"])
                    profsLevels += """**Fishing:** {} [*{}%*]\n""".format(profs["fishing"]["level"],profs["fishing"]["xp"])
                    profsLevels += """**Woodcutting:** {} [*{}%*]\n""".format(profs["woodcutting"]["level"],profs["woodcutting"]["xp"])

                    profsLevels += """**Alchemism:** {} [*{}%*]\n""".format(profs["alchemism"]["level"],profs["alchemism"]["xp"])
                    profsLevels += """**Cooking:** {} [*{}%*]\n""".format(profs["cooking"]["level"],profs["cooking"]["xp"])
                    profsLevels += """**Scribing:** {} [*{}%*]\n""".format(profs["scribing"]["level"],profs["scribing"]["xp"])
                    profsLevels += """**Woodworking:** {} [*{}%*]\n""".format(profs["woodworking"]["level"],profs["woodworking"]["xp"])
                    profsLevels += """**Weaponsmithing:** {} [*{}%*]\n""".format(profs["weaponsmithing"]["level"],profs["weaponsmithing"]["xp"])
                    profsLevels += """**Armouring:** {} [*{}%*]\n""".format(profs["armouring"]["level"],profs["armouring"]["xp"])
                    profsLevels += """**Tailoring:** {} [*{}%*]\n""".format(profs["tailoring"]["level"],profs["tailoring"]["xp"])

                    embed.add_field(name="__**Levels**__", value=profsLevels, inline=True)

                    dungString = """Total: {}""".format(data["dungeons"]["completed"])
                    for i in data["dungeons"]["list"]:
                        if i["name"] != "Spider" and i["name"] != "Skeleton" and i["name"] != "Animal" and i["name"] != "Zombie": 
                            dungString = dungString + """\n**{}**: {}""".format(i["name"], i["completed"])


                    raidString = """Total: {}""".format(data["raids"]["completed"])
                    for i in data["raids"]["list"]:
                        raidString = raidString + """\n**{}**: {}""".format(i["name"], i["completed"])

                    embed.add_field(name="__**Dungeons**__", value=dungString, inline=True)
                    embed.add_field(name="__**Raids**__", value=raidString, inline=False)
                    embed.set_footer(text=f"STR: {skills['strength']}, DEX: {skills['dexterity']}, INT: {skills['intelligence']}, DEF: {skills['defence']}, AGI: {skills['agility']}\n*Old dungeons are not listen but do count towards the total.")

                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("That player's class doesnt excist.")
                
        elif data["code"] == 400:
            await ctx.channel.send("A player with that username was not found")


def setup(bot):
    bot.add_cog(Wynncraft(bot))