import openai
from typing import Optional
openai.api_key = "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"
def generate_story_part(prompt: str) -> Optional[str]:
    try:
        response = openai.Completion.create(
            engine="davinci",  # ou outro motor apropriado
            prompt=prompt,
            max_tokens=100  # ajuste conforme necessário
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Erro na geração da história: {e}")
        return None