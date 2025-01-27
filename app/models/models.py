from pydantic import BaseModel, Field
from typing import List, Dict

class Step(BaseModel):
    start_time: str = Field(description="Start time of the step in format 'minutes:seconds'")
    end_time: str = Field(description="End time of the step in format 'minutes:seconds'")
    screenshot_timestamp: str = Field(description="Exact time for the screenshot in format 'minutes:seconds'")
    title: str = Field(description="Title of the step")
    description: str = Field(description="Detailed description of the step, including user intent, actions, input data,and expected results")
    input_data: dict = Field(description="Data that must be entered", default_factory=dict)
    output_data: dict = Field(description="Exact data that should be returned", default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "input_data": {
                    "data label": "Username",
                    "data value": "john_doe"
                },
                "output_data": {
                    "data label": "Login Status",
                    "data value": "Success"
                }
            }
        }

class TestCase(BaseModel):
    name: str = Field(description="Nombre del caso de prueba")
    steps: List[Step] = Field(description="Lista de pasos en el caso de prueba")
    text: str = Field(description="Texto completo correspondiente al caso de prueba")

    class Config:
        extra = "forbid"  # Evita campos adicionales no definidos

class TestCaseIndex(BaseModel):
    name: str = Field(description="Name of the use case")
    start_time: str = Field(description="Start time of the use case in format 'minutes:seconds'")
    end_time: str = Field(description="End time of the use case in format 'minutes:seconds'")

class TestCaseList(BaseModel):
    test_cases: List[TestCase]

class TestCaseIndexList(BaseModel):
    test_cases: List[TestCaseIndex]
