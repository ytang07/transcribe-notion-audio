import requests

headers = {
    'Content-Type': "application/json"
}
body = {
    "url": "https://www.notion.so/69f267134bd44249817339cad1a2e140#6575059dc4f14ead922e8e09f0afee6b"
}
response = requests.post("http://127.0.0.1:5000/", headers=headers, json=body)
print(response.text)