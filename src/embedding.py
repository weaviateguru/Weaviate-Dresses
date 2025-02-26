
import logging
# import openai
from openai import OpenAI

from src.config import Setting


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__EMBEDDING__")


client = OpenAI(api_key=Setting.OPENAI_API_KEY)



def get_embedding(text: str):
    """Create an embedding from text."""
    if not text:
        logger.warning("Received empty text for embedding.")
        return None
    try:
        logger.debug(f"Generating embedding for text: {text}")
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small",
        )
        logger.debug("Embedding successfully generated.")
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise
