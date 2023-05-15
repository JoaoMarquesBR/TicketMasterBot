import asyncio
import os
import interactions
import requests
from gitResponse import gitResponse, Actor, Payload
from dotenv import load_dotenv

class CheckPushCog(interactions.Extension):
    def __init__(self, client):
        self.client = client
        self.github_token = os.getenv('GIT_TOKEN')
        self.github_username = os.getenv('GIT_USERNAME')
        self.guild_id = int(os.getenv('SERVER_ID'))
        self.headers = {"Authorization": "Token {}".format(self.github_token)}

    @interactions.extension_listener(name='on_ready')
    async def on_ready(self):
        self.guild = await interactions.get(self.client, interactions.Guild, object_id=self.guild_id)
        last_id = self.get_last_id()
        while True:
            response = requests.get(f'https://api.github.com/users/{self.github_username}/events', headers=self.headers)

            for value in response.json():
                if value.get('type') == 'PushEvent':
                    if value.get('id') == last_id:
                        break
                    await self.send_message_for_channel(value)
                    last_id = self.get_last_id()

    def get_last_id(self) -> str:
        response = requests.get(f'https://api.github.com/users/{self.github_username}/events', headers=self.headers)
        values = response.json()
        print(values)
        for value in values:
            if value.get('type') == 'PushEvent':
                return value.get('id')


    async def send_message_for_channel(self, data: dict):
        mensagem = 'teste'
        print('fjsoiefnsfn')
        git_response = gitResponse(**data)
        actor = Actor(**git_response.actor)
        payload = Payload(**git_response.payload)
        category = await self.get_category(git_response.repo.get('name').replace('refs/heads/', '').lower())
        for channel in self.guild.channels:
            if channel.parent_id == category.id:
                if channel.name == payload.branch:
                    await channel.send(mensagem)

        channel = await self.guild.create_channel(
            name=payload.branch,
            type=interactions.ChannelType.GUILD_TEXT,
            parent_id=int(category.id)
        )
        await channel.send(mensagem)

    async def get_category(self, repo_name) -> interactions.Channel:
        channels = await self.guild.get_all_channels()
        for channel in channels:
            if channel.type == interactions.ChannelType.GUILD_CATEGORY:
                if channel.name == repo_name:
                    return channel

        channel = await self.guild.create_channel(
            name=repo_name,
            type=interactions.ChannelType.GUILD_CATEGORY
        )
        return channel

def setup(bot):
    CheckPushCog(bot)
