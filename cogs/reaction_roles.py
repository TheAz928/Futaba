import re

import discord

from discord.ext import commands

from discord.ext.commands import Cog, Context

import variables

from utilities import logger, feedback

from utilities.config import ConfigProvider, ConfigFile
	
class ReactionRoles(Cog):
	
	def __init__(self, bot):
		self._bot = bot
		self._config = ConfigFile(variables.get_file_path("config/reaction_roles.yml"), provider=ConfigProvider.YAML)
		
		if len(self._config.cache) == 0:
			self._config.cache = []
			
	@commands.command(name='rr')
	@commands.has_permissions(administrator=True)
	async def command(self, ctx: Context, message_id, reaction_id, role_id):
		await ctx.message.delete()
		
		rid = re.search(r":([^:]+):", reaction_id)
		if rid:
			reaction_id = rid.group(1)
		
		data = {
			'message_id': int(message_id),
			'reaction_id': reaction_id,
			'role_id': int(role_id)
		}
		
		if isinstance(self._config.cache, dict):
			if data in self._config.cache.values():
				return await feedback.notify(f"An entry already exists!", ctx, delay=5)
		if isinstance(self._config.cache, list):
			if data in self._config.cache:
				return await feedback.notify(f"An entry already exists!", ctx, delay=5)
		
		self._config.cache.append(data)
		self._config.save()

		logger.get_logger().info(f"A new reaction role data has been recorded: \n``Message ID: {message_id}``\n``Reaction: {reaction_id}``\n``Role ID: {role_id}``")
	
		return await feedback.notify(f"A new reaction role data has been recorded, {data}", ctx, delay=5)
	
	@command.error
	async def command_error(self, ctx: Context, error):
		await ctx.message.delete()
		
		return await feedback.notify(error, ctx, delay=5)
	
	@Cog.listener()
	async def on_message_delete(self, message):
		if len(self._config.cache) == 0:
			return
		
		for data in self._config.cache:
			if data['message_id'] == message.id:
				self._config.cache.remove(data)
				self._config.save()
				
				logger.get_logger().info(f"Removed a reaction role entry due to message removal: {message}")
				
	@Cog.listener()
	async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
		if len(self._config.cache) == 0:
			return
		
		guild = self._bot.get_guild(payload.guild_id)
		if guild is None:
			return
		
		for data in self._config.get_all():
			if payload.message_id != int(data['message_id']):
				continue
			
			matched = False
			if payload.emoji.name == str(data['reaction_id']):
				matched = True
			if not matched:
				try:
					if payload.emoji.id == int(data['reaction_id']):
						matched = True
				except Exception:
					pass
			
			if not matched:
				continue
			
			role = guild.get_role(int(data['role_id']))
			if role is None:
				continue
			
			try:
				logger.get_logger().info(payload.member.name + " has reacted with (" + payload.emoji.name + ") and has been granted the role: " + str(role.name))
				
				await payload.member.add_roles(role)
			except discord.HTTPException as error:
				logger.get_logger().error(error)
				
				pass
	
	@Cog.listener()
	async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
		if len(self._config.cache) == 0:
			return
		
		guild = self._bot.get_guild(payload.guild_id)
		member = guild.get_member(payload.user_id)
		
		if guild is None:
			return
		
		for data in self._config.get_all():
			if payload.message_id != int(data['message_id']):
				continue
			
			matched = False
			if payload.emoji.name == str(data['reaction_id']):
				matched = True
			if not matched:
				try:
					if payload.emoji.id == int(data['reaction_id']):
						matched = True
				except Exception:
					pass
			
			if not matched:
				continue
			
			role = guild.get_role(int(data['role_id']))
			if role is None:
				continue
			
			try:
				logger.get_logger().info(member.name + " has reacted with (" + payload.emoji.name + ") resulting in removal of the role: " + str(role.name))
				
				await member.remove_roles(role)
			except discord.HTTPException as error:
				logger.get_logger().error(error)
				
				pass
		
async def setup(bot):
	await bot.add_cog(ReactionRoles(bot))