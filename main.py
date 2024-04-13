from llm.wrapper import setup_rag_pipeline

from haystack import Pipeline

from getpass import getpass
import argparse
import os
import timeit
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
                        type=str,
                        default='What is the invoice number value?',
                        help='Enter the query to pass into the LLM')
    args = parser.parse_args()

    if "HF_API_TOKEN" not in os.environ:
        os.environ["HF_API_TOKEN"] = getpass("Enter Hugging Face token:")

    start = timeit.default_timer()

    rag_pipeline = setup_rag_pipeline()

    #Execute the query
    json_response = rag_pipeline.run(
        {
            "embedder": {
                "text": args.input
            },
            "prompt_builder": {
                "question": args.input
            },
            "llm": {
                "generation_kwargs": {
                    "max_new_tokens": 350
                }
            }
        }
    )

    end = timeit.default_timer()

    replies = json_response['llm']['replies']
    answer = 'No answer found'
    if replies:
        answer = replies[0].strip()

    print(f'\nAnswer:\n {answer}')
    print('='*50)

    print(f"Time to retrieve answer: {end - start}")

