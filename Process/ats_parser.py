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
    system_ins = """Analyze the provided resume and perform the following tasks:
    1. Extract its contents into a structured format under the fields:
       {
        "name": None,
        "email": None,
        "phone": None,
        "skills": None,
        "experience": None,
        "education": None,
        "certifications": None,
        "areas of interest": None
       }
       Provide this output in JSON format under the key "structured_data". If a field is missing or cannot be determined, set its value to None.

    2. Convert the resume into a well-structured and professional markdown format, ensuring proper use of headings, subheadings, bullet points, and consistent formatting for sections like education, experience, projects, skills, and certifications. Include the markdown content in a JSON field named "markdown", properly escaped to maintain JSON validity.

    Combine the outputs into the following JSON format:
    {
        "markdown": {markdown_content},
        "structured_data": {structured_data}
    }
    """
    combined_output = get_response(prompt=resume, task=system_ins)
    result = json.loads(combined_output)
    return result.get("markdown"), result.get("structured_data")

# structured_output = extract_structured_data()
# print(structured_output)
