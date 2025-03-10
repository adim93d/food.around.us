
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import temp
import models
import ai_temp


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

def plant_exists(db, scientific_name: str) -> bool:
    # This query will use the index on scientific_name (if set) and be very efficient.
    return db.query(models.Plant).filter(models.Plant.scientific_name == scientific_name).first() is not None

PLANETNET_API_KEY = get_env_data("../.env", "PLANETNET_API_KEY")	# Your API_KEY here
PERMAPEOPLE_API_KEY_ID = get_env_data("../.env", "PERMAPEOPLE_API_KEY_ID")
PERMAPEOPLE_API_KEY_SECRET = get_env_data("../.env", "PERMAPEOPLE_API_KEY_SECRET")

planenet_api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANETNET_API_KEY}&lang=he"
permapeople_api_endpoint = "https://permapeople.org/api/search"

permapeople_headers = {
    "Content-Type": "application/json",
    "x-permapeople-key-id": PERMAPEOPLE_API_KEY_ID,
    "x-permapeople-key-secret": PERMAPEOPLE_API_KEY_SECRET
}

image_path_1 = "../app/static/flower1.jpg"
image_data_1 = open(image_path_1, 'rb')

image_path_2 = "../app/static/leaf1.jpg"
image_data_2 = open(image_path_2, 'rb')

image_path_3 = "../app/static/leaf2.jpg"
image_data_3 = open(image_path_3, 'rb')

image_path_4 = "../app/static/leaf3.jpg"
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

plant_data = plant_ml_data['results'][3]['species']
scientific_name = plant_data['scientificNameWithoutAuthor']
family_name = plant_data['family']['scientificNameWithoutAuthor']

plants2 = temp.get_all_plants()
if not any(plant["scientific_name"] == scientific_name for plant in plants2):  #Time Complexity: O(n), Need to be change to O(1)
    print("Not in DB")
    print("Gathering information")
    print("Adding to DB")
    temp.post_plant(scientific_name, family_name, True)
else:
    print("Plant in DB")
    print("Fetching Data")
    pprint(ai_temp.ai_response(scientific_name))



