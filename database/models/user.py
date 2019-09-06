from .Collection import Collection
from discord import Embed, Webhook, RequestsWebhookAdapter
from random import randint
from datetime import datetime
from json import load
import requests
import asyncio

with open('data/rank.json') as file_data:
  data = load(file_data)

class UserCollection(Collection):
  def __init__ (self, collection, user_id, register):
    super().__init__(collection, user_id, register)

  def get_structure(self):
    return {
      "_id": self.id, # id do discord doo usúario
      "pdl": 0, # experiencia que ele tem
      "rank": 1, # nivel que ele está
      "blue_essence": 0, # dinheiro que ele tem
      "honors_points": 0, # reputação que ele tem
      "honors_per_day": {}, # quantos de reputação q ele ganha por dia
      "pdl_per_day": {}, # quantos de pdl ele ganha por dia
      "rank_per_day": {}, # quantos niveis ele upou por dia
      "daily_timestamp": None, # timestamp do ultimo daily
      "political_party": None, # id do partido q ele está
      "voted": None # id de qual partido ele votou
    }

  # nome do rank que ele tá (pq o rank é salvado em numero)
  def rank_name (self, rank = None, showEmoji = False):
    rank = rank or self.data['rank']

    name = data['names'][rank - 1]
    if not showEmoji:
      return name
    else:
      emoji = data['emojis'][name.split(' ')[0].lower()]
      return f'{emoji} {name}'
  
  # total de pdl que ele tem / quando precisa pra upar
  def pdl_total (self, pdl = None, required = None, showRequired = True):
   pdl = pdl or self.data['pdl']
   if not showRequired:
     return pdl
   required = required or (self.data['rank'] * 100)
   return f'{pdl}/{required}'

  # add pdl de acordo com a mensagem dele
  async def addPdl (self, ctx):
    # ignora users em cooldown
    if ctx.author.id in ctx.bot.cooldown_users:
      return
    
    # rank, pdl e essencia azul atual
    rank = self.data.get('rank') or 1
    pdl = self.data.get('pdl') or 0
    blue_essence = self.data.get('blue_essence') or 0

    # datetime atual
    date = str(datetime.now().timestamp())


    #
    pdl_p_d = self.data.get('pdl_per_day') or {}
    rank_p_d = self.data.get('rank_per_day') or {}
    if date not in pdl_p_d:
      pdl_p_d[date] = 0
    if date not in rank_p_d:
      rank_p_d[date] = 0

    # porcentagem de quanto vai recebe
    percentage = rank_percentage[rank - 1] / 100

    # quantidade de palavras
    args_count = len(ctx.message.clean_content.strip().split(' ')) / 2

    # numero aleatorio 
    num_max = int(rank * percentage) + 1
    num_min = int(rank * percentage) - 1
    random_number = randint(num_min, num_max)

    # quantos pdl vai ganhar
    result_total = args_count + random_number
    discount_result = int(result_total * percentage)

    # quantia maximo
    if discount_result > 50:
      discount_result = 50

    # quantia minima
    if discount_result < 1:
      discount_result = 1

    # adicionando os pdl
    pdl += discount_result
    pdl_p_d[date] += discount_result

    # quantidade necessaria pra upar
    required = rank * 100
    rank_up = False

    # verificando se upou
    if pdl >= required and not rank == 27:
      pdl -= required
      rank += 1
      blue_essence += 1000
      rank_up = True
      rank_p_d[data] += 1

    # salvando na database
    self.update({
      "pdl": int(pdl),
      "rank": int(rank),
      "blue_essence": int(blue_essence),
      "pdl_per_day": pdl_p_d,
      "rank_per_day": rank_p_d
    })

    # enviar mensagem de promoção
    if rank_up:
      await send_promotion_message(self, rank, ctx)

    # adicionando user no cooldown
    await add_cooldown(ctx.author.id, ctx.bot.cooldown_users)
    # envindo msg no log
    send_to_log(ctx, random_number, result_total, discount_result, args_count)
     
# adicionando user no cooldown por 3 sec
async def add_cooldown (user_id, users):
  if not user_id in users:
    users.append(user_id)
    await asyncio.sleep(3)
    users.remove(user_id)

# porcentagem de quanto vai ganhar 
rank_percentage = [
    100, 100, 100, 100, # ferro
    98, 98, 98, 98, # bronze
    95, 95, 95, 95, # prata
    90, 90, 90, 90, # gold
    80, 80, 80, 80, # platina
    70, 70, 70, 70, # diamante
    60, # grao-mastre
    50, # mestre
    40, # challenger
]

# envia msg de promoção
async def send_promotion_message (_user, rank, ctx):
  rank_name = _user.rank_name(rank, showEmoji = True)
  await ctx.channel.send(f'{ctx.author.mention} Foi promovido para **{rank_name}**!')

# envia msg no log
def send_to_log (ctx, random_number, result_total, discount_result, args_count):
  webhook = Webhook.partial(int(ctx.bot.env['WEBHOOK_ID']), ctx.bot.env['WEBHOOK_TOKEN'], adapter=RequestsWebhookAdapter())
  if webhook:
    embed = Embed(color=ctx.author.color, description=f'''
    **{ctx.author}**
    **[mensagem]({ctx.message.jump_url})**
    **numero aleatorio: ** {random_number} 
    **quanto pelas palavras: ** {args_count}
    **resultado verdadeiro: ** {result_total}
    **resultado a receber: ** {discount_result}
    ''')
    webhook.send(embed = embed, username='PDL LOGS', avatar_url=ctx.bot.user.avatar_url)
