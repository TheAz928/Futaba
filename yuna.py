import os

import discord

import variables

from discord.ext.commands import AutoShardedBot

from terminal.terminal import TerminalListener

from utilities import logger

from utilities.config import ConfigFile

class DiscordBot(AutoShardedBot):
	
	def __init__(self, config: ConfigFile, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.config = config
	
	async def setup_hook(self):
		for file in os.listdir("cogs"):
			if not file.endswith(".py"):
				continue  # Skip non-python files
			
			name = file[:-3]
			await self.load_extension(f"cogs.{name}")
	
	async def on_ready(self):
		logger.get_logger().info(f"Logged in as {self.user.name}")

if __name__ == "__main__":
	bot = DiscordBot(variables.bot_config, command_prefix=variables.bot_config.get('prefix'), intents=discord.Intents.all())

	logger.get_logger().info("Now listening on terminal")

	terminal = TerminalListener(bot=bot)
	terminal.start()
	
	logger.get_logger().info("Attempting to connect with the bot")
	
	bot.run(bot.config.get('token'))
	
	terminal.join()