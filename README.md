# Weaviate




### Getting Started
Follow these steps to set up the environment and run the application.
1. Clone the repository.
```
git clone https://github.com/ldebele/Weaviate.git
cd Weaviate
```
2.Create a python virtual environment.
```
python3 -m venv venv
```
3. Activate the virtual environment.
- On Linux and macOS
```
source venv/bin/activate
```
4. Install Dependencies
```
pip install -r requirements.txt
```
5. Run the main app.
```
python3 app/main.py
```

## Setting Up Weaviate with Docker
To start weaviate using Docker Compose, run:
```
docker compose up
```
To stop and remove the containers, run:
```
docker compose down
```

## Tasks
### Generating a Dataset
To generate a dataset, run the following command:
```
docker exec -it weaviate_app python3 src/tasks/generate_data.py --source </path/to/source_images> --output-dir </path/to/output-directory>
```
Example:
```
docker exec -it weaviate_app python3 src/tasks/generate_data.py 
```

### Uploading Data to Weaviate
- #### Uploading Dataset
If you are using the default collection name `DressReview`, run:
```
docker exec -it weaviate_app python src/tasks/upload_to_weaviate.py --source "/path/to/datasets"
```
To specify a custom collection name:
```
docker exec -it weaviate_app python src/tasks/upload_to_weaviate.py --source="/path/to/datasets" --collection-name="<new-collection-name>"
```
- #### Uploading Images
By default, images should be placed in `./static/images` and uploaded to the `DressImages` collection, To upload images, run:
```
docker exec -it weaviate_app python3 app/tasks/upload_to_weaviate.py
```

To upload images to a new collection from a different directory, use:
```
docker exec -it weaviate_app python3 src/tasks/upload_img_to_weaviate.py --source="/path/to/images" --collection-name="<new-collection-name>"
```

### To Access the Website
- To access text search: http://localhost:5050
- To access image search: http://localhost:6060
