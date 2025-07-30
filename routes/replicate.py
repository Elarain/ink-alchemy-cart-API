from flask import Blueprint, jsonify, g, request
from dotenv import load_dotenv
import replicate
import os

# Load environment variables from .env file
load_dotenv()

replicate_bp = Blueprint('replicate', __name__)

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
MODEL_ID = "google/imagen-4"
MODEL_VERSION = "111arpt4pnrma0cpydtr8n0qx0"  # replace with latest if needed

@replicate_bp.route('/replicate/generate', methods=['POST'])
def generate():
    print("Received request to generate image using Replicate API")
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        output = replicate.run(
            "google/imagen-4",
            input={
                "prompt": prompt
            }
        )
        return jsonify({"image-url": output.url})  # typically a list of image URLs

    except Exception as e:
        return jsonify({"error": "Replicate API error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error", "message": str(e)}), 500
