import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_plant_info(scientific_name: str) -> dict:
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

