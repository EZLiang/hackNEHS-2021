import discord
import os
import requests
import json
from discord.ext import commands

alexa = commands.Bot(("Alexa, ", "alexa, ", "Alexa ", "alexa "), case_insensitive=True)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = ""


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

@alexa.command(name="in")
async def get_weather(ctx, *, city):
    REQUEST_URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(REQUEST_URL)
    if response.status_code == 200:
        response_data = response.json()
        main = response_data['main']
        temp = main['temp']
        report = main['report'][0]['description']
        await ctx.send("Right now in " + str(city) + ", it's " + str(temp) + " degrees with " + str(report) + ".")
    else:
        await ctx.send("Response error. (Status Code: " + str(response.status_code) + ")")


@alexa.event
async def on_connect():
    print("Success!")


alexa.run(os.getenv("token"))
