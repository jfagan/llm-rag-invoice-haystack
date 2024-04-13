from haystack.components.generators import HuggingFaceTGIGenerator

def setup_llm(model_name):
    return HuggingFaceTGIGenerator(model_name)