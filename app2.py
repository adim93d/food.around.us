
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os


def get_env_data(env_file_path: str, required_data: str) -> str:
    load_dotenv(dotenv_path=env_file_path)
    return os.getenv(required_data)

def prepare_request(api_req):
    prepared = api_req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    print(response.status_code)
    return json_result


PLANETNET_API_KEY = get_env_data(".env", "PLANETNET_API_KEY")	# Your API_KEY here
PERMAPEOPLE_API_KEY_ID = get_env_data(".env", "PERMAPEOPLE_API_KEY_ID")
PERMAPEOPLE_API_KEY_SECRET = get_env_data(".env", "PERMAPEOPLE_API_KEY_SECRET")

PROJECT = "all"  # try specific floras: "weurope", "canada"…
planenet_api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={PLANETNET_API_KEY}&lang=he"
permapeople_api_endpoint = "https://permapeople.org/api/search"

permapeople_headers = {
    "Content-Type": "application/json",
    "x-permapeople-key-id": PERMAPEOPLE_API_KEY_ID,
    "x-permapeople-key-secret": PERMAPEOPLE_API_KEY_SECRET
}

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

plant_ml_req = requests.Request('POST', url=planenet_api_endpoint, files=files, data=data)
plant_ml_data = prepare_request(plant_ml_req)
pprint(plant_ml_data)


# plant_data = plant_ml_data['results'][3]['species']
# local_name = plant_data['commonNames'][1]
# scientific_name = plant_data['scientificNameWithoutAuthor']
#
# print(scientific_name)
# print(local_name)
#
# permapeople_payload = {
#     "q": scientific_name
# }
#
# permapeople_data = json.dumps(permapeople_payload)
# permapeople_req = requests.Request('POST', url=permapeople_api_endpoint, headers=permapeople_headers, data=permapeople_data)
# permapeople_result = prepare_request(permapeople_req)
#
# edible = permapeople_result['plants'][0]['data'][1].values()
# edible_parts = permapeople_result['plants'][0]['data'][10].values()
#
# print(edible)
# print(edible_parts)




