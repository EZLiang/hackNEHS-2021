import discord
import os
import requests
import json
import random
import asyncio
from datetime import datetime
from PyDictionary import PyDictionary # pip3 install PyDictionary
from discord.ext import commands

alexa = commands.Bot(("Alexa, ", "alexa, ", "Alexa ", "alexa "), case_insensitive=True, help_command=None)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = ""

dictionary = PyDictionary()


temp_group = None


async def nothing(ctx):
    ...


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
    if arg == "with colors":
        colors = "\n".join(XColor.avail)
        await ctx.send("Recognised colors: ```\n" + colors + "\n```\nAlso, you can specify a color using the "
                                                             "hexadecimal `#ABCDEF` format, or invisible for the "
                                                             "Discord background color (`#36393F`), or a random color "
                                                             "to get a random color")


temp_group = alexa.group(name="simon")(nothing)


@temp_group.command(name="says")
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


temp_group = alexa.group(name="weather")(nothing)


@temp_group.command(name="in")
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


temp_group = alexa.group(name="make")(nothing)


@temp_group.command(name="me")
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


@alexa.command(name="reset")
async def decolorize(ctx):
    rname = "color-" + str(ctx.author.id)
    role_exists = False
    for i in ctx.guild.roles:
        if i.name == rname:
            role_exists = i
    if role_exists == False:
        return
    else:
        await role_exists.delete()


@alexa.command(name="time")
async def get_time(ctx):
    time = datetime.now().strftime("%H:%M")
    await ctx.send("Right now, it is " + time + ".")


@alexa.command(name="date")
async def get_date(ctx):
    date = datetime.today().strftime("%m/%d/%y")
    day_of_week = datetime.today().strftime("%A")
    await ctx.send("Today is " + day_of_week + ", " + date + ".")


temp_group = alexa.group(name="super")(nothing)


@temp_group.command(name="alexa")
async def super_text(ctx):
    await ctx.send("Super Alexa mode, activated.")
    await asyncio.sleep(1)
    await ctx.send("Starting reactors...")
    await asyncio.sleep(1)
    await ctx.send("Online.")
    await ctx.send("Enabling advanced systems...")
    await asyncio.sleep(1)
    await ctx.send("Online.")
    await ctx.send("Raising dongers...")
    await asyncio.sleep(1)
    await ctx.send("Error! Dongers missing.")
    await ctx.send("Aborting...")


@alexa.command(name="translate")
async def translate(ctx, word, into, language_code):
    translated_word = dictionary.translate(word, language_code)
    await ctx.send("In " + language_code + ", " + word + " is: " + translated_word + ".")


temp_group = alexa.group(name="roll")(nothing)


@temp_group.command(name="dice")
async def roll(ctx, sides: int):
    await ctx.send(random.randint(1, sides))


temp_group = alexa.group(name="flip")(nothing)


@temp_group.command(name="coin")
async def roll(ctx):
    if random.randint(1, 2) == 1:
        await ctx.send("You got heads!")
    else:
        await ctx.send("You got tails!")

temp_group = alexa.group(name="roast")(nothing)
@temp_group.command(name="me")
async def roast_someone(ctx):
    await ctx.send("Okay, just let me go get a fire extinguisher real quick.")



@alexa.command(name="ping")
async def return_ping(ctx):
    await ctx.send(f'My ping is {round(alexa.latency*100, 2)}ms!')


@alexa.command(name="info")
async def return_info(ctx):
    await ctx.send("""Alexa Personal Assistant Bot v0.1
    (c) 2021 EZLiang, waitblock under the MIT License
    Made for hackNEHS 2021
    Not affiliated with Amazon.com, Inc.""")


temp_group = alexa.group(name="do")(nothing)
temp_group = temp_group.group(name="you")(nothing)
temp_group = temp_group.group(name="work")(nothing)


@temp_group.command(name="for")
async def nightlight(ctx):
    await ctx.send("Operation Nightlight has been compromised")


@alexa.command(name="rickroll")
async def rick(ctx, channel: discord.VoiceChannel):
    connection = await channel.connect()
    connection.play(discord.FFmpegPCMAudio("rick.mp3", executable="ffmpeg.exe"))


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
