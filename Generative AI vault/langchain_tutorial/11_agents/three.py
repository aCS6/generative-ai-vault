# Custom Tool (Using Decorator)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


class SearchInput(BaseModel):
    query: str = Field(description="Should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(question: str) -> str:
    """Look up things online"""

    return "Langchain"


print(search.name)
print(search.description)
print(search.args)
