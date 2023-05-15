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
name_git = 'victorgabrieldeon'

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
    response = requests.get(f'https://api.github.com/users/{name_git}/events', headers=headers)
    values = response.json()
    for value in values:
        print(value)
        if value.get('type') == 'PushEvent':
            ultimo_id = value.get('id')
            break
    while True:
        await asyncio.sleep(5)
        verify=False
        response = requests.get(f'https://api.github.com/users/{name_git}/events', headers=headers)
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

class NewBranch(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name='new_branch',
        description='adicione uma nova branch',
        options=[
            interactions.Option(
                type=interactions.OptionType.STRING,
                name="branch_name",
                description="o nome do branch",
                required=True,
            )
        ]
    )
    async def new_branch(self, ctx: interactions.CommandContext, branch_name):
        self.branch_name = branch_name
        headers = {
            'Authorization': 'Token {}'.format(git_Token),
        }
        request_repositorys = requests.get('https://api.github.com/user/repos', headers=headers)
        options_repo = []
        for repo in request_repositorys.json():
            name = repo.get('name')
            if name not in [repo.value for repo in options_repo]:
                options_repo.append(
                    interactions.SelectOption(
                        label=name,
                        value=name,
                    )
                )
        await ctx.send('Escolha um repository')
        select_menu_options = []
        for i in range((len(options_repo) // 25)+1):

            menu = interactions.SelectMenu(
                custom_id='branch_selected',
                placeholder='Selecione um repository',
                options=options_repo[i*25:(i+1)*25]
                )

            await ctx.channel.send(components=menu)

    @interactions.extension_component('branch_selected')
    async def branch_selected(self, ctx: interactions.ComponentContext, repo_name: list[str]):
        repo_name = repo_name[0]
        base_url = f'https://api.github.com/repos/{name_git}/{repo_name}'
        main_branch_url = f'{base_url}/git/refs/heads/main'
        branch_url = f'{base_url}/git/refs'
        headers = {
            'Authorization': 'Token {}'.format(git_Token),
            'Accept'       : 'application/vnd.github.v3+json'
        }

        # Busca o último commit na branch main
        response = requests.get(main_branch_url, headers=headers)
        commit_sha = response.json()['object']['sha']

        # Cria a nova branch
        data = {
            'ref': f'refs/heads/{self.branch_name}',
            'sha': commit_sha
        }
        response = requests.post(branch_url, headers=headers, json=data)

        if response.status_code == 201:
            await ctx.send('Nova branch criada com sucesso!')
        else:
            await ctx.send('Erro ao criar a nova branch')
            print(response.text)
NewBranch(bot)

bot.start()