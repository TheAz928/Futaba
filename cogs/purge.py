import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit: int, user: discord.Member = None):
        if user:
            check = lambda m: m.author == user and m.channel == ctx.channel
        else:
            check = lambda m: m.channel == ctx.channel

        deleted = await ctx.channel.purge(limit=limit + 1, check=check)
        
        await ctx.send(f"Deleted {len(deleted) - 1} messages.")

async def setup(bot):
    await bot.add_cog(Purge(bot))
