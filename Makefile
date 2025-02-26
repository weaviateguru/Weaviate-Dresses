
# Define interpreter
PYTHON = python3

# Export Python path
export PYTHONPATH := $(PWD)

all: run

# run the main app
run:
	$(PYTHON) app/main.py 

# to upload the datasets to weaviate vector database.
upload:
	$(PYTHON) app/tasks/upload_to_weaviate.py

# to generate data for datasets.
generate_data:
	$(PYTHON) app/tasks/generate_data.py

# create a virtual environment
venv:
	rm -rf venv
	$(PYTHON) -m venv venv
	@echo "Virtual environment created."

# install dependencies
install:
	pip install -r requirements.txt
	@echo "Dependencies installed."

# clean up generated files
clean:
	deactivate
	rm -rf __pycache__ venv
	@echo "Cleaned up."

