import time
from steamship import Steamship
from steamship.base import TaskState
from flask import Flask, request
import os
import requests
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

'''initilize flask application framework'''
app = Flask(__name__)
app.debug = True
  
@app.route('/', methods=['GET','POST'])
def mp3_file_submit():

  instance = Steamship.use("audio-markdown", "audio-markdown-crows-v27")

  # this is the link to the mp3 block
  # url = "https://api.notion.com/v1/blocks/3db65f57ffd747ecabcb167c2594e02c"
  if request.method == "POST":
    data = request.json
    url = data['url']
    # print(url)
    block_id = url.split("#")[1]
    url = f"https://api.notion.com/v1/blocks/{block_id}"

  response = requests.get(url, headers=headers)
  # print(response.text)
  res_json = json.loads(response.text)
  # print(res_json)

  audio_url = res_json['audio']['file']['url']
  page_id = res_json['parent']['page_id']

  transcribe_task = instance.invoke("transcribe_url", url=audio_url)
  task_id = transcribe_task["task_id"]
  status = transcribe_task["status"]

  # Wait for completion
  retries = 0
  while retries <= 100 and status != TaskState.succeeded:
      response = instance.invoke("get_markdown", task_id=task_id)
      status = response["status"]
      if status == TaskState.failed:
          print(f"[FAILED] {response}['status_message']")
          break

      print(f"[Try {retries}] Transcription {status}.")
      if status == TaskState.succeeded:
          break
      time.sleep(2)
      retries += 1

  # Get Markdown
  markdown = response["markdown"]

  # this page id points to the page housing both the mp3 file and the returned markdown
  add_text_block = {
    "children":
    [{
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{
          "type": "text",
          "text": {
            "content": markdown,
          }
        }]
      }
    }]
  }

  create_response = requests.patch(
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    json=add_text_block, headers=headers)
  return (create_response.json())