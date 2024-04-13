from haystack.components.writers import DocumentWriter
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentSplitter, DocumentCleaner
from haystack.components.routers import FileTypeRouter
from haystack.components.joiners import DocumentJoiner
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack_integrations.document_stores.weaviate.document_store import WeaviateDocumentStore
from pathlib import Path
from dotenv import load_dotenv
import box
import yaml

load_dotenv()

# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

#Vector Database
document_store = WeaviateDocumentStore(url=cfg.WEAVIATE_URL)

input_dir = cfg.DATA_PATH

#Document Processors 
file_type_router = FileTypeRouter(mime_types=["application/pdf"])
pdf_converter = PyPDFToDocument()
document_joiner = DocumentJoiner()


document_cleaner = DocumentCleaner() 

document_splitter = DocumentSplitter(split_by="word", split_length=cfg.PRE_PROCESSOR_SPLIT_LENGTH, split_overlap=cfg.PRE_PROCESSOR_SPLIT_OVERLAP)

#Sentence Embeddings
document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2") #Will create the embeddings
document_writer = DocumentWriter(document_store) #Will write the docs to the vector store 

#Build processing pipeline
preprocessing_pipeline = Pipeline()
preprocessing_pipeline.add_component(instance=file_type_router, name="file_type_router")
preprocessing_pipeline.add_component(instance=pdf_converter, name="pypdf_converter")
preprocessing_pipeline.add_component(instance=document_joiner, name="document_joiner")
preprocessing_pipeline.add_component(instance=document_cleaner, name="document_cleaner")
preprocessing_pipeline.add_component(instance=document_splitter, name="document_splitter")
preprocessing_pipeline.add_component(instance=document_embedder, name="document_embedder")
preprocessing_pipeline.add_component(instance=document_writer, name="document_writer")

#Connect the pipeline components
preprocessing_pipeline.connect("file_type_router.application/pdf", "pypdf_converter.sources")
preprocessing_pipeline.connect("pypdf_converter", "document_joiner")
preprocessing_pipeline.connect("document_joiner", "document_cleaner")
preprocessing_pipeline.connect("document_cleaner", "document_splitter")
preprocessing_pipeline.connect("document_splitter", "document_embedder")
preprocessing_pipeline.connect("document_embedder", "document_writer")

#Ingest the docs
res = preprocessing_pipeline.run({"file_type_router": {"sources": list(Path(input_dir).glob("**/*"))}})

print(res)