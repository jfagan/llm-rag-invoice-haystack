# RAG Invoice Data Processing with Llama2, Haystack 2, & Docker

## Requirements

To run this project, you will need a Hugging Face API token, which should be set in your local environment as follows:

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

## Examples 

`python main.py "What is the invoice seller name, address and tax ID? use this format for the answer {\"seller_name\": {},\"address\": {},\"tax_id\": {}}"`

Answer:
 {"seller_name": "Chapman, Kim and Green", "address": "64731 James Branch Smithmouth, NC 26872", "tax_id": "949-84-9105"}
==================================================
Time to retrieve answer: 3.551683001991478


`python main.py "retrieve invoice IBAN in the format {\"invoice_iban\": {}}"`

Answer:
{"invoice_iban": {"GB50ACIE59715038217063"}}
==================================================
Time to retrieve answer: 9.18394808798621


`python main.py "retrieve two values: net price and gross worth for the second invoice item in this format: {\"net_price\": {},\"gross_worth\": {}}"`

Answer:
{"net_price": {"1.00": 7.50},"gross_worth": {"1.00": 12.99}}
==================================================
Time to retrieve answer: 3.623518834996503


## Credits

This project is based on [Andrej Baranovskij's original work](https://github.com/katanaml/llm-rag-invoice-cpu).

## Changes

- The code has been refactored to integrate with Haystack 2, and now utilizes Llama2 hosted on HuggingFace. This change enhances response times and simplifies the architecture by eliminating the need for a local LLM.
- The application is fully containerized using Docker.
- Response times have significantly improved, and all scenarios in the `prompts-structured` directory are now generating answers.