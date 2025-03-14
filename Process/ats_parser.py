import re
import logging
from .response import get_response  
from pydantic import BaseModel, TypeAdapter
import json
import traceback

# Set up logging
logger = logging.getLogger(__name__)

class Section:
    name: str
    email: str
    phone: str
    skills: str
    experience: str
    education: str
    certifications: str
    areas_of_interest: str

def deep_get(dictionary, keys, default=None):
    logger.debug(f"Accessing deep keys {keys} in dictionary")
    try:
        for key in keys:
            if isinstance(dictionary, dict):
                dictionary = dictionary.get(key, {})
            else:
                logger.warning(f"Could not access key {key}, returning default value")
                return default
        return dictionary if dictionary != {} else default
    except Exception as e:
        logger.error(f"Error in deep_get function: {e}")
        return default

def extract_resume_details(resume: str):
    logger.info("Starting resume details extraction")
    """
    This function processes a given resume text to:
    1. Extract structured data into predefined fields.
    

    Parameters:
        resume (str): The raw text of the resume.

    Returns:
        JSON: A JSON containing the structured data in JSON format.
    """

    system_ins = """Analyze the provided resume and perform the following tasks:

1. Extract the resume's content into a structured format under the following fields:

{
    "structured_data":{
        "name": None,
        "email": None,
        "github": None,
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
}

- Provide this output in JSON format under the key "structured_data".
- If a field is missing or cannot be determined, set its value to None.
"""
    try:
        logger.info("Sending resume to get_response function")
        combined_output = get_response(prompt=resume, task=system_ins)
        logger.debug("Raw response received from get_response")
        
        logger.info("Attempting to parse response to JSON")
        result = json.loads(combined_output)
        logger.debug("Successfully parsed response to JSON")

        logger.info("Extracting structured data from result")
        structured_data = result["structured_data"]
        logger.info("Resume structured data extraction completed successfully")

        return structured_data
    except json.JSONDecodeError as e:
        error_msg = f"JSON parsing error: {e}"
        logger.error(error_msg)
        logger.debug(f"Failed JSON content: {combined_output}")
        return {"structured_data_error": error_msg}
    except KeyError as e:
        error_msg = f"Missing key in response: {e}"
        logger.error(error_msg)
        return {"structured_data_error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error in extract_resume_details: {e}"
        logger.error(error_msg)
        logger.debug(traceback.format_exc())
        return {"structured_data_error": error_msg}
