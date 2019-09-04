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

    args_count = len(ctx.message.content.split(' '))
    random_number = randint(0, 11)
    timestamp = ((ctx.message.created_at - self.data['timestamp']).total_seconds() * 3) / 100
    rank_boost = rank_boosts[self.data['rank'] - 1]
    result = int(limit((limit(args_count) + random_number + limit(timestamp) + rank_boost) / 2, True))

    if args_count == 1 and len(ctx.message.content) <= 3:
      result = 1

    total_pdl = self.data['pdl'] + result
    total_rank = self.data['rank']
    total_blue_essence = self.data['blue_essence']

    required = total_rank * 100
    rank_up = False

    if total_pdl >= required and not total_rank == 27:
      total_pdl -= required
      total_rank += 1
      total_blue_essence += 1000
      rank_up = True

    self.update({
      "pdl": total_pdl,
      "rank": total_rank,
      "blue_essence": total_blue_essence
    })

    if rank_up:
      rank_name = ctx.bot._data['names'][total_rank - 1]
      rank_emoji = ctx.bot._data['emojis'][rank_name.split(' ')[0].lower()]
      be_emoji = ctx.bot._data['emojis']['blue_essence']
      await ctx.channel.send(f'{ctx.author.mention} Foi promovido para {rank_emoji} **{rank_name}**!\n > {be_emoji} 1000')

    print(f'''
    args_count {args_count}
    random_number {random_number}
    timestamp {timestamp}
    rank_boost {rank_boost}

    result {result}
    total {total_pdl}
    ''')
    channel = ctx.bot.get_channel(int(ctx.bot.env['PDL_CHANNEL']))
    if channel:
      await channel.send(f'**{ctx.author}** ganhou {result} **PDL**!')
     

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