# app/services/ai_service.py
import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_plant_edibility(scientific_name: str) -> dict:
    prompt = (
        f"Is the plant {scientific_name} edible? If edible, provide the response in a JSON object with the key "
        "'is_edible'."
    )

    messages = [{"role": "user", "content": prompt}]

    functions = [
        {
            "name": "parse_plant_info",
            "description": "Parses plant information into a structured JSON object.",
            "parameters": {
                "type": "object",
                "properties": {
                    "is_edible": {
                        "type": "boolean",
                        "description": "True if the plant is edible, otherwise False."
                    }
                },
                "required": ["is_edible"]
            }
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        function_response = response.choices[0].message.function_call
        if function_response:
            arguments = json.loads(function_response.arguments)
            return arguments.get('is_edible')
        else:
            raise Exception("No function call returned from the API response.")
    except Exception as e:
        raise Exception(f"Error when calling OpenAI API: {e}")


def get_detailed_plant_info(scientific_name: str) -> dict:
    prompt = (
        f"Is the plant {scientific_name} edible? If edible, provide the response in a JSON object with the keys "
        "'edible', 'edible_parts', and 'safety'."
    )

    messages = [{"role": "user", "content": prompt}]

    functions = [
        {
            "name": "parse_plant_info",
            "description": "Parses plant information into a structured JSON object.",
            "parameters": {
                "type": "object",
                "properties": {
                    "edible": {
                        "type": "boolean",
                        "description": "True if the plant is edible, otherwise False."
                    },
                    "edible_parts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of edible parts of the plant."
                    },
                    "safety": {
                        "type": "string",
                        "description": "Preparation and safety considerations for consuming the plant."
                    }
                },
                "required": ["edible", "edible_parts", "safety"]
            }
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        message = response.choices[0].message

        if message.function_call:
            print("[AI] Got function_call")
            try:
                arguments = json.loads(message.function_call.arguments)
                print("[AI] Parsed function_call JSON:", arguments)
                return arguments
            except Exception as e:
                raise Exception(f"[AI] Failed to parse function_call JSON: {e}")

        elif message.content:
            print("[AI] Got content:", message.content)
            try:
                return json.loads(message.content)
            except json.JSONDecodeError:
                json_match = re.search(r'\{[\s\S]*\}', message.content)
                if not json_match:
                    raise Exception("[AI] No valid JSON block found in content.")
                json_str = json_match.group(0)
                try:
                    arguments = json.loads(json_str)
                    print("[AI] Parsed extracted JSON:", arguments)
                    return arguments
                except json.JSONDecodeError as je:
                    raise Exception(f"[AI] Failed to parse extracted JSON: {je}")
            except Exception as e:
                raise Exception(f"[AI] Unexpected error parsing content: {e}")

        else:
            raise Exception("[AI] OpenAI response had no function_call and no content")

    except Exception as e:
        print("[get_detailed_plant_info] ERROR:", e)
        raise Exception(f"Error when calling OpenAI API: {e}")
