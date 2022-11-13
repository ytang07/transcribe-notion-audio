import requests
import os
import json

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

NOTION_KEY = os.environ.get("NOTION_KEY")
headers = {'authorization': f"Bearer {NOTION_KEY}",
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
            "accept": "application/json",
            }
# this is the link to the mp3 block
url = "https://api.notion.com/v1/blocks/3db65f57ffd747ecabcb167c2594e02c"

response = requests.get(url, headers=headers)
res_json = json.loads(response.text)
for key, value in res_json.items():
    print(key, value)
# print(res_json['parent']['page_id'])