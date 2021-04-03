import discord
from discord.ext import commands
import os

alexa = commands.Bot(("Alexa, ", "alexa, "), case_insensitive=True)


@alexa.command(name="simon says")
def echo(ctx, *, text):
    await ctx.send(text)


alexa.run(os.getenv("token"))
