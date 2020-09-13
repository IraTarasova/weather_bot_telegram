from pathlib import Path
from datetime import timezone, timedelta


project_dir = Path(__file__).resolve().parent


def read_secrets(filename=project_dir / 'secrets.txt'):
    with open(filename, 'r') as fin:
        tokens_str = fin.read().split('\n')
    tokens_dict = {string.split()[0]: string.split()[1] for string in tokens_str}
    return tokens_dict


tokens = read_secrets()
token_telegram = tokens['token_telegram']
token_owm = tokens['token_owm']
lat = 59.860220
lon = 30.201939
timezone_moscow = timezone(timedelta(hours=3))
