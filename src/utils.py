
import base64





def list_collections(client):
    return client.collections.list_all()


def fetch_query(client, collection_name: str):
    # fetch query
    collection = client.collections.get(collection_name)
    query = collection.query.fetch_objects(
                include_vector=True)
    return query


def get_total_data(client, collection_name: str):
    collection = client.collections.get(collection_name)
    response = collection.aggregate.over_all(total_count=True)
    return response.total_count


def encode_image_to_base64(img_path: str):
    with open(img_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def decode_base64_to_image(base64_im0):
    return base64.b64decode(base64_im0)