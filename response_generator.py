from groq import Groq
from emotion_context import analyze_emotion_context
from dotenv import load_dotenv
import os

load_dotenv()

client = None


def get_client():
    global client
    if client is None:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return client


def generate_response(message, emotion):

    context = analyze_emotion_context()

    extra_instruction = ""

    if context == "persistent_sadness":
        extra_instruction = "The user seems emotionally distressed. Respond with extra empathy and encouragement."

    elif context == "persistent_anger":
        extra_instruction = "The user seems frustrated. Respond calmly and help de-escalate the situation."

    elif context == "persistent_fear":
        extra_instruction = "The user seems anxious. Provide reassurance and supportive advice."

    # Handle greetings quickly without LLM
    if message.lower() in ["hi", "hello", "hey"]:
        return "Hello! 😊 How are you feeling today?"

    prompt = f"""
You are an emotionally intelligent AI assistant.

Detected user emotion: {emotion}
Emotion context: {context}

User message:
{message}

Instructions:
- Respond empathetically
- Acknowledge the user's feelings
- Keep the reply SHORT (2–3 sentences maximum)
- Be conversational and supportive
- Do NOT give long explanations
- {extra_instruction}
"""

    completion = get_client().chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=80
    )

    return completion.choices[0].message.content