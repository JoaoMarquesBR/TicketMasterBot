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

print(server_ID)


bot = interactions.Client(
    bot_Token,
    intents=interactions.Intents.ALL
)


        #print("Branch: ", value.get('payload').get('ref'))


@bot.event(name="on_ready")
async def onready():
    guild = await interactions.get(bot, interactions.Guild, object_id= int(server_ID))
    headers = {"Authorization": "Token {}".format(git_Token)}
    response = requests.get('https://api.github.com/users/JoaoMarquesBR/events', headers=headers)
    values = response.json()
    for value in values:
        print(value)
        if value.get('type') == 'PushEvent':
            ultimo_id = value.get('id')
            break
    while True:
        await asyncio.sleep(5)
        verify=False
        response = requests.get('https://api.github.com/users/JoaoMarquesBR/events', headers=headers)
        values = response.json()
        for value in values:
            if value.get('type') == 'PushEvent':
                if value.get('id') == ultimo_id:
                    break
                gitResponseJSON = gitResponse(**value)
                print(gitResponseJSON.id)
                print(gitResponseJSON.actor)
                print("=====================================")
                ultimo_id = value.get('id')
                branch_name = value.get('payload').get('ref').replace('refs/heads/', '')
                branch_name = branch_name.lower()
                verify = False
                for channel in guild.channels:
                    if channel.name == branch_name:
                        await channel.send(branch_name+" Commit from "+ value.get("actor").get("login"))
                        verify = True
                        break
                if verify:
                    break
                channel = await guild.create_channel(
                    name=branch_name,
                    type=interactions.ChannelType.GUILD_TEXT
                )
                await channel.send('mensagem 2')
                break

bot.start()