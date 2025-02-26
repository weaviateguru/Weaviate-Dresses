
import os
import logging
from pathlib import Path

from src.config import Setting
from flask import Flask, request, render_template
from src.embedding import get_embedding
from src.utils import encode_image_to_base64
from src.vector_db.weaviate_db import (
    connect_to_weaviate, 
    connect_to_local_weaviate,
    vector_search, 
    bm25_search, 
    hybrid_search,
    generative_ai,
    image_search,
)



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent



app = Flask(__name__, 
            template_folder=str(BASE_DIR /"templates"),
            static_folder=str(BASE_DIR / "static"))



@app.before_request
def startup_function():
    # connect to weaviate
    try:
        global client
        global wvc_client
        client = connect_to_local_weaviate()
        wvc_client = connect_to_weaviate()
    except Exception as e:
        logger.critical("Critical failure in connecting to Weaviate. Exiting.")
        raise SystemExit(e)


# Close Weaviate client when app shuts down
@app.teardown_appcontext
def close_weaviate_client(exception):
    client.close()
    wvc_client.close()


@app.route("/text", methods=["GET", "POST"])
def home():
    """
    Handle both the search form and the search results on the same page.
    """
    results = []
    user_query = ""
    collection_name = "DressReviewGenerated"    
    search_method = request.form.get("search_method", "vector") 

    if request.method == "POST":
        user_query = request.form.get("query", "")
        search_method = request.form.get("search_method", "vector")
        logger.debug(f"Received search query: {user_query} with method: {search_method}")

        collection = wvc_client.collections.get(collection_name)
        # Generate embedding for the user query
        query_embedding = get_embedding(user_query)
        if not query_embedding:
            return "Error: Failed to generate embedding for the query.", 500

        try:
            if search_method == "vector":
                results = vector_search(collection=collection,
                                        embedding=query_embedding,
                                        limit=10,
                                        distance=True)
               
            elif search_method == "bm25":
                results = bm25_search(collection=collection,
                                      query=user_query,
                                      limit=10,
                                      score=True)

            elif search_method == "hybrid":
                results = hybrid_search(collection=collection, 
                                        query=user_query,
                                        embedding=query_embedding,
                                        alpha=0.5,
                                        limit=10,
                                        score=True,
                                        distance=True)

            elif search_method == "hybrid_0.25":
                results = hybrid_search(collection=collection,
                                         query=user_query,
                                         embedding=query_embedding,
                                         alpha=0.25,
                                         limit=10,
                                         score=True,
                                         distance=True)

            elif search_method == "hybrid_0.75":
                results = hybrid_search(collection=collection,
                                        query=user_query,
                                        embedding=query_embedding,
                                        alpha=0.75,
                                        limit=10,
                                        score=True,
                                        distance=True)

            elif search_method == "gen_ai":
                results = generative_ai(collection=collection,
                                        query=user_query,
                                        prompt=Setting.RECOMMENDATION_PROMPT,
                                        limit=3)


            logger.debug(f"Search results: {results}")

        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return f"Error during search: {e}", 500

    # Render the combined template
    logger.debug("Rendering home page with results.")
    return render_template("search.html", query=user_query, results=results, search_method=search_method)


@app.route("/image", methods=["GET", "POST"])
def upload():
    """
    Handle both the search form and the search results on the same page.
    """
    results = []
    collection_name = "DressImages"

    if request.method == "POST":
        # if 'image' not in request.files['image']:
        #     return "No Selected file", 400
        
        file = request.files['image']
        if file.filename == "":
            return "No selected file", 400

        uploaded_folder = './uploaded'
        os.makedirs(uploaded_folder, exist_ok=True)
        try:
            file_path = os.path.join(uploaded_folder, file.filename)
            file.save(file_path)

            base64_im0 = encode_image_to_base64(file_path)

            collection = client.collections.get(collection_name)

            results = image_search(
                collection=collection,
                base64_im0=base64_im0,
                limit=10
            )

        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return f"Error during search: {e}", 500

    # Render the combined template
    logger.debug("Rendering home page with results.")
    return render_template("search_image.html", results=results)



if __name__ == "__main__":
    logger.debug("Starting Flask app...")
    app.run(host="0.0.0.0", port=6060, debug=True)
