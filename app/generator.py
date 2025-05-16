import google.generativeai as genai
from app.config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def generate_answer(contexts, query):
    context_text = "\n\n".join([f"{i+1}. {doc}" for i, doc in enumerate(contexts)])
    prompt = f"""Given the following company data:\n{context_text}\n\nAnswer the user's question:\n{query}"""
    response = model.generate_content(prompt)
    return response.text.strip()
