import discord
import os
import requests
import json
import asyncio
from datetime import datetime
from discord.ext import commands

alexa = commands.Bot(("Alexa, ", "alexa, ", "Alexa ", "alexa "), case_insensitive=True, help_command=None)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = ""


class XColor(commands.Converter):
    avail = ['blue', 'blurple', 'dark_blue', 'dark_gold', 'dark_gray', 'dark_green', 'dark_grey', 'dark_magenta',
             'dark_orange', 'dark_purple', 'dark_red', 'dark_teal', 'dark_theme', 'darker_gray', 'darker_grey',
             'default', 'gold', 'green', 'greyple', 'light_gray', 'light_grey', 'lighter_gray', 'lighter_grey',
             'magenta', 'orange', 'purple', 'random', 'red', 'teal']

    async def convert(self, ctx, arg):
        if arg == "a random color":
            return discord.Colour.random()
        elif arg == "invisible":
            return discord.Colour.dark_theme()
        elif arg in self.avail:
            return getattr(discord.Colour, arg)()
        else:
            return discord.Colour.from_rgb(int(arg[1:3], base=16), int(arg[3:5], base=16), int(arg[5:7], base=16))


@alexa.command()
async def help(ctx, *, arg=None):
    if arg is None:
        with open("help.txt") as f:
            await ctx.send(f.read())


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
async def weather(ctx):
    ...


@weather.command(name="in")
async def get_weather(ctx, *, city):
    REQUEST_URL = BASE_URL + "q=" + city + "&appid=" + os.getenv("weatherapi")
    response = requests.get(REQUEST_URL)
    if response.status_code == 200:
        response_data = response.json()
        main = response_data['main']
        temp = round((main['temp'] - 273.15) * 180 + 3200) / 100
        #report = main['report'][0]['description']
        #await ctx.send("Right now in " + str(city) + ", it's " + str(temp) + " degrees with " + str(report) + ".")
        await ctx.send("Right now in " + str(city) + ", it's " + str(temp) + " degrees.")
    else:
        await ctx.send("Response error. (Status Code: " + str(response.status_code) + ")")


@alexa.group()
async def make(ctx):
    ...


@make.command(name="me")
async def colorize(ctx, *, col: XColor()):
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


@alexa.command(name="time")
async def get_time(ctx):
    time = datetime.now().strftime("%H:%M")
    await ctx.send("Right now, it is " + time + ".")


@alexa.command(name="date")
async def get_date(ctx):
    month = datetime.today().strftime("%m")
    day = datetime.today().strftime("%d")
    year = datetime.today().strftime("%y")
    day_of_week = datetime.today().strftime("%A")
    await ctx.send("Today is " + day_of_week + ", " + month + " " + day + ", " + year + ".")


@alexa.group()
async def super(ctx):
    ...


@super.command(name="alexa")
async def super_text(ctx):
    await ctx.send("Super Alexa mode, activated.")
    await asyncio.sleep(1)
    await ctx.send("Starting reactors...")
    await asyncio.sleep(1)
    await ctx.send("Online.")
    await ctx.send("Enabling advanced systems...")
    await asyncio.sleep(1)
    await ctx.send("Online.")
    await ctx.send("Raising dongers.")
    await asyncio.sleep(1)
    await ctx.send("Error! Dongers missing.")
    await ctx.send("Aborting...")


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
