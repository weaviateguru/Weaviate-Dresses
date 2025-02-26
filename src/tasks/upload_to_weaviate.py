
import logging
import argparse
import pandas as pd

from weaviate.exceptions import UnexpectedStatusCodeException
import weaviate.classes as wvc

from src.vector_db.weaviate_db import connect_to_weaviate



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__UPLOAD-DATA-TO-WEAVIATE__")



def create_collection(client, collection_name: str):

    # List all existing collections (returns a list of names, not objects)
    all_colls = client.collections.list_all()
    # Check if collection_name is in that list
    if collection_name in all_colls:
        client.collections.delete(collection_name)
        logger.info(f"Deleted existing '{collection_name}' collection.")

    try:
        collection = client.collections.create(
            name=collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
            generative_config=wvc.config.Configure.Generative.openai(model="gpt-3.5-turbo", max_tokens=512),
            properties=[
                # wvc.config.Property(name="age", data_type=wvc.config.DataType.INT, skip_vectorization=True),
                # wvc.config.Property(name="division_name", data_type=wvc.config.DataType.TEXT),
                # wvc.config.Property(name="class_name", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="clothing_id", data_type=wvc.config.DataType.TEXT, skip_vectorization=True),
                wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="review", data_type=wvc.config.DataType.TEXT),
                wvc.config.Property(name="rating", data_type=wvc.config.DataType.INT, skip_vectorization=True)
        ])
    except UnexpectedStatusCodeException as e:
        logger.error(f"Error creating {collection_name} collection: {e}")


def upload_data(client, collection_name: str, csv_file: str):

    df = pd.read_csv(csv_file)
    logger.info(f"Loaded {len(df)} rows from {csv_file}.")

    # get collection object
    collection = client.collections.get(collection_name)

    # For each row, generate embedding, then upsert the object
    for idx, row in df.iterrows():
        data_object = {
            # "age": int(row["age"]) if not pd.isna(row["age"]) else None,
            # "division_name": row.get("division_name"),
            # "class_name": row.get("class_name"),
            "clothing_id": str(row.get("clothing_id")) if row.get("clothing_id") else None,
            "title": row.get("title"),
            "review": row.get("review"),
            "rating": int(row["rating"]) if not pd.isna(row["rating"]) else None
        }

        try:
            collection.data.insert(data_object)
        except UnexpectedStatusCodeException as e:
            logger.error(f"Error uploading row to DressReview: {e}")

    logger.info("All data uploaded successfully with embeddings.")
   

def opt_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, required=True, help="Path to the uploaded datasets.")
    parser.add_argument('--collection-name', type=str, default="DressReview", help="Collection name for your weaviate database.")

    return parser.parse_args()


if __name__ == "__main__":

    logger.info("Starting upload dataset to weaviate database...")
    args = opt_parser()

    client = connect_to_weaviate()

    create_collection(client=client, collection_name=args.collection_name)
    upload_data(client=client, collection_name=args.collection_name, csv_file=args.source)

    client.close()