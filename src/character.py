import yaml
import os
from .config import *
from dataclasses import dataclass
from typing import List, Dict, Tuple

def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error in configuration file: {e}")
            return None
@dataclass 
class Character:
    name: str
    summary: Dict[str, str]
    config: dict

class CharactersLoader:
    def __init__(self, story_config) -> None:
        self.characters = self._load_characters(story_config)

    def _load_characters(self, story_config):
        characters = {}
        base_path = os.path.join(story_config['path']  + '/Characters')
        for character_name in story_config['characters'].keys():
            character_path = os.path.join(base_path, character_name)
            if os.path.isdir(character_path):
                config_path = os.path.join(character_path, 'config.yaml')
                summary_path = os.path.join(character_path, 'summary.txt')
                character_config = read_yaml_file(config_path)
                
                with open(summary_path, 'r') as summary_file:
                    summary = summary_file.read()
                character = Character(name=character_name, summary={f'chapter_{index+1}':chap for index, chap in enumerate(summary.split('@@@'))}, config=character_config)
                characters[character_name] = character
                
        return characters
    
    def __iter__(self)->Tuple[str, Character]:
        return iter(self.characters.items())

if __name__ == '__main__':
    characters_instance = CharactersLoader(StoryPath['Cinderella'])
    for char_name, value in characters_instance:
        print(value.config)
        break