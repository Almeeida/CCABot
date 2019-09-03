from dotenv import load_dotenv
load_dotenv()

import discord
import asyncio

from os import environ

import pymongo

myclient = pymongo.MongoClient(environ['DATABASE_URL'])
database = myclient['users']
collection = database['users']

from random import randint

class User:
    pdl = 0
    rank = 0
    money = 0
    rep = 0
    region = None
    def __init__(self, userID, last_message):
        self._id = userID
        self.last_message = last_message

users = []
cooldown_users = []
async def cooldown (user_id):
  if not user_id in cooldown_users:
    cooldown_users.append(user_id)
    print(f'{user_id} adicionado')
    await asyncio.sleep(3)
    cooldown_users.remove(user_id)
    print(f'{user_id} removido')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content == 'ddd' and message.author.id == '281561868844269569':
          exit()
        print(cooldown_users)
        if message.author.bot:
              return
        
        x = [x for x in users if x['id'] == message.author.id]
        if len(x) <= 0:
          user = {
            "id": message.author.id,
            "timestamp": message.created_at,
            "pdl": 0,
            "count": 0,
            "total": 0
          }
          users.append(user)
        else:
          user = x[0]
        
        index = users.index(user)
        # quantidade de frases
        a = len(message.content.strip().split(' ')) / 2
        if a > 15:
          a = 15
        # um numero aleatorio de 1 a 10
        b = randint(0, 11)
        # o tempo entre a ultima msg q ele enviou
        c = message.created_at - user['timestamp']
        # em segundos
        d = c.total_seconds()
        if d > 15:
          d = 15
        # resultado
        result = (float(a) + float(b) + float(d)) / 2
        if result <= 0:
          result = 1

         # salvando
        user['timestamp'] = message.created_at
        if not message.author.id in cooldown_users:
          user['pdl'] += int(result)
          user['count'] += 1
        user['total'] += 1
        users[index] = user

        print('-' * 50)
        print(f'''
        palavra: {a}
        numero aleatorio: {b}
        timestamp: {c}
        total de segundos do timestamp: {d / 0.1}
        result2: {result}

        pdl = {user['pdl']}
        mensagens = {user['count']}
        ''')
        print('Message from {0.author}: {0.content}'.format(message))

        if message.content == '!test':
          await message.channel.send("{}**PDL** em {} **mensagens** (total de msgs enviadas {})".format(user['pdl'], user['count'], user['total']))

        await cooldown(message.author.id)


client = MyClient()
client.run(environ['DISCORD_TOKEN'])