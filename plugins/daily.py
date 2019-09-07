from discord.ext import commands
from datetime import timedelta, datetime
from random import randint

day = timedelta(seconds=86400)

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

class Daily(commands.Cog):
  def __init__ (self, bot):
    self.bot = bot

  @commands.command(name='daily')
  @commands.cooldown(1, 4, commands.BucketType.user)
  async def _daily (self, ctx):
    user = ctx._user

    first_daily = False
    last_timestamp = user.data.get('daily_timestamp')
    date_now = datetime.now()

    if not last_timestamp:
      first_daily = True
      last_timestamp = date_now

    result = last_timestamp - date_now

    if result > day or first_daily:
      random_number = randint(0, 1000)
      blue_essence = (user.data.get('blue_essence') or 0) + random_number
      emoji = ctx.bot._data['emojis']['blue_essence']
      user.update({
        "blue_essence": int(blue_essence),
        "daily_timestamp": date_now
      })
      await ctx.channel.send(f'{ctx.author.mention}, você recebeu seus {emoji} {random_number} EA diários!')
    else:
      await ctx.channel.send(strfdelta(result - day, f'{ctx.author.mention},' + ' bônus diário já foi resgatado! aguarde {hours} Hora(s), {minutes} minuto(s), {seconds} segundo(s) para pegar novamente.'))
      
      
def setup(bot):
    bot.add_cog(Daily(bot))