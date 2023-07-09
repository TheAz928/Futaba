import os

from utilities.config import ConfigFile, ConfigProvider

base_directory = os.path.dirname(os.path.realpath(__file__))

def get_file_path(path: str) -> str :
	return os.path.realpath(base_directory + "/" + path)

def get_dir_path(path: str) -> str :
	return os.path.realpath(base_directory + "/" + path + "/")

bot_config = ConfigFile(get_file_path('config/bot.yml'), provider=ConfigProvider.YAML)