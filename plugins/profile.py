from discord.ext import commands

class Profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='rank')
  @commands.cooldown(1, 4, commands.BucketType.user)
  async def _profile (self, ctx):
    elo = ctx.bot._data['names'][ctx._user.data['rank'] - 1]
    pdl = ctx._user.data['pdl']
    pdl_total = ctx._user.data['rank'] * 100
    await ctx.channel.send(f'{ctx.author.mention}, **{elo}** com **{pdl}/{pdl_total}** PDL.')

def setup(bot):
    bot.add_cog(Profile(bot))