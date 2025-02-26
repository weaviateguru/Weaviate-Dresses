
import os
import glob
import logging
import argparse

import weaviate.classes as wvc
from weaviate.util import generate_uuid5
from weaviate.exceptions import UnexpectedStatusCodeException

from src.utils import list_collections
from src.utils import encode_image_to_base64
from src.vector_db.weaviate_db import connect_to_local_weaviate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__UPLOAD-IMAGE-TO-WEAVIATE__")



def create_collection(client, collection_name: str):
    # List all existing collections (returns a list of names, not objects)
    all_colls = list_collections(client)
    if collection_name in all_colls:
        client.collections.delete(collection_name)
        logger.info(f"Deleted existing '{collection_name}' collection.")

    try:
        client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.img2vec_neural(image_fields=["image"]),
            vector_index_config=wvc.config.Configure.VectorIndex.hnsw(distance_metric=wvc.config.VectorDistances.COSINE),
            # vectorizer_config=wvc.config.Configure.Vectorizer.img2vec-neural(
            #     image_fields=[wvc.config.Img2VecField(name="image", weight=1.0)],   
            # ),
            # vectorizer_config=wvc.config.Configure.Vectorizer.multi2vec_clip(
            #     image_fields=[wvc.config.Multi2VecField(name="image", weight=1.0)],   
            # ),
            properties=[
                wvc.config.Property(name="image", data_type=wvc.config.DataType.BLOB),
                wvc.config.Property(name="file_id", data_type=wvc.config.DataType.TEXT, skip_vectorization=True),
            ],
        )
        logger.info("weaviate collection successfully created.")
    except UnexpectedStatusCodeException as e:
        logger.error(f"Error creating {collection_name} collection: {e}")


def upload_image(client, collection_name: str, img_path: str, batch_size: int = 2):
    collection = client.collections.get(collection_name)

    with collection.batch.fixed_size(batch_size) as batch:
        for img_path in glob.glob(f"{img_path}/*.jpg"):
            base64_img = encode_image_to_base64(img_path)

            file = img_path.split('/')[-1]
            filename, ext = os.path.splitext(file)

            data = {
                "image": base64_img,
                "file_id": filename
            }
            try:
                batch.add_object(
                    properties=data,
                    uuid=generate_uuid5(data)
                )
            except UnexpectedStatusCodeException as e:
                logger.error(f"Error uploading row to DressReview: {e}")

    logger.info("All images uploaded successfully to weaviate database.")


def opt_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, default="./static/images", help="Path to the uploaded images.")
    parser.add_argument("--collection-name", type=str, default="DressImages", help="Collection name for your weaviate database.")

    return parser.parse_args()

   

if __name__ == "__main__":

    logger.info("Starting upload images to weaviate database....")
    
    args = opt_parser()

    client = connect_to_local_weaviate()
    create_collection(client=client, collection_name=args.collection_name)
    upload_image(client=client, collection_name=args.collection_name, img_path=args.source)

    client.close()
