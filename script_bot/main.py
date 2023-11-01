import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from requests import get

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is on ready')


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if "bonjours" in message.content:
        await message.channel.send(f'bonjours')
    await bot.process_commands(message)


@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(f'hello {ctx.author}')


@bot.command()
async def compteur(ctx: commands.Context, n: int):
    for i in range(n + 1):
        await ctx.send(str(i))


@bot.command()
async def echo(ctx: commands.Context, n: int, *, message: str):
    for _ in range(n):
        await ctx.send(message)


@bot.command()
async def clear(ctx: commands.Context, amount: int = 5) -> discord.Message:
    async for message in ctx.channel.history(limit=amount):
        await message.delete()


@bot.command()
async def meteo(ctx: commands.Context, *, city: str):
    def get_geo_city(city):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={getenv("WEATHER_APP_KEY")}'
        result = get(url).json()
        lat = result[0]["lat"]
        lon = result[0]["lon"]
        return lat, lon

    def weather_city(city_geo):
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={city_geo[0]}&lon={city_geo[1]}&appid={getenv("WEATHER_APP_KEY")}'
        result = get(url).json()
        return result["weather"], result['main']

    def convert_kelvin_to_celsius(temp):
        return round(temp - 273.15)

    geo = get_geo_city(city)
    geo_dunkerque = get_geo_city('dunkerque')
    data = weather_city(geo)
    data_dunkerque = weather_city(geo_dunkerque)
    temp = convert_kelvin_to_celsius(data[1]['temp_max'])
    temp_dunkerque = convert_kelvin_to_celsius(data_dunkerque[1]['temp_max'])
    weather = data[0][0]['main']
    weather_dunkerque = data_dunkerque[0][0]['main']
    response = f"{city} => {temp}°C et le ciel est {weather} \n Dunkerque => {temp_dunkerque}°C et le ciel est {weather_dunkerque}"
    await ctx.send(response)

if __name__ == '__main__':
    bot.run(getenv('TOKEN'))
