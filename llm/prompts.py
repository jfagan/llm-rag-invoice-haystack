# Note: Precise formatting of spacing and indentation of the prompt template is important,
# as it is highly sensitive to whitespace changes. For example, it could have problems generating
# a summary from the pieces of context if the spacing is not done correctly

prompt_template = """Given the provided Documents, answer the Query. Make your answer short and concise.
Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}
Question: {{ question }}
Answer:
"""