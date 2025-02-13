
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os


def get_api_key(env_file_path: str) -> str:
    load_dotenv(dotenv_path=env_file_path)
    return os.getenv("API_KEY")

API_KEY = get_api_key(".env")	# Your API_KEY here
PROJECT = "all"  # try specific floras: "weurope", "canada"…
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

image_path_1 = "static/flower1.jpg"
image_data_1 = open(image_path_1, 'rb')

image_path_2 = "static/leaf1.jpg"
image_data_2 = open(image_path_2, 'rb')

image_path_3 = "static/leaf2.jpg"
image_data_3 = open(image_path_3, 'rb')

image_path_4 = "static/leaf3.jpg"
image_data_4 = open(image_path_4, 'rb')

data = { 'organs': ['flower', 'leaf', 'leaf', 'leaf'] }

files = [
  ('images', (image_path_1, image_data_1)),
  ('images', (image_path_2, image_data_2)),
  ('images', (image_path_3, image_data_3)),
  ('images', (image_path_4, image_data_4)),

]

req = requests.Request('POST', url=api_endpoint, files=files, data=data)
prepared = req.prepare()

s = requests.Session()
response = s.send(prepared)
json_result = json.loads(response.text)

pprint(response.status_code)
pprint(json_result)