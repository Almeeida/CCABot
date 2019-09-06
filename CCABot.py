from os import environ, listdir

from discord.ext.commands import Bot, when_mentioned_or
from database import UserManager, db

from json import load
with open('data/rank.json') as file_data:
  data = load(file_data)

class CCABot(Bot):
  def __init__ (self):
    super().__init__(
      command_prefix=when_mentioned_or('!'),
      owner_id=map(lambda x: int(x), environ['OWNER_ID'].split(', ')),
      case_insensitive=True,
      help_command=None
    )

    self.db = db
    self.cooldown_users = []
    self._users = UserManager(db.users.users)
    self._data = data
    self.env = environ

  async def on_ready (self):
    for plugin in [p[:-3] for p in listdir('plugins') if p.endswith('.py')]:
      try:
        self.load_extension('plugins.' + plugin)
      except Exception as e:
        print(f'Falha ao carregar o plugin \'{plugin}\'\n-\n{e.__class__.__name__}: {e}\n-')
      else:
        print(f'Plugin {plugin} carregado com sucesso.')

  async def on_message(self, message):
    if message.author.bot:
      return
  
    ctx = await self.get_context(message)

    ctx._user = self._users.get(message.author.id)
  
    try:
      await self.invoke(ctx)
    except Exception as e:
      print(e)
    await ctx._user.addPdl(ctx)

  def run(self):
    super().run(environ['DISCORD_TOKEN'], reconnect=True, bot=True)