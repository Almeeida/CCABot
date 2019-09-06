from discord.ext import commands
from discord import Embed, File


class Profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='rank')
  @commands.cooldown(1, 4, commands.BucketType.user)
  async def _rank (self, ctx):
    rank = ctx._user.rank_name()
    pdl = ctx._user.pdl_total()
    await ctx.channel.send(f'{ctx.author.mention}, **{rank}** com **{pdl}** PDL.')


  @commands.command(name='profile', aliases=['p'])
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def _profile (self, ctx):
    user = ctx._user

    rank = user.rank_name()
    pdl = user.pdl_total()
    rank_name = rank.lower().split(' ')[0]
    blue_essence = user.data['blue_essence']
    reputation = user.data.get('reputation') or '0'
    political_party = user.data.get('political_party') or 'Nenhum'
    voted = user.data.get('voted') or 'Ninguém'

    embed = Embed(colour = ctx.author.color)
    embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    embed.add_field(name='ELO', value=rank)
    embed.add_field(name='PDLs', value=pdl)
    embed.add_field(name='Essencia Azul', value=blue_essence)
    embed.add_field(name='Reputação', value=reputation)
    embed.add_field(name='Partido', value=political_party)
    embed.add_field(name='Votou', value=voted)

    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_image(url='attachment://image.png')

    image = File(fp=f'assets/{rank_name}.png', filename='image.png')
    await ctx.send(embed=embed, file=image)


    
def setup(bot):
    bot.add_cog(Profile(bot))