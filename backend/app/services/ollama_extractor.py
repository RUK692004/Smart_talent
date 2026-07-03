import json
import requests
from typing import Any, Dict, List
from app.services.prompts import RESUME_EXTRACTION_PROMPT


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma2:2b"


def _safe_json_parse(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()
    return json.loads(text)


def try_ollama_extract(cleaned_text: str) -> Dict[str, Any]:
    """
    Attempt to extract structured resume data using Ollama (local LLM).
    Returns same format as extract_structured_data_with_ai().
    """
    if not cleaned_text:
        return {
            "status": "error",
            "message": "Empty text for Ollama extraction",
            "structured_data": {}
        }

    prompt = f"{RESUME_EXTRACTION_PROMPT}\n\n{cleaned_text}"

    try:
        print("OLLAMA EXTRACTOR: calling Ollama")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )
        response.raise_for_status()

        data = response.json()
        raw_text = (data.get("response") or "").strip()

        if not raw_text:
            return {
                "status": "error",
                "message": "Empty Ollama response",
                "structured_data": {}
            }

        print("OLLAMA EXTRACTOR: raw response length =", len(raw_text))

        try:
            parsed = _safe_json_parse(raw_text)
        except Exception as json_error:
            print(f"OLLAMA EXTRACTOR: JSON parse failed: {str(json_error)}")
            return {
                "status": "error",
                "message": f"Ollama returned invalid JSON: {str(json_error)}",
                "structured_data": {}
            }

        if not isinstance(parsed, dict):
            return {
                "status": "error",
                "message": "Ollama returned non-dict JSON",
                "structured_data": {}
            }

        parsed["raw_text"] = cleaned_text

        return {
            "status": "success",
            "message": f"Ollama extraction success using {OLLAMA_MODEL}",
            "structured_data": parsed
        }

    except requests.exceptions.ConnectionError:
        print("OLLAMA EXTRACTOR: Ollama is not running or not installed")
        return {
            "status": "error",
            "message": "Ollama is not running or not installed",
            "structured_data": {}
        }
    except requests.exceptions.Timeout:
        print("OLLAMA EXTRACTOR: Ollama request timed out")
        return {
            "status": "error",
            "message": "Ollama request timed out",
            "structured_data": {}
        }
    except Exception as e:
        print(f"OLLAMA EXTRACTOR: Error: {str(e)}")
        return {
            "status": "error",
            "message": f"Ollama extraction failed: {str(e)}",
            "structured_data": {}
        }