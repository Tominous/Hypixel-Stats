import aiopypixel
import arrow
import asyncio
import discord
from discord.ext import commands
from math import floor, ceil


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cache = self.bot.get_cog("Cache")

        self.embed = discord.Embed(color=self.bot.cc)

    @commands.command(name="arcade", aliases=["hypixelarcade", "hypixel_arcade", "ak"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def arcade(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Arcade Stats", icon_url=await self.cache.get_player_head(p.UUID))

        arcade = p.STATS["Arcade"]

        embed.add_field(name="All Time Coins", value=floor(arcade.get("coins")), inline=False)
        embed.add_field(name="Coins This Month",
                        value=arcade.get("monthly_coins_a"),
                        inline=False)
        embed.add_field(name="Coins This Week", value=arcade.get("weekly_coins_a"),
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="arena", aliases=["hypixelarena", "hypixel_arena", "ar"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def arena(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Arena Stats", icon_url=await self.cache.get_player_head(p.UUID))

        arena = p.STATS["Arena"]

        embed.add_field(name="Coins", value=arena.get("coins"), inline=True)
        embed.add_field(name="\uFEFF", value=f"\uFEFF")
        embed.add_field(name="Coins Spent", value=arena.get("coins_spent"), inline=True)

        kills = sum({k: v for k, v in arena.items() if "kills_" in k}.values())
        deaths = sum({k: v for k, v in arena.items() if "deaths_" in k}.values())
        embed.add_field(name="Kills", value=kills)
        embed.add_field(name="Deaths", value=deaths)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        games = sum({k: v for k, v in arena.items() if "games_" in k}.values())
        wins = arena.get("wins")
        losses = sum({k: v for k, v in arena.items() if "losses_" in k}.values())
        embed.add_field(name="Games", value=games, inline=True)
        embed.add_field(name="Wins", value=wins if wins is not None else 0, inline=True)
        embed.add_field(name="Losses", value=losses, inline=True)

        total_dmg = sum({k: v for k, v in arena.items() if "games_" in k}.values())
        embed.add_field(name="Total Damage", value=total_dmg, inline=True)
        embed.add_field(name="Rating", value=round(arena.get("rating", 0), 2), inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="battleground", aliases=["battle ground", "battlegrounds", "battle_ground", "bg"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def battleground(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Battleground Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        battle = p.STATS["Battleground"]

        embed.add_field(name="Coins", value=battle.get("coins"), inline=True)
        embed.add_field(name="Wins", value=battle.get("wins"), inline=True)
        embed.add_field(name="Losses", value=battle.get("losses"), inline=True)

        kills = battle.get("kills", 0)
        deaths = battle.get("deaths", 0)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        embed.add_field(name="Damage Inflicted", value=battle.get("damage"))
        embed.add_field(name="Damage Taken", value=battle.get("damage_taken"))
        embed.add_field(name="Life Leeched", value=battle.get("life_leeched"))

        await ctx.send(embed=embed)

    @commands.command(name="hungergames", aliases=["hungergame", "hunger_games", "hg"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hunger_games(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Hungergames Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        hunger = p.STATS["HungerGames"]

        embed.add_field(name="Coins", value=hunger.get("coins"), inline=True)
        embed.add_field(name="\uFEFF", value=f"\uFEFF")
        embed.add_field(name="Wins", value=hunger.get("wins"), inline=True)

        kills = hunger.get("kills", 0)
        deaths = hunger.get("deaths", 0)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="paintball", aliases=["paint_ball", "pb"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def paintball(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Paintball Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        paint = p.STATS["Paintball"]

        embed.add_field(name="Coins", value=paint.get("coins"), inline=True)
        embed.add_field(name="\uFEFF", value=f"\uFEFF")
        embed.add_field(name="Wins", value=paint.get("wins"), inline=True)

        kills = paint.get("kills", 0)
        deaths = paint.get("deaths", 0)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        embed.add_field(name="Shots Fired", value=paint.get("shots_fired"), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="quake", aliases=["qk"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def quake(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Quake Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        quake = p.STATS["Quake"]

        embed.add_field(name="Coins", value=quake.get("coins"), inline=True)
        embed.add_field(name="\uFEFF", value=f"\uFEFF")
        embed.add_field(name="Wins", value=quake.get("wins"), inline=True)

        kills = quake.get("kills", 0)
        deaths = quake.get("deaths", 0)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        embed.add_field(name="Shots Fired", value=quake.get("shots_fired"), inline=True)
        embed.add_field(name="Headshots", value=quake.get("headshots"), inline=True)

        embed.add_field(name="Highest Killstreak", value=quake.get("highest_killstreak"), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="uhc", aliases=["ultrahc", "ultrahardcore", "uhardcore"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def uhc(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s UHC Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        uhc = p.STATS["UHC"]

        embed.add_field(name="Coins", value=uhc.get("coins"), inline=True)
        embed.add_field(name="Wins", value=uhc.get("wins"), inline=True)
        embed.add_field(name="Score", value=uhc.get("score"), inline=True)

        kills = uhc.get("kills", 0)
        deaths = uhc.get("deaths", 0)
        embed.add_field(name="Kills", value=kills, inline=True)
        embed.add_field(name="Deaths", value=deaths, inline=True)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        embed.add_field(name="Heads Eaten", value=uhc.get("heads_eaten"), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="bedwars", aliases=["bed_wars", "bed", "bedw"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def bedwars(self, ctx, *, player):
        p = await self.cache.get_player(player)

        embed = self.embed.copy()

        embed.set_author(name=f"{p.DISPLAY_NAME}'s Bedwars Stats",
                         icon_url=await self.cache.get_player_head(p.UUID))

        bedwars = p.STATS["Bedwars"]

        embed.add_field(name="XP", value=bedwars.get("Experience"))
        embed.add_field(name="Coins", value=bedwars.get("coins"))
        embed.add_field(name="Stars", value=p.ACHIEVEMENTS.get("bedwars_level"), inline=True)

        embed.add_field(name="Losses", value=bedwars.get("beds_lost_bedwars"))
        embed.add_field(name="Wins", value=bedwars.get("wins_bedwars"))
        embed.add_field(name="Winstreak", value=bedwars.get("winstreak"))

        kills = bedwars.get("kills_bedwars", 0)
        deaths = bedwars.get("deaths_bedwars", 0)
        embed.add_field(name="Kills", value=kills)
        embed.add_field(name="Deaths", value=deaths)
        embed.add_field(name="KDR", value=round(
            (kills + .00001) / (deaths + .00001), 2),
                        inline=True)

        embed.add_field(name="Beds Broken", value=bedwars.get("beds_broken_bedwars"), inline=True)
        embed.add_field(name="Total Games",
                        value=sum({k: v for k, v in bedwars.items() if "games_played" in k}.values()))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))