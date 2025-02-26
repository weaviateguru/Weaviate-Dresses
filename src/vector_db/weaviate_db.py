
import logging

import weaviate
import weaviate.classes as wvc
from weaviate.classes.init import Auth

from src.config import Setting
from src.utils import encode_image_to_base64


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("__WEAVIATE-DB__")




def connect_to_weaviate():
    logger.debug("Connecting to Weaviate...")
    try:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=Setting.WEAVIATE_URL,
            auth_credentials=Auth.api_key(Setting.WEAVIATE_API_KEY),
            headers={"X-OpenAI-Api-key": Setting.OPENAI_API_KEY},
            skip_init_checks=True
        )
        logger.info("Weaviate connection established successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Weaviate: {e}")
        raise


def connect_to_local_weaviate():
    try:
        client = weaviate.connect_to_local(
            host="weaviate",
            port=8080,
            grpc_port=50051
        )
        # client = weaviate.connect_to_local(
        #     host="localhost",
        #     port=8080,
        #     grpc_port=50051
        # )
        logger.info("Weaviate connection established successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to weaviate: {e}")
        raise


def vector_search(collection, embedding, limit: int = 10, distance: bool = True):
    # Perform a nearVector search using the query embedding
    response = collection.query.near_vector(
        near_vector=embedding,
        limit=limit,
        return_metadata=weaviate.classes.query.MetadataQuery(distance=distance), 
    )

    # Extract objects from the response
    results = [
        {"properties": obj.properties, "distance": obj.metadata.distance}
        for obj in response.objects
    ]

    return results


def bm25_search(collection, query: str, limit: int = 10, score: bool = True):
    # Perform a BM25 search using the user query
    response = collection.query.bm25(
        query=query,
        limit=limit,
        return_metadata=weaviate.classes.query.MetadataQuery(score=score),
    )

    # Extract objects from the response
    results = [
        {"properties": obj.properties, "score": obj.metadata.score}
        for obj in response.objects
    ]

    return results


def hybrid_search(collection, query, embedding, alpha: float = 0.5, limit: int = 10, score: bool = True, distance: bool = True):
    # Perform a hybrid search using BM25 and vector search
    response = collection.query.hybrid(
        query=query,
        vector=embedding,
        alpha=alpha,
        limit=limit,
        return_metadata=weaviate.classes.query.MetadataQuery(score=score, distance=distance),
    )

    results = [
        {"properties": obj.properties, "score": obj.metadata.score} #"distance": obj.metadata.distance
        for obj in response.objects
    ]
    
    return results


def generative_ai(collection, query: str, prompt: str, limit: int = 10):

    response = collection.generate.near_text(
        query=query,
        # single_prompt=prompt,
        grouped_task=prompt,
        limit=limit
    )

    results = [
        {"generated": response.generated}
        ] + [
            {"properties": obj.properties} for obj in response.objects
    ]

    return results


def image_search(collection, base64_im0, limit: int = 3):
    response = collection.query.near_image(
        near_image=base64_im0,
        # return_properties=["image", "file_id"],
        limit=limit,
        return_metadata=wvc.query.MetadataQuery(distance=True),  
    )

    results = [
        {"properties": obj.properties}
        for obj in response.objects
    ]

    return results


def filters(collection, limit: int = 5):
    """
    Filters let you include, or exclude, particular objects from your result.
    """
    response = collection.query.fetch_objects(
        filters=wvc.query.Filter.by_property("rating").greater_than(4),
        limit=limit
    )

    return response


def aggregate_data(collection):

    # response = collection.aggreage_over_all(total_count=True)
    response = collection.aggregate.over_all(
        total_count=True,
        filters=wvc.query.Filter.by_property("rating").equal(4)
    )

    return response


if __name__ == "__main__":

    collection_name = "DressReviewGenerated"

    client = connect_to_weaviate()
    collection = client.collections.get(collection_name)
    
    # results = filters(collection=collection)
    results = aggregate_data(collection)
    print(results)