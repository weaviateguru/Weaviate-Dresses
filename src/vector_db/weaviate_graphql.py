import requests
from src.vector_db.weaviate_db import connect_to_weaviate
from src.embedding import get_embedding
from src.config import Setting





def vector_search(client, collection_name: str, embedding: list, limit: int = 3):
    """
    Find objects with similar vectors.
    Args:
        client (): 
        embedding (list): 
        limit (int): 

    Returns:

    """
    gql_query = f"""
        {{
            Get {{
                {collection_name}(
                    limit: {limit},
                    nearVector: {{
                        vector: {embedding},
                    }}
                ){{
                    title
                    review
                    rating
                    _additional {{
                        distance
                    }}
                }}
            }}
        }}
    """

    response = client.graphql_raw_query(gql_query)
    return response
  


def bm25_search(client, collection_name: str, query, limit: int = 3):

    gql_query = f""" 
        {{
            Get {{
                {collection_name}(
                    limit: {limit},
                    bm25: {{
                        query: "{query}"
                    }}
                ){{
                    title
                    review
                    rating
                    _additional {{
                        score
                    }}
                }}
            }}
        }}
    """

    response = client.graphql_raw_query(gql_query)

    return response



def hybrid_search(client, collection_name: str, query, limit: int = 3, alpha: float = 0.5):

    gql_query = f""" 
        {{
            Get {{
                {collection_name}(
                    limit: {limit},
                    hybrid: {{
                        query: "{query}",
                        alpha: {alpha}
                    }},
                ){{
                    title
                    review
                    rating
                    _additional {{
                        score
                        explainScore
                    }}
                }}
            }}
        }}
    """ 

    response = client.graphql_raw_query(gql_query)
    return response


def generative_ai(client, collection_name: str, query: str, prompt: str, limit: int = 3):

    gql_query = f""" 
        {{
            Get {{
                {collection_name} (
                    nearText: {{
                        concepts: ["{query}"]
                    }}
                    limit: {limit}
                ) {{
                    title
                    review
                    rating
                    _additional {{
                        generate(
                        groupedResult: {{
                            task: \"\"\"
                            {prompt}
                            \"\"\"
                        }}
                        ) {{
                        error
                        groupedResult
                        }}
                    }}
                }}
            }}
        }}
    """
    response = client.graphql_raw_query(gql_query)
    return response


def filters(client, collection_name: str):

    gql_query = f"""
        {{
            Get{{
                {collection_name}(
                limit: 3,
                where: {{
                    path: ["rating"],
                    operator: GreaterThan,
                    valueInt: 0
                }}
                ){{
                    title
                    review
                    rating
                }}
            }}
        }}
    """

    response = client.graphql_raw_query(gql_query)
    return response


# def aggregate(client, collection_name: str):

if __name__ == "__main__":

    client = connect_to_weaviate()
    collection_name = "DressReviewGenerated"
    response = filters(client=client, collection_name=collection_name)
    print(response)