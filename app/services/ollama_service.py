import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL")

def check_if_edible(species_name: str) -> bool:
    prompt = f"Is the plant '{species_name}' edible? Answer only 'Yes' or 'No'."

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3.2",  # Assuming you pulled llama3.2
                "prompt": prompt,
                "stream": False  # We want full response, not streaming
            }
        )
        response.raise_for_status()
        result_text = response.json().get("response", "").strip().lower()
        return result_text
        # if "yes" in result_text:
        #     return True
        # elif "no" in result_text:
        #     return False
        # else:
        #     # Fallback if uncertain
        #     return False

    except Exception as e:
        print(f"Ollama check failed: {str(e)}")
        # Default to False if something goes wrong
        return False