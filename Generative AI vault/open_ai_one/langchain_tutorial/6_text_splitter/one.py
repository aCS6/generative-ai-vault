"""
Text splitter doesn't guarantee that it would spilt text
after the specified chunk_size. It will look for the separator,
and separates.
"""

from langchain_text_splitters import CharacterTextSplitter

# This is a long document we can split up.
with open("6_text_splitter/sample.txt") as f:
    iran = f.read()


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.create_documents([iran])

for chunk in texts:
    print(chunk.page_content)
