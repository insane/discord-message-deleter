import discord, ctypes
import threading, time
from datetime import datetime
from os.path import exists
from rich import print

token = None
cpm = []
deleted = 0

def printLine(ln):
    print(f"[bold blue]{datetime.now().strftime('%H:%M:%S')}[/bold blue] {ln}")

if exists("cache/token.txt") and len(open("cache/token.txt").read()) > 0:
    printLine("Token found from cache/token.txt..")
    token = open("cache/token.txt").read().replace('"', '')
else:
    token = input("Enter your Discord token: ").replace('"', '')
    printLine("Saving token to cache/token.txt..")
    with open("cache/token.txt", "a+") as f:
        f.write(f"{token}")
        f.close()

def display():
    global cpm, deleted
    while 1:
        cpm = list(filter(lambda x: (time.time()-x)<=(60*1), cpm))
        ctypes.windll.kernel32.SetConsoleTitleW(f"discord msg deleter, dpm: {str(len(cpm))}, deleted: {deleted}")

threading.Thread(target=display).start()

class MyClient(discord.Client):

    async def on_ready(self):
        global cpm, deleted
        
        printLine(f"logged in as {self.user}")
        while 1:
            channel_id = int(input(f"\n[INPUT]: discord message link: ").split('/')[5])
            oldest_option = input(f"[OPTION]: oldest to first deletion? Y/N: ")
            oldest_option = False if oldest_option == "N" else True
            
            channel = self.get_channel(channel_id)
            printLine("starting task to delete messages..")
            
            async for msg in channel.history(limit=None, oldest_first=oldest_option):
                try:
                    
                    if msg.author == self.user and msg.type == discord.MessageType.default:
                        printLine(f"[{msg.id}] => successfully deleted")
                        deleted += 1
                        cpm.insert(0, time.time())
                        await msg.delete()
                        
                except: continue
                
            printLine(f"{deleted} messages deleted.")
            deleted = 0

try:
    client = MyClient(heartbeat_timeout=86400, guild_subscriptions=False)
    client.run(token, bot=False)
except KeyboardInterrupt:
    printLine(f"program quit by interrupt, reopen")
