from google import genai
from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)
from logger import logger


def generate_response(full_prompt):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config={
                "temperature": TEMPERATURE,
                "max_output_tokens": MAX_OUTPUT_TOKENS,
                "top_p": 0.9,
            },
        )

        if not response or not response.text:
            logger.warning("Empty response from Gemini.")
            return "Unable to generate a response at the moment. Please try again."

        final_text = response.text.strip()

        # If model got cut due to token limit, make it explicit
        if not final_text.endswith((".", "!", "?", ":")):
            final_text += "\n\n(Note: Response truncated due to output limit.)"

        logger.info("Gemini response generated successfully.")
        return final_text

    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return "System is temporarily unavailable. Please try again shortly."