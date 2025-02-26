import os
import csv
import json
import base64
import openai
import logging
import argparse
from glob import glob
from datetime import datetime
from pydantic import BaseModel
from openai import OpenAI

from src.config import Setting
from src.utils import encode_image_to_base64



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__DATASET-GENERATION__")


client = OpenAI(api_key=Setting.OPENAI_API_KEY)


class ProductReview(BaseModel):
    title: str
    review: str
    rating: float


def save_to_csv(data, saved_path):
    """save the generated review datasets into csv file."""
    file_exists = os.path.isfile(saved_path)
    is_empty = not file_exists or os.stat(saved_path).st_size == 0

    with open(saved_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        # writer header only if the file is empty.
        if is_empty:
            writer.writeheader()

        writer.writerow(data)


def generate_review_from_image(img_path: str, 
                               model_id: str = "gpt-4o-mini",
                               max_tokens: int = 512,
                               temperature: float = 0.7):

    # encode image to base46
    base64_img = encode_image_to_base64(img_path)

    try:
        # generate a response
        response = client.beta.chat.completions.parse(
            model=model_id,
            messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": Setting.REVIEW_GENERATION_PROMPT,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg; base64, {base64_img}",
                                },
                            },

                        ],
                    },
                ],

            response_format=ProductReview,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.parsed

    except Exception as e:
        logger.info(f"Error occurred while generating product review: {e}")
        raise


def opt_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str,default='./static/images', help="Path to the source images.")
    parser.add_argument("--output-dir", type=str, default='./data', help="Path to saved directory.")

    return parser.parse_args()


if __name__ == "__main__":

    logger.info("Starting generate datasets...")
    args = opt_parser()

    # generate timestamp to save the generated datasets.
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d_%H-%M%-S")
    saved_path = os.path.join(args.output_dir, f"{date_time_str}.csv")

    # create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    imgs_paths = glob(f'{args.source}/*.jpg') + glob(f'{args.source}/*.png') + glob(f'{args.source}/*.jpeg')
    for img_path in imgs_paths:
        base_filename = os.path.basename(img_path)
        file_id, _ = os.path.splitext(base_filename)

        response = generate_review_from_image(img_path)
        logger.info(f"Product review successfully generated for file: {img_path}")
        data = {
            "clothing_id": file_id,
            "title": response.title,
            "review": response.review,
            "rating": response.rating
        }
        
        save_to_csv(data=data, saved_path=saved_path)
        logger.info("Response data successfully saved.")

    logger.info(f"All product review successfully generated and saved at: {saved_path}")