import re
from .response import get_response  
from pydantic import BaseModel, TypeAdapter
import json

class Section:
    name: str
    email: str
    phone: str
    skills: str
    experience: str
    education: str
    certifications: str
    areas_of_interest: str

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
    "areas_of_interest": None,
    "projects": None,
    "languages": None,
    "awards_and_achievements": None,
    "volunteer_experience": None,
    "hobbies_and_interests": None,
    "publications": None,
    "conferences_and_presentations": None,
    "patents": None,
    "professional_affiliations": None,
    "portfolio_links": None,
    "summary_or_objective": None
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

    combined_output = get_response(prompt=resume, task=system_ins)

    result = json.loads(combined_output)

    markdown = result.get("markdown", "")
    structured_data = result.get("structured_data")

    markdown = '\n'.join(line.rstrip() for line in markdown.splitlines())

    return markdown, structured_data
