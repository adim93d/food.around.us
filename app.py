
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os


def get_api_key(env_file_path: str) -> str:
    load_dotenv(dotenv_path=env_file_path)
    return os.getenv("API_KEY")

# API_KEY = "YOUR-PRIVATE-API-KEY-HERE"	# Your API_KEY here
PROJECT = "all"; # try specific floras: "weurope", "canada"…
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

image_path_1 = "../data/image_1.jpeg"
image_data_1 = open(image_path_1, 'rb')

image_path_2 = "../data/image_2.jpeg"
image_data_2 = open(image_path_2, 'rb')

data = { 'organs': ['flower', 'leaf'] }

files = [
  ('images', (image_path_1, image_data_1)),
  ('images', (image_path_2, image_data_2))
]

req = requests.Request('POST', url=api_endpoint, files=files, data=data)
prepared = req.prepare()

s = requests.Session()
response = s.send(prepared)
json_result = json.loads(response.text)

pprint(response.status_code)
pprint(json_result)