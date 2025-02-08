import re
from .response import get_response
from pydantic import BaseModel, TypeAdapter

class Section:
    name: str
    email: str
    phone: str
    skills: str
    experience: str
    education: str
    certifications: str
    areas_of_interest: str

def extract_structured_data(resume: str):
    system_ins = """Analyze the following resume and extract its contents into a structured format. Ensure that the extracted information is accurate and well-categorized under the following fields:
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

                Provide the output in the exact JSON format mentioned above. If a field is missing or cannot be determined, set its value to None."""
    structured_data = get_response(prompt=resume,task=system_ins)
    # Return structured data
    return structured_data
# structured_output = extract_structured_data()
# print(structured_output)
