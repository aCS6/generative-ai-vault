# Custom Tool (Using StructuredTool)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


class CalculatorInput(BaseModel):
    a: int = Field(description="First Number")
    b: int = Field(description="Second Number")


def multiply(a: int, b: int) -> int:
    """Multiply two integers"""
    return a * b


calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="Multiply Numbers",
    args_schema=CalculatorInput,
    return_direct=True,
)

print(calculator.name)
print(calculator.description)
print(calculator.args)
