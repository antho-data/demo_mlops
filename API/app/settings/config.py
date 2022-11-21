import os
import yaml

def load_yaml_file(file_path : str):
	"""Load config from yaml file.
	:param file_path: String
	:return: dict
	"""
	with open(file=file_path, mode='r') as ymlfile:
		return yaml.load(ymlfile, Loader=yaml.FullLoader)

def get(setting_name : str):
	return settings.get(setting_name)

settings = load_yaml_file(os.path.realpath("app/settings/config.yaml"))