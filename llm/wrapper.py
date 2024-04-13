from haystack.components.builders import PromptBuilder
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.document_stores.weaviate.document_store import WeaviateDocumentStore
from haystack_integrations.components.retrievers.weaviate.embedding_retriever import WeaviateEmbeddingRetriever
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline

import box
import yaml

from llm.llm import setup_llm
from llm.prompts import prompt_template


with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def setup_prompt():
    return PromptBuilder(template = prompt_template)


def setup_embedder(model_name):
    return SentenceTransformersTextEmbedder(model = model_name)


def setup_retriever(doc_store):
    return WeaviateEmbeddingRetriever(document_store=doc_store, top_k=3)


def setup_rag_pipeline():
    document_store = WeaviateDocumentStore(url=cfg.WEAVIATE_URL)

    prompt = setup_prompt()
    llm = setup_llm(cfg.LLM_MODEL)
    embedder = setup_embedder(cfg.EMBEDDINGS)
    retriever = setup_retriever(document_store)

    rag_pipeline = Pipeline()
    rag_pipeline.add_component("embedder", embedder)
    rag_pipeline.add_component("retriever", retriever)
    rag_pipeline.add_component("prompt_builder", prompt)
    rag_pipeline.add_component("llm", llm )

    rag_pipeline.connect("embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "llm")

    return rag_pipeline