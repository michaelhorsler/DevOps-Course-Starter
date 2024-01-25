import requests
import dotenv
import os

dotenv.load_dotenv()

reqUrl = f"https://api.trello.com/1/cards/65799b16c97e67f761ea2042"

query_params={
    "key": os.getenv("TRELLO_API_KEY"),
    "token": os.getenv("TRELLO_API_TOKEN"),
    "idList": os.getenv("TRELLO_DONE_LIST_ID")
}

response = requests.put(reqUrl, params = query_params)

print(response.text)