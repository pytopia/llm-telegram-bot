import os

from openai import OpenAI

assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt: str, model: str = "gpt-4o-mini", system_prompt: str = "You are a helpful assistant.") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
