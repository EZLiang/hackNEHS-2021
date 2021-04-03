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

@alexa.command(name="add")
async def add(ctx, num1: float, num2: float):
    await ctx.send(num1+num2)

@alexa.command(name="subtract")
async def sub(ctx, num1: float, num2: float):
    await ctx.send(num1-num2)

@alexa.command(name="multiply")
async def mul(ctx, num1: float, num2: float):
    await ctx.send(num1*num2)

@alexa.command(name="divide")
async def div(ctx, num1: float, num2: float):
    try:
        await ctx.send(num1/num2)
    except ZeroDivisionError:
        await ctx.send("You can't divide by zero!")


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
