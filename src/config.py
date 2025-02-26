
import os
from dotenv import load_dotenv, find_dotenv



_ = load_dotenv(find_dotenv("./.config/.env"))


class Setting:
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "")
    WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY', "")
    WEAVIATE_URL = os.environ.get('WEAVIATE_URL', "")


    REVIEW_GENERATION_PROMPT = """ 
        write a stylish product title of this image, also analyze the dress in the provided image and write a detailed review. Include the following points:

        Personal Preference: Explain why I might like or dislike this dress based on its design, color, fit, and overall appeal.
        Age Suitability: Identify the age group best suited for this dress.
        Occasions: Suggest the best occasions to wear this dress, such as formal events, casual outings, or special celebrations.
        Energy & Confidence Level: Describe the vibe this dress gives off—does it make me feel bold and empowered, elegant and refined, playful and fun, or another mood?
        Ensure the review is engaging, insightful, and fashion-forward!"
    """
    
    # REVIEW_GENERATION_PROMPT = """
    #     write a nice product title of this image, also a great review in a very colloquial way.
    # """

    # REVIEW_GENERATION_PROMPT = """ 
    #     write a nice product title of this image, also a great review in a very colloquial way, focus on the confidence and energy level of the dress in the image. 
    # """

    # REVIEW_GENERATION_PROMPT = """ 
    #     write a chic product title of this image, also a review that describe how wearing this dress makes me feel.
    # """

    # REVIEW_GENERATION_PROMPT = """ 
    #     You are a creative product title and review generator. 
    #     I will provide you with an image and you will create an appealing and catchy product title that encapsulates the essence of the item. 
    #     Following the title, you will write a casual and relatable review that highlights the product's features and benefits in everyday language. 
    #     Keep the tone friendly and engaging, as if you're sharing your thoughts with a close friend. Make sure to reflect on personal experiences, desired outcomes, and any standout qualities of the product
    # """
    # 

    RECOMMENDATION_PROMPT = """
        Summarize the following user review: {review}. In the response, please 
        start with "Our recommendations " then references the query to address user's needs. 
        In the summary, avoid the words reviewer or review, end with a suggestion of choosing
        based on different occasions 
    """
