import subprocess
# インストールした discord.py を読み込む
import discord
import os
import sys
import yarr
import numpy
import time
import socketserver
import mcstatus
from wakeonlan import send_magic_packet
from mcstatus import MinecraftServer

def proc_numpy(a):
    print(a)

server1 = MinecraftServer.lookup("192.168.11.13")
try:
    status = server1.status()
    print("サーバーオンライン")
except:
    print("サーバーオフライン")

os.chdir('C:\spigot1.16.4')

# TOKENとサーバーの情報
TOKEN = 'ODQxNzQwMDQzMDQzMzQwMjg4.YJrJgQ.QfP5Cwc1CiiOJlJ5S-fPwWU_48A'
f_name = 'spigot-1.16.4.jar'
maxMemory = '10G'  # 任意の最大メモリ割り当てサイズ
minMemory = '10G'  # 任意の最小メモリ割り当てサイズ

# 接続に必要なオブジェクトを生成
client = discord.Client()

# サーバー操作用
class server_process:

    def __init__(self, f_name, maxMemory,minMemory):
        self.server = None
        self.command = ["java", "-server",f'-Xms{minMemory}', f'-Xmx{maxMemory}', "-jar", f_name, "nogui"]

    def start(self):
        self.server = subprocess.Popen(self.command, stdin=subprocess.PIPE)

    def stop(self):
        input_string = "stop"
        self.server.communicate(input_string.encode())

server = server_process(f_name, maxMemory, minMemory)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == '/mcstart':
        await message.channel.send('サーバーを起動します')
        server.start()

    elif message.content == '/mcstop':
        await message.channel.send('サーバーを終了します')
        server.stop()
        time.sleep(10)
        os.execv(sys.executable, ['Python'] + sys.argv)
    
    elif message.content == '/mcstatus':
        try:
            status = server1.status() #server開いてるかのコマンド
            print("ステータスリクエスト")
            await message.channel.send('サーバーはオンラインです')
        except:
            print("ステータスリクエスト")
            await message.channel.send('サーバーはオフラインです')

    elif message.content == '/mcplayer':
        try:
            status = server1.status()
            print("プレイヤーリクエスト")
            await message.channel.send("サーバーには{0}人います".format(status.players.online))
        except:
            print("サーバーオフライン")
            await message.channel.send("サーバーを起動してください")

    elif message.content == '/wsstart': 
         send_magic_packet('00.00.00.00.00.00')
         print("パソコン起動中")
         await message.channel.send("パソコン起動中")

    elif message.content == '/wsstop': 
        try:
            status = server1.status()
            print("オンライン")
            server.stop()
            await message.channel.send('サーバー停止中')
            time.sleep(10)
            await message.channel.send('パソコンをシャットダウンします')
            os.system('shutdown -s -f')
        except:
            await message.channel.send('パソコンをシャットダウンします')
            os.system('shutdown -s -f')

    elif message.content == '/wsrestart':
        try:
            status = server1.status()
            print("オンライン")
            await message.channel.send('サーバー停止')
            server.stop()
            time.sleep(10)
            await message.channel.send('パソコンを再起動します')
            os.system('shutdown -r -f')
        except:
            await message.channel.send('パソコンを再起動します')
            os.system('shutdown -r -f')

    elif message.content == '/mchelp':
        print('ヘルプコマンド')
        await message.channel.send('/mcstart:サーバー起動\n/mcstop:サーバー停止\n/mcstatus:ステータス確認\n/mcplayer:サーバー人数\n/mchelp:コマンド確認\n/wsrestart:PC再起動')
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
