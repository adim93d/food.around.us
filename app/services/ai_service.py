import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_plant_edibility(scientific_name: str) -> dict:
    """
    Determines plant information by calling the OpenAI API using function calling.

    The function returns a dictionary with the following key:
      - is_edible (bool): True if the plant is edible, otherwise False.

    Args:
        scientific_name (str): The scientific name of the plant.

    Returns:
        dict: A dictionary containing the plant information.

    Raises:
        Exception: If the API call fails or no function call is returned.
    """
    prompt = (
        f"Is the plant {scientific_name} edible? If edible, provide the response in a JSON object with the key "
        "'is_edible'."
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

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
            model="gpt-4-0613",  # Ensure you use a model that supports function calling
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        function_response = response.choices[0].message.function_call
        if function_response:
            # Use dot notation to access the 'arguments' attribute
            arguments = json.loads(function_response.arguments)
            return arguments.get('is_edible')
        else:
            raise Exception("No function call returned from the API response.")
    except Exception as e:
        raise Exception(f"Error when calling OpenAI API: {e}")


def get_detailed_plant_info(scientific_name: str) -> dict:
    """
    Determines plant information by calling the OpenAI API using function calling.
    Returns a dictionary with keys: 'edible', 'edible_parts', and 'safety'.
    """
    prompt = (
        f"Is the plant {scientific_name} edible? If edible, provide the response in a JSON object with the keys "
        "'edible', 'edible_parts', and 'safety'."
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

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
            model="gpt-4-0613",  # Use a model that supports function calling.
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        message = response.choices[0].message

        # If a function call is returned, parse its arguments.
        if message.function_call:
            arguments = json.loads(message.function_call.arguments)
            return arguments
        # Otherwise, if plain content is returned, try to parse that as JSON.
        elif message.content:
            try:
                arguments = json.loads(message.content)
                return arguments
            except Exception as e:
                raise Exception(f"Could not parse message content as JSON: {e}")
        else:
            raise Exception("No function call or content returned from the API response.")
    except Exception as e:
        raise Exception(f"Error when calling OpenAI API: {e}")


if __name__ == "__main__":
    try:

        detailed_result = get_detailed_plant_info("Malva sylvestris")
        print("\nDetailed Info:")
        print("Edible:", detailed_result.get("edible"))
        print("Edible parts:", detailed_result.get("edible_parts"))
        print("Safety:", detailed_result.get("safety"))
    except Exception as error:
        print(error)
