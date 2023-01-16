import discord
from discord.ext import commands
from nextcord.ext import commands
import json
import aiohttp
import random
from gtts import gTTS
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO


intents=discord.Intents.default()
intents.members=True
api_key="AIzaSyBaUcMzJmGBuSwTQZD74WqQNR08jxbVuxw"

client = commands.Bot(command_prefix=".",intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot is connected successfully")

#For checking the latency of the bot
@client.command()
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")

#To join channel 
@client.command()
async def join(ctx):
    if(ctx.author.voice):
        channel=ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("U are Not in a vc")

#To leave channel
@client.command()
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the vc")
    else:
        await ctx.send("I am not in a vc")

#to import memes from subreddit
@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cd:
        async with cd.get("https://www.reddit.com/r/dankmemes/.json") as r:
            meme = await r.json()
            embed = discord.Embed(color=discord.Color.random())
            embed.set_image(url=meme["data"]["children"][random.randint(0,25)]["data"]["url"])
            embed.set_footer(text= f"Memes by {ctx.author}")
            await ctx.send(embed= embed)



#To display users avatar
@client.command()
async def avatar(ctx,*,member: discord.Member=None):
    member=ctx.author if not member else member
    embed = discord.Embed()
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)



#To make the bot write
@client.command()
async def write(ctx, arg):
    await ctx.send(arg)


#For TTSS
@client.command(name="tts")
async def tts(ctx, *args):
    text= " ".join(args)
    user = ctx.message.author
    if user.voice != None:
        try:
            vc = await user.voice.channel.connect()
        except:
            vc=ctx.voice_client
        sound=gTTS(text=text,lang="en", slow=False)
        sound.save("tts-audio.mp3")

        source = await discord.FFmpegOpusAudio.from_probe("tts-audio.mp3", method="fallback")
        vc.play(source) 
    else:
        await ctx.send("First come into a vc")

#Dming welcome message to joining members
@client.event
async def on_member_join(member):
    embed= discord.Embed(
        colour= (discord.Colour.blue()),
        title="Welcome to our server",
        description=f'Welcome {member.mention}, Enjoy ur time here 😊'
    )
    await member.send(embed=embed)

#Image search
@client.command(aliases=["show","search","find"])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="5341ac67f7b724df9", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here is your Image ({search}) ")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)



client.run("MTA1ODY0Nzc3OTU4NjYwOTE4Mg.Gq8afK.HkqPuPllPL88a0HVGQ4iwUJAiApr9TGHhTSEWI")