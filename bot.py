from discord.ext import commands
import discord
import logging
import asyncio
import asyncpg
import dotenv
import os

logging.basicConfig(level=logging.INFO)  # Should be logging.WARNING in the future, like this for debug purposes ig
logging.getLogger("asyncio").setLevel(logging.CRITICAL)  # Hide those annoying errors

dotenv.load_dotenv()


async def get_prefix(_bot, msg):
    if msg.guild is not None:
        pp = await _bot.db.fetchrow("SELECT prefix FROM prefixes WHERE gid=$1", msg.guild.id)
        if pp is not None:
            return pp
    return "h!"


bot = commands.AutoShardedBot(shard_count=1, command_prefix=get_prefix, help_command=None, case_insensitive=True,
                              max_messages=512)

# Stuffs
bot.cc = "0xFFAA00"
bot.guild_invite_code = "MZ2cXxF"
bot.error_channel_id = 718983583779520541


async def setup_db():
    bot.db = await asyncpg.create_pool(host="localhost", database="hypixel-stats-bot", user="pi",
                                       password=os.getenv("psql"),
                                       command_timeout=5)


asyncio.get_event_loop().run_until_complete(setup_db())

# Yes this bc !!reload *
bot.cog_list = ["cogs.core.errors", "cogs.core.events", "cogs.core.database", "cogs.cmds.basic_mc",
                "cogs.cmds.settings"]

for cog in bot.cog_list:
    bot.load_extension(cog)


@bot.check
async def _bot_check_thingy(ctx):
    if not bot.is_ready():
        await ctx.send(embed=discord.Embed(color=bot.cmd_c, description="Hold on! We're starting up!"))
        return False
    return not ctx.author.bot


bot.run(os.getenv("discord"), bot=True)
