CHARACTER = """```python
from langchain.text_splitter import CharacterTextSplitter

{length_function}

splitter = CharacterTextSplitter(
    separator = "\\n\\n",
    chunk_size={chunk_size},
    chunk_overlap={chunk_overlap},
    length_function=length_function,
)
text = "foo bar"
splits = splitter.split_text(text)
```"""

RECURSIVE_CHARACTER = """```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

{length_function}

splitter = RecursiveCharacterTextSplitter(
    separators=["\\n\\n", "\\n", " ", ""],
    chunk_size={chunk_size},
    chunk_overlap={chunk_overlap},
    length_function=length_function,
)
text = "foo bar"
splits = splitter.split_text(text)
```"""

LANGUAGE = """```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

{length_function}

splitter = RecursiveCharacterTextSplitter.from_language(
    {language},
    chunk_size={chunk_size},
    chunk_overlap={chunk_overlap},
    length_function=length_function,
)
text = "foo bar"
splits = splitter.split_text(text)
```"""

CHARACTER_LENGTH = "length_function = len"

TOKEN_LENGTH = """import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def length_function(text: str) -> int:
    return len(enc.encode(text))
"""
