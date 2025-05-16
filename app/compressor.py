# import google.generativeai as genai
# import json
# import re
# # Assumes you already ran: genai.configure(api_key=...) elsewhere

# def compress_chunks(query: str, candidates: list[dict]) -> list[dict]:
#     context = "\n\n".join([f"[{i+1}] {json.dumps(c)}" for i, c in enumerate(candidates)])

#     prompt = f"""
# You are an AI assistant helping to filter company records for a user query.

# Query:
# "{query}"

# Here are 10 candidate company records:
# {context}

# Return only the records that are most relevant to the query.
# Respond with a valid JSON list of dictionaries, like: [{{...}}, {{...}}].
# Note:- Make sure all the requirements written in the query is fullfilled, if not, then do not write that information in the  output result.
#     """

#     try:
#         model = genai.GenerativeModel("models/gemini-2.0-flash")
#         response = model.generate_content(prompt)
#         # Attempt to extract and parse JSON from the response
#         text = response.text.strip()
#         if text.startswith("```"):
#             text = re.sub(r"^```(?:json)?", "", text).strip()
#             text = re.sub(r"```$", "", text).strip()
#         # Handle case: response includes text around the JSON
#         start = text.find("[{")
#         end = text.rfind("}]") + 2
#         if start != -1 and end != -1:
#             return json.loads(text[start:end])
#         else:
#             return json.loads(text)  # fallback if clean JSON

#     except Exception as e:
#         print(f"❌ Compression failed: {e}")
#         return []
import google.generativeai as genai
import json

# Assumes: genai.configure(...) has been run already

def compress_chunks(query: str, candidates: list[dict]) -> list[dict]:
    relevant_chunks = []
    model = genai.GenerativeModel("models/gemini-2.5-flash-preview-04-17")

    for idx, candidate in enumerate(candidates, 1):
        prompt = f"""
            You are an AI assistant helping to filter company records for a user query.

            ### Query:
            {query}

            ### Company Record:
            {json.dumps(candidate)}

            Does this record fully meet the requirements described in the query?

            Respond strictly with:
            - Yes → if it satisfies the query
            - No → if it does not

            Do NOT add explanation or extra text.
        """

        try:
            response = model.generate_content(prompt)
            answer = response.text.strip().lower()
            print(f"[{idx}] LLM answer: {answer}")

            if "yes" in answer:
                relevant_chunks.append(candidate)

        except Exception as e:
            print(f"[{idx}] ❌ LLM filtering failed: {e}")

    return relevant_chunks
