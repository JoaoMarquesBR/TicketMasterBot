import asyncio
import requests
import interactions
import os
from dotenv import load_dotenv
from gitResponse import gitResponse



load_dotenv()
bot_Token = os.getenv("BOT_TOKEN")
server_ID = os.getenv("SERVER_ID")
git_Token = os.getenv("GIT_TOKEN")
name_git = os.getenv("GIT_USERNAME")

print(server_ID)


bot = interactions.Client(
    bot_Token,
    intents=interactions.Intents.ALL
)




async def getEvents():
    headers = {"Authorization": "Token {}".format(git_Token)}
    response = requests.get(f'https://api.github.com/users/{name_git}/events', headers=headers)
    values = response.json()
    return values

async def checkForCommits(guild,last_id):
    eventsResponse = await getEvents()
    verify = False
    for event in eventsResponse:
        if(event.get('type') == 'PushEvent'):
            if event.get('id') == last_id:  
                #no changes were made.
                    print("No changes were made.")
                    break
            last_id = event.get('id')
            branch_name = event.get('payload').get('ref').replace('refs/heads/', '')
            branch_name = branch_name.lower()
            verify = False
            for channel in guild.channels:
                if channel.name == branch_name:
                    print("attempt to send msg")
                    await channel.send(branch_name+" Commit from "+ event.get("actor").get("login"))
                    verify = True
                    break
            if verify:
                break      
    return last_id

@bot.event(name="on_ready")
async def onready():
    guild = await interactions.get(bot, interactions.Guild, object_id= int(server_ID))
    #gets last response and save last_id    
    last_id = ""
    eventsResponse = await getEvents()
    for event in eventsResponse:
        if event.get('type') == 'PushEvent':
            last_id = event.get('id')
            break
    while True:
        await asyncio.sleep(5)
        last_id = await checkForCommits(guild,last_id)


    
print("exit with 1?")

bot.start()
