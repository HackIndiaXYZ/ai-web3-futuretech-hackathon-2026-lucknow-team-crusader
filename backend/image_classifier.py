import os
import json
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def classify_leaf_image(image_bytes: bytes) -> dict:
    """Uses Gemini Vision with rate-limit avoidance and explicit JSON forcing."""
    
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
    
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = (
        "Analyze this farm image. Identify what is in the image (e.g., 'Freshly Harvested Potatoes', 'Healthy Wheat', 'Tomato Blight', 'Dry Dirt'). "
        "Return ONLY a valid JSON object with two keys: 'predicted_label' (string) and 'confidence' (integer 0-100)."
    )
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inlineData": {
                        "mimeType": "image/jpeg", 
                        "data": encoded_image
                    }
                }
            ]
        }],
        # This officially forces Google's API to only return clean JSON
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    try:
        # Increased timeout to 30s just in case the image takes a second to upload
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        data = response.json()
        
        # If Google blocks us, catch it so we don't silently fail to 0 confidence!
        if "error" in data:
            print(f"\n[GOOGLE API ERROR]: {data['error'].get('message')}")
            return {"predicted_label": f"API Error: {data['error'].get('message')}", "confidence": 0}
            
        raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        return json.loads(raw_text)
        
    except KeyError:
        print(f"\n[Unexpected API Response]: {data}")
        return {"predicted_label": "Error parsing Google response", "confidence": 0}
    except Exception as e:
        print(f"\n[System Error]: {e}")
        return {"predicted_label": "System connection failed", "confidence": 0}
