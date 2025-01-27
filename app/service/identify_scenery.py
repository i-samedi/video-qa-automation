import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.models import TestCaseIndexList
from dotenv import load_dotenv

load_dotenv()

def identify_test_case_indices(transcript):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found in .env file. Please add it and try again.")
        return None

    chat = ChatOpenAI(temperature=0, api_key=api_key, model="gpt-4")

    parser = PydanticOutputParser(pydantic_object=TestCaseIndexList)

    prompt = ChatPromptTemplate.from_template(
        "Analyze the following transcript and identify distinct test cases and their actions. "
        "For each test case:\n"
        "1. Identify when a new action or workflow begins\n"
        "2. Track the sequence of actions until they form a complete test case\n"
        "3. Mark the end when the action sequence completes or a new workflow begins\n"
        "4. Pay special attention to:\n"
        "   - User interactions (clicks, inputs, selections)\n"
        "   - System responses\n"
        "   - Navigation between screens\n"
        "   - Completion of workflows\n\n"
        "Provide the name, precise start time, and end time for each test case. "
        "Use the format 'minutes:seconds' for start and end times.\n"
        "Return the result in the following format:\n{format_instructions}\n\n"
        "Example of what constitutes a complete test case:\n"
        "- A sequence of related actions that achieve a specific goal\n"
        "- Actions that begin with user input and end with system confirmation\n"
        "- Complete workflows like login, form submission, or data validation\n\n"
        "Transcript: {transcript}"
    )

    formatted_prompt = prompt.format_prompt(
        format_instructions=parser.get_format_instructions(),
        transcript=transcript
    )

    response = chat(formatted_prompt.to_messages())
    parsed_response = parser.parse(response.content)

    return parsed_response.model_dump()