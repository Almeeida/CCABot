from .Collection import Collection
from random import randint

import asyncio

class UserCollection(Collection):
  def __init__ (self, collection, user_id, created_at, register):
    self.created_at = created_at
    super().__init__(collection, user_id, register)

  def get_structure(self):
    return {
      "_id": self.id,
      "timestamp": self.created_at,
      "pdl": 0,
      "rank": 1,
      "blue_essence": 0,
      "reputation": 0,
      "daily_timestamp": None,
      "political_party": None
    }

  async def addPdl (self, ctx):
    if ctx.author.id in ctx.bot.cooldown_users:
      return

    args_count = len(ctx.args)
    random_number = randint(0, 11)
    timestamp = (ctx.message.created_at - self.data['timestamp']).total_seconds()
    rank_boost = rank_boosts[self.data['rank'] - 1]
    result = limit((limit(args_count / 2) + random_number + limit(timestamp) + rank_boost) / 2, True)

    total_pdl = self.data['pdl'] + result
    total_rank = self.data['rank']

    if total_pdl >= 1000:
      total_pdl = 0
      total_rank += 1
      rank_name = rank[total_rank - 1]
      ctx.send(f'Upou pro {rank_name}!')

    self.update({
      "pdl": total_pdl,
      "rank": total_rank
    })

    channel = ctx.bot.get_channel(ctx.bot.env['PDL_CHANNEL'])
    print(channel, ctx.bot.env['PDL_CHANNEL'])
    if channel:
      channel[0].send(f'**{ctx.author.username}** ganhou {result} **PDL**!')
     

def limit (number, total = False):
  if total and number > 40:
    return 40
  elif total == False and number > 15:
    return 15
  else:
    return number

async def add_cooldown (user_id, users):
  if not user_id in users:
    users.append(user_id)
    await asyncio.sleep(3)
    users.remove(user_id)

rank_boosts = [
  9, 9, 9, 9, # ferro
  8, 8, 8, 8, # bronze
  7, 7, 7, 7, # prata
  6, 6, 6, 6, # gold
  5, 5, 5, 5, # platina
  4, 4, 4, 4, # diamante
  3, # grão-mastre
  2, # mestre
  1 # challenger
]

rank = [
  'Ferro I', 'Ferro II', 'Ferro III', 'Ferro IV',
  'Bronze I', 'Bronze II', 'Bronze III', 'Bronze IV',
  'Prata I', 'Prata II', 'Prata III', 'Prata IV',
  'Gold I', 'Gold II', 'Gold III', 'Gold IV',
  'Platina I', 'Platina II', 'Platina III', 'Platina IV',
  'Diamante I', 'Diamante II', 'Diamante III', 'Diamante IV',
  'Grão Mestre',
  'Mestre',
  'Desafiante'
]