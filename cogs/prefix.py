from discord.ext.commands import Cog, Context
from discord.ext import commands

import variables
from utilities import logger, feedback

class Prefix(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix')
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        await ctx.message.delete()
        
        self.bot.command_prefix = prefix
        
        variables.bot_config.set('prefix', prefix)
        variables.bot_config.save()

        logger.get_logger().info(f"Bot prefix has been changed to {prefix}")
        
        return await feedback.notify(f"Bot prefix has been changed to {prefix} by {ctx.author.name}", ctx, delay=5)
        
    @prefix.error
    async def prefix_error(self, ctx: Context, error):
        await ctx.message.delete()
        await feedback.notify(error, ctx, delay=5)
        
async def setup(bot):
    await bot.add_cog(Prefix(bot))