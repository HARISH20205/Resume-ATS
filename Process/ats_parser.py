import re
from .response import get_response  # Custom module to handle AI responses
from pydantic import BaseModel, TypeAdapter  # Validation and data modeling
import json

# Define a class to structure the extracted resume data
class Section:
    name: str
    email: str
    phone: str
    skills: str
    experience: str
    education: str
    certifications: str
    areas_of_interest: str

# Function to extract resume details and generate markdown
def extract_resume_details(resume: str):
    """
    This function processes a given resume text to:
    1. Extract structured data into predefined fields.
    2. Convert the resume into valid markdown, formatted with manual whitespace for clarity.

    Parameters:
        resume (str): The raw text of the resume.

    Returns:
        tuple: A tuple containing the markdown content and structured data in JSON format.
    """

    # System instruction for AI response
    system_ins = """Analyze the provided resume and perform the following tasks:

1. Extract the resume's content into a structured format under the following fields:
{
    "name": None,
    "email": None,
    "phone": None,
    "skills": None,
    "experience": None,
    "education": None,
    "certifications": None,
    "areas_of_interest": None
}
- Provide this output in JSON format under the key "structured_data".
- If a field is missing or cannot be determined, set its value to None.

2. Convert the provided resume into **valid markdown** formatted for professional readability. Ensure the markdown uses manual whitespace for separation between sections and avoids any escaped characters like `\\n`. Use proper headings, subheadings, and bullet points to organize the information.

Return the output in the following JSON format:
{
    "markdown": "Valid markdown content with manual whitespace for separation.",
    "structured_data": {structured_data}
}
"""

    # Combine the resume text with the system instructions for processing
    combined_output = get_response(prompt=resume, task=system_ins)

    # Parse the combined output as JSON
    result = json.loads(combined_output)

    # Extract the markdown content and structured data
    markdown = result.get("markdown", "")
    structured_data = result.get("structured_data")

    # Clean up trailing whitespace in the markdown
    markdown = '\n'.join(line.rstrip() for line in markdown.splitlines())

    return markdown, structured_data
