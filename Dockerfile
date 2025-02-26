# Use Python 3.11 as base image
FROM python:3.11.1-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY ./src ./src
COPY ./static ./static
COPY ./templates ./templates

# set PYTHONPATH
ENV PYTHONPATH="/app/src:/app"

RUN mkdir uploads

CMD ["python", "src/main.py"]



