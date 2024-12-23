import yaml

with open('discource_parser/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, yaml.CLoader)