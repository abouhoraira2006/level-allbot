import math
import aiosqlite
import asyncio
import discord
from discord.ext import commands

# should be fixed

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!")
bot.multiplier = 1

async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("expData.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, PRIMARY KEY (guild_id, user_id))")
    
@bot.event
async def on_ready():
    print(bot.user.name + " is ready.")

@bot.event
async def on_message(message):
    if not message.author.bot:
        cursor = await bot.db.execute("INSERT OR IGNORE INTO guildData (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id, message.author.id, 1)) 

        if cursor.rowcount == 0:
            await bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            cur = await bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (message.guild.id, message.author.id))
            data = await cur.fetchone()
            exp = data[0]
            lvl = math.sqrt(exp) / bot.multiplier
        
            if lvl.is_integer():
                await message.channel.send(f"{message.author.mention} well done! You're now level: {int(lvl)}.")

        await bot.db.commit()

    await bot.process_commands(message)

@bot.command()
async def me(ctx, member: discord.Member=None):
    if member is None: member = ctx.author

    # get user exp
    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND user_id = ?", (ctx.guild.id, member.id)) as cursor:
        data = await cursor.fetchone()
        exp = data[0]

        # calculate rank
    async with bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?", (ctx.guild.id,)) as cursor:
        rank = 1
        async for value in cursor:
            if exp < value[0]:
                rank += 1

    lvl = int(math.sqrt(exp)//bot.multiplier)

    current_lvl_exp = (bot.multiplier*(lvl))**2
    next_lvl_exp = (bot.multiplier*((lvl+1)))**2

    lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) * 100

    embed = discord.Embed(title=f"Stats for {member.name}", colour=discord.Colour.gold())
    embed.add_field(name="Level", value=str(lvl))
    embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}")
    embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
    embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

    await ctx.send(embed=embed)


#token = 'OTg2Mjc5NDczNTAwNTQwOTc5.G0a0SS.YKWszF8AEO3lEnfQ3L98_dQOkOZIpdxmZQ00xQ'
bot.loop.create_task(initialize())
#bot.run(token)
bot.run('OTg1OTI1OTE3NzQ4NjQxODUy.GaZLaP.sfibI4I_rgVnzm1RVp6qi6M19cV39CSflMPaF8')
#OTU2MTgyMTM5OTk1NTUzODQy.GZmeVg.g6_rp4vyayLxlq7PlZktStL7Qeq3VPhInJfXK8
#bot.run("OTU2MTgyMTM5OTk1NTUzODQy.G_yPGu.s0sqAjoa_zOiKepE1hJ_9quF5yOVtfXhOQvtG4")
#bot.run('OTg2Mjc5NDczNTAwNTQwOTc5.G0a0SS.YKWszF8AEO3lEnfQ3L98_dQOkOZIpdxmZQ00xQ')
#bot.run('OTg2Mjc5NDczNTAwNTQwOTc5.G0a0SS.YKWszF8AEO3lEnfQ3L98_dQOkOZIpdxmZQ00xQ')
asyncio.run(bot.db.close())
