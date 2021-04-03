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


@alexa.group()
async def make(ctx):
    ...


@make.command(name="me")
async def colorize(ctx, col: discord.Colour):
    rname = "color-" + str(ctx.author.id)
    role_exists = False
    for i in ctx.guild.roles:
        if i.name == rname:
            role_exists = i
    if role_exists == False:
        role_exists = await ctx.guild.create_role(name=rname, color=col)
    else:
        await role_exists.edit(color=col)
    while True:
        try:
            await role_exists.edit(position=(role_exists.position+1))
        except:
            break
    await ctx.author.add_roles(role_exists)


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
