#!/usr/bin/python
import time
import discord
import os
import subprocess
import mcstatus
from mcstatus import MinecraftServer

CHANNEL_ID = 841821749406203975

async def greet():
    channel = client.get_channel(CHANNEL_ID)

os.chdir('C:\spigot1.16.4')
print(os.getcwd())
from mcstatus import MinecraftServer

from discord.ext import commands

server = MinecraftServer.lookup("192.168.3.14")
try:
    status = server.status()
    print("サーバーはオンラインです".format(status.players.online, status.latency))
except:
    print("サーバーはオフラインです")

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Ready")
    
@client.command()
async def server_start(ctx):
    print("Starting server")
    try:
        status = server.status()
        print("```css\nThe server is already running")
        await ctx.send("```css\nThe server is already running\n```")
    except:
        await ctx.send('Starting minecraft server. Please wait a few seconds...')
        subprocess.Popen('start.sh', shell=True)
        time.sleep(10)
        await ctx.send("```css\nServer started\nAddress: 00.152.192.000```")
        
    
    
@client.command()
async def server_status(ctx):
    print("Server status requested.")
    try:
        status = server.status()
        print("サーバーはオンラインです".format(status.players.online, status.latency))
        await ctx.send("**Server status**\n```サーバーはオンラインです```".format(status.players.online, status.latency))
    except:
        await ctx.send("**Server status**\n```サーバーはオフラインです```")
    
@client.command()
async def server_stop(ctx):
    print("サーバーはシャットダウンされます")
    try:
        status = server.status()
        if status.players.online !=0:
            await ctx.send("**このコマンドは準備中です:**\n```diff\n- Sorry. server can only be shutdown if no one is playing.\nPlayers: {0}```".format(status.players.online))
        else:
            await ctx.send("**Server shutdown requested:**\n```このコマンドは準備中です```")
    except:
        await ctx.send('```diff\n- Server is not running\n```')
    
    status = server.status()
    
@client.command()
async def server_help(ctx):
    print("Server shutdown requested.")
    await ctx.send("```css\nMinecraft server controller\nBy AyyZee\nWritten in python\n```\n```arm\nCOMMAND : WHAT HAPPENS\n```\n```arm\n.server_help : Show this message.\n\n.server_start : Starts the minecraft server, playable after 5 to 10 seconds.\n\n.server_status : Shows player numbers & latency or whether the server is offline.\n\n.server_stop : Stops the server only when no one is playing.\n```\n```fix\nServer address = YOURSERVER.COM```")
    

client.run('ODQxNzQwMDQzMDQzMzQwMjg4.YJrJgQ.QfP5Cwc1CiiOJlJ5S-XXX_000')
