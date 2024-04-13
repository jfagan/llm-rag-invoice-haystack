# RAG Invoice Data Processing with Llama2, Haystack 2, & Docker

## Credits

This project is based on [Andrej Baranovskij's original work](https://github.com/katanaml/llm-rag-invoice-cpu).

## Changes

- The code has been refactored to integrate with Haystack 2, and now utilizes Llama2 hosted on HuggingFace. This change enhances response times and simplifies the architecture by eliminating the need for a local LLM.
- The application is fully containerized using Docker.
- Response times have significantly improved, and all scenarios in the `prompts-structured` directory are now generating answers.

## Requirements

To run this project, you will need a Hugging Face API token, which should be set in your local environment as follows:

## Requirements

You will need to have a Hugging Face API token in your local environment:

`HF_API_TOKEN=''`


## Quickstart

### RAG runs on Haystack, Weaviate, and HuggingFace

1. Build the Docker images, containers, and services:

`docker-compose up --build`

2. (Optional) Copy text PDF files to the `data` folder. (An example invoice is provided for demo/testing purposes.)

3. Open a new CLI tab and perform the following to SSH into your running container:

- Retrieve your `CONTAINER_ID` with `docker ps`.
- Access the container using `docker exec -it CONTAINER_ID bash`.

4. Run the script to convert PDF documents to vector embeddings and save them in Weaviate vector storage:

`python ingest.py`

5. Run the following script to process inquiries about the data and fetch the answers:

`python main.py "What is the invoice number value?"`