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

        # Handle function_call (structured JSON)
        if message.function_call:
            print("[AI] Got function_call")
            try:
                arguments = json.loads(message.function_call.arguments)
                print("[AI] Parsed function_call JSON:", arguments)
                return arguments
            except Exception as e:
                raise Exception(f"[AI] Failed to parse function_call JSON: {e}")

        # Handle plain content (fallback)
        elif message.content:
            print("[AI] Got content:", message.content)
            try:
                arguments = json.loads(message.content)
                print("[AI] Parsed content JSON:", arguments)
                return arguments
            except Exception as e:
                raise Exception(f"[AI] Could not parse message.content as JSON: {e}")

        # Neither function_call nor content
        else:
            raise Exception("[AI] OpenAI response had no function_call and no content")

    except Exception as e:
        print("[get_detailed_plant_info] ERROR:", e)
        raise Exception(f"Error when calling OpenAI API: {e}")
