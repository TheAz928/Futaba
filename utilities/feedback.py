from discord.ext.commands import Context

async def notify(message: str, ctx: Context, delay=None):
	var = await ctx.send(message)
	
	return await var.delete(delay=delay)

