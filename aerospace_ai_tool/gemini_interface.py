
import os
import google.generativeai as genai
import requests

class GeminiAPI:
    def __init__(self, api_key=None, model_name="models/gemini-1.5-pro-latest", openrouter_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.openrouter_key = openrouter_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError('GEMINI_API_KEY not set in environment or passed to GeminiAPI')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def ask(self, prompt, system_instructions=None):
        full_prompt = prompt
        if system_instructions:
            full_prompt = f"System: {system_instructions}\nUser: {prompt}"
        try:
            response = self.model.generate_content(full_prompt)
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'candidates'):
                return response.candidates[0].text
            return str(response)
        except Exception as e:
            # Fallback to OpenRouter if Gemini fails
            return self.ask_openrouter(full_prompt)

    def ask_openrouter(self, prompt, model="meta-llama/llama-3-70b-instruct"):
        if not self.openrouter_key:
            return "OpenRouter API key not set."
        url = "https://openrouter.ai/api/v1/chat"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"OpenRouter error: {e}"
