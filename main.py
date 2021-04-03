import discord
from discord.ext import commands
import os

alexa = commands.Bot(("Alexa, ", "alexa, "), case_insensitive=True)


@alexa.group()
async def simon(ctx):
    ...


@simon.command(name="says")
async def echo(ctx, *, text):
    await ctx.send(text)


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
