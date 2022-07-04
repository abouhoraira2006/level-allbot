import math
import aiosqlite
import asyncio
import discord
from discord.ext import commands

# should be fixed
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(bot.user.name + " is ready.")
    
@bot.command()
async def on(ctx):
    await ctx.send("hi , i am on')
                   
bot.run("OTg1OTIyMTY0NjkzODE5NDY0.GnYWNh.aOJNAikjn2BDPM1koXiE9RIWQTz4q-Yy4oPlrU")
