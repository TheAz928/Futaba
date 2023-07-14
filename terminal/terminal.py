import os
import threading

from discord.ext.commands import AutoShardedBot

from utilities import logger

class TerminalListener(threading.Thread):
	
	def __init__(self, bot: AutoShardedBot):
		super().__init__()
		
		self.bot_loaded = False
		self.bot = bot
		self.commands = [
		
		]
		
	def run(self):
		def clear_input():
			if os.name == 'nt':
				os.system('cls')
			else:
				os.system('clear')
		
		while not self.bot.is_closed():
			user_input = input()
			loop = self.bot.loop
			
			# clear_input()
			
			if user_input == 'info' or user_input == 'about':
				async def show():
					info = await self.bot.application_info()
					
					return logger.get_logger().info(info)
				
				loop.call_soon(loop.create_task, show())
				
			if user_input == 'stop':
				logger.get_logger().info("This is goodbye, shutdown sequence initiated")
				
				loop.call_soon(loop.create_task, self.bot.close())
				
				break
			
			# todo: implement command system with 'help' command
		
		exit(0)