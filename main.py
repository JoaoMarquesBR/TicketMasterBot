from src import main

if __name__ == '__main__':
    main()




'''class NewBranch(interactions.Extension):
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
            ),
            interactions.Option(
                type=interactions.OptionType.CHANNEL,
                channel_types=[interactions.ChannelType.GUILD_CATEGORY],
                name="categoria",
                description="Escolha a categoria",
                required=True,
            ),
        ]
    )
    async def new_branch(self, ctx: interactions.CommandContext, branch_name, categoria):
        self.branch_name = branch_name
        self.categoria: interactions.Channel = categoria
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
        try:
            response = requests.get(main_branch_url, headers=headers)
            commit_sha = response.json()['object']['sha']
        except:
            main_branch_url = f'{base_url}/git/refs/heads/master'
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
            await ctx.guild.create_channel(
                name=self.branch_name,
                type=interactions.ChannelType.GUILD_TEXT,
                parent_id=int(self.categoria.id)
            )
        else:
            await ctx.send('Erro ao criar a nova branch')
            print(response.text)'''

