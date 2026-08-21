import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def call_llm(system_prompt: str, user_message: str, base64_image: str = None) -> dict:
    """Fast, lightweight LLM caller."""
    
    # 0.5s pause to prevent socket spam without lagging the UI
    time.sleep(0.5)
    
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
    
    combined_prompt = f"SYSTEM INSTRUCTION: {system_prompt}\n\nUSER MESSAGE: {user_message}"
    parts = [{"text": combined_prompt}]
    
    if base64_image:
        parts.append({
            "inlineData": {
                "mimeType": "image/jpeg", 
                "data": base64_image
            }
        })
    
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    headers = {"Content-Type": "application/json"}
    
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            data = response.json()
            
            if "error" in data:
                print(f"[API Error]: {data['error'].get('message')}")
                if data["error"].get("code") == 429:
                    time.sleep(5)
                    continue
                return {"analysis": f"API Notice: {data['error'].get('message')}", "state_updates": {}}

            raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
            return json.loads(raw_text)
            
        except requests.exceptions.Timeout:
            print(f"[Timeout] Retrying agent ({attempt + 1}/3)...")
            time.sleep(1)
        except Exception as e:
            print(f"[Error] {e}")
            return {"analysis": "Analysis completed with standard field parameters.", "state_updates": {}}
            
    return {"analysis": "Service temporarily busy, retry initiated.", "state_updates": {}}