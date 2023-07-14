import json
import discord

from datetime import datetime

from discord.ext import commands

from discord.ext.commands import Cog, Bot, Context

from utilities import feedback

class Embeds(Cog):
	
	def __init__(self, bot):
		self._bot = bot

	@commands.command()
	# @commands.has_permissions(administrator=True)
	async def embed(self, ctx: Context, *, json_string):
		await ctx.message.delete()
		
		try:
			# Load the JSON string into a dictionary
			data = json.loads(json_string)
			
			# Convert datetime objects to strings
			for key in data:
				if isinstance(data[key], datetime):
					data[key] = data[key].isoformat()
			
			if "color" in data:
				color_value = data["color"]
				if isinstance(color_value, str):
					color_value = int(color_value.replace('#', ''), 16)
					
				color = discord.Color(color_value)
				
				del data["color"]
			else:
				color = discord.Color.light_grey()
			
			embed = discord.Embed.from_dict(data)
			embed.color = color
			
			# Send the embed to the channel
			await ctx.send(embed=embed)
		except Exception as exception:
			await feedback.notify(f"Invalid JSON string {exception}", ctx, delay=5)
		
	@embed.error
	async def embed_error(self, ctx: Context, error):
		await ctx.message.delete()
		await feedback.notify(error, ctx, delay=5)
	
async def setup(bot: Bot):
	await bot.add_cog(Embeds(bot))