from discord.ext import commands

import requests, discord

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(pass_context=True, aliases=["poke", "pokémon"])
    async def pokemon(self, ctx, pokemon, shiny=" "):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        data = response.json()
        if len(str(data["id"])) == 1:
            id = "00" + str(data["id"])

        if len(str(data["id"])) == 2:
            id = "00" + str(data["id"])

        else:
            id = str(data["id"])

        if len(data["types"]) == 1:
            types = data["types"][0]["type"]["name"].capitalize()
        else:
            types = data["types"][0]["type"]["name"].capitalize() + "\n" + data["types"][1]["type"]["name"].capitalize()

        abilities = []
        for i in data["abilities"]:
            if i["is_hidden"]:
                abilities.append(i["ability"]["name"].capitalize() + " (Hidden Ability)")

            else:
                abilities.append(i["ability"]["name"].capitalize())
        

        embed=discord.Embed(title=f"#{id} {data['name'].capitalize()}", url=f"https://www.pokemon.com/uk/pokedex/{pokemon}", color=0xff0000)
        embed.set_author(name="Pokédex", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/1026px-Pok%C3%A9_Ball_icon.svg.png")
        if str(shiny).lower() == "shiny":
            embed.set_thumbnail(url=data["sprites"]["front_shiny"])
        else:
            embed.set_thumbnail(url=data["sprites"]["front_default"])
        embed.add_field(name="Type", value=types + "     ", inline=True)
        embed.add_field(name="Weight/Height", value=f"Height: *{data['height']*10}cm*\nWeight: *{data['weight']/10}kg*     ", inline=True)
        embed.add_field(name="Abilities", value="\n".join(abilities), inline=True)
        stats = f"""**HP:** {data['stats'][0]['base_stat']}
    **ATK:** {data['stats'][1]['base_stat']}
    **DEF:** {data['stats'][2]['base_stat']}
    **SPATK:** {data['stats'][3]['base_stat']}
    **SPDEF:** {data['stats'][4]['base_stat']}
    **SPD:** {data['stats'][5]['base_stat']}"""

        embed.add_field(name="__Base Stats__", value=stats, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pokemon(bot))