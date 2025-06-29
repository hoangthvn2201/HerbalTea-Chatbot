# from langchain.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field

# Define a BaseModel Retrieve class for LLM tool calling
class Retrieve(BaseModel):
    """
    Searches the knowledge base for answers. The query parameter should contain the contextualized question to search for in the knowledge base.
    """
    query: str = Field(description="should be a search query")