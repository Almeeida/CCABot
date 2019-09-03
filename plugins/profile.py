from discord.ext import commands

class Profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='profile', aliases=['p'])
  @commands.cooldown(1, 4, commands.BucketType.user)
  async def _profile (self, ctx):
    elo = rank_names[ctx._user.data['rank'] - 1]
    pdl = ctx._user.data['pdl']
    pdl_total = ctx._user.data['rank'] * 100
    await ctx.channel.send(f'{ctx.author} **{elo}** com **{pdl}/{pdl_total}** PDL.')

rank_names = [
  'Ferro IV', 'Ferro III', 'Ferro II', 'Ferro I',
  'Bronze IV', 'Bronze III', 'Bronze II', 'Bronze I',
  'Prata IV', 'Prata III', 'Prata II', 'Prata I',
  'Gold IV', 'Gold II', 'Gold III', 'Gold IV',
  'Platina IV', 'Platina III', 'Platina II', 'Platina I',
  'Diamante IV', 'Diamante III', 'Diamante II', 'Diamante I',
  'Grão Mestre',
  'Mestre',
  'Desafiante'
]

def setup(bot):
    bot.add_cog(Profile(bot))