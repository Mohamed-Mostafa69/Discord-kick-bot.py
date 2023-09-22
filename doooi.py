import discord
from discord.ext import commands, tasks

intents = discord.Intents(guilds=True, members=True)
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix="&", intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Genshin Impact Players"))
    print(f'{bot.user} has connected to Discord!')
    check_genshin_players.start()


@tasks.loop(seconds=60)
async def check_genshin_players():
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot:
                continue

            for activity in member.activities:
                if isinstance(activity, discord.Game) and activity.name == 'Genshin Impact':
                    try:
                        await member.kick(reason="Playing Genshin Impact")
                        await member.send(
                            "You were kicked from the server for playing Genshin Impact."
                        )

                        print(f"Kicked {member} for playing Genshin Impact.")
                    except discord.Forbidden:
                        print(
                            f"Failed to kick {member}. Insufficient permissions.")
                    except discord.HTTPException as e:
                        print(f"Failed to kick {member}. Error: {e}")


bot.run("")
