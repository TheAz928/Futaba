import json
import os

import yaml

from enum import Enum

class ConfigProvider(Enum):
	YAML = "yml"
	JSON = "json"
	
class ConfigFile:
	
	file_path = ""
	cache = []
	
	def __init__(self, path: str, provider: ConfigProvider):
		if provider == ConfigProvider.YAML:
			pass
		elif provider == ConfigProvider.JSON:
			pass
		else:
			raise TypeError("Unknown config type")
		
		self.file_path = path
		self.provider = provider
		
		self.reload()
		
	def get_provider(self):
		return self.provider
		
	def reload(self):
		if self.provider == ConfigProvider.YAML:
			if os.path.isfile(self.file_path):
				self.cache = yaml.safe_load(open(self.file_path, 'r', encoding='UTF-8'))
			else:
				stream = open(self.file_path, 'w', encoding='UTF-8')
				# stream.write("---[]\n...")
				stream.close()
				
		if self.provider == ConfigProvider.JSON:
			if os.path.isfile(self.file_path):
				self.cache = json.load(open(self.file_path, 'r', encoding='UTF-8'))
			else:
				stream = open(self.file_path, 'w', encoding='UTF-8')
				# stream.write("{}")
				stream.close()
				
		if self.cache is None:
			self.cache = []
		
	def get_all(self):
		return self.cache
	
	def get(self, key: str | int, default=None):
		if key in self.cache:
			return self.cache[key]
		else:
			return default
		
	def set(self, key: str | int, value):
		self.cache[key] = value
	
	def get_nested(self, key: str, default=None):
		keys = key.split(".")
		value = self.cache
		
		try:
			for i in keys:
				value = value[i]
		except KeyError:
			return default
		
		return value
	
	def set_nested(self, key: str, value):
		keys = key.split(".")
		for key in keys[:-1]:
			self.cache = self.cache.setdefault(key, {})
			
		self.cache[keys[-1]] = value
		
	def save(self):
		if self.provider == ConfigProvider.YAML:
			with open(self.file_path, 'w') as file:
				yaml.dump(self.cache, file)
				
				file.close()
		if self.provider == ConfigProvider.JSON:
			with open(self.file_path, 'w') as file:
				json.dump(self.cache, file)
				
				file.close()
			