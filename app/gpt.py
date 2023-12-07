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
