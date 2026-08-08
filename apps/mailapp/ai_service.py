import requests
import json
import logging

logger = logging.getLogger(__name__)


def generate_or_refine_email(prompt, action='generate', provider='gemini', api_key='', tone='professional'):
    """
    Multi-LLM Service supporting Google Gemini, OpenAI GPT-4o, Anthropic Claude, Groq Llama, and Offline Fallback.
    Actions: 'generate', 'polish', 'summarize', 'professional', 'persuasive', 'short'
    """
    prompt = (prompt or '').strip()
    if not prompt:
        return "Please provide an email draft or prompt to process."

    # Construct System Prompt based on tone and action
    tone_instructions = {
        'professional': "Maintain a professional, clear, and polite corporate tone.",
        'persuasive': "Use a compelling, enthusiastic, and persuasive tone.",
        'short': "Keep the message very concise, direct, and under 4 sentences.",
        'casual': "Use a friendly, relaxed, and approachable conversational tone.",
    }.get(tone, "Maintain a clear and polished email format.")

    if action == 'generate':
        system_prompt = f"You are an expert AI email copywriter. Write a complete, high quality email based on this request. {tone_instructions} Do not include place-holder tags like [Your Name] if user info is obvious."
    elif action == 'polish':
        system_prompt = f"You are an expert editor. Polish and improve the grammar, structure, and readability of the following email draft. {tone_instructions}"
    elif action == 'summarize':
        system_prompt = "Provide a concise summary of the key points in this email text."
    else:
        system_prompt = f"Rewrite this email to make it {action}. {tone_instructions}"

    # Try live provider call if API key provided
    if provider == 'gemini' and api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{
                    "parts": [{"text": f"{system_prompt}\n\nTask/Email: {prompt}"}]
                }]
            }
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}")

    elif provider == 'openai' and api_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.warning(f"OpenAI API call failed: {e}")

    elif provider == 'claude' and api_key:
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            payload = {
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 1000,
                "system": system_prompt,
                "messages": [{"role": "user", "content": prompt}]
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                return resp.json()['content'][0]['text']
        except Exception as e:
            logger.warning(f"Claude API call failed: {e}")

    elif provider == 'groq' and api_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                return resp.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.warning(f"Groq API call failed: {e}")

    # Smart Built-in Fallback Generator (Guarantees responsive output even without API key)
    if action == 'generate':
        return (
            f"Dear Recipient,\n\n"
            f"I hope this message finds you well.\n\n"
            f"{prompt}\n\n"
            f"Please let me know if you need any additional information or have any questions.\n\n"
            f"Best regards,\nRina Nose"
        )
    elif action in ['polish', 'professional']:
        cleaned = prompt.strip()
        if not cleaned.lower().startswith(('dear', 'hi', 'hello')):
            cleaned = f"Hi,\n\n{cleaned}"
        if not cleaned.lower().endswith(('regards', 'sincerely', 'thanks')):
            cleaned += "\n\nThank you,\nBest regards"
        return cleaned
    elif action == 'short':
        words = prompt.split()
        shortened = " ".join(words[:25])
        return f"{shortened}...\n\nThanks,\nRina Nose"

    return prompt
