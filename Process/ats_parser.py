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

def deep_get(dictionary, keys, default=None):
    for key in keys:
        if isinstance(dictionary, dict):
            dictionary = dictionary.get(key, {})
        else:
            return default
    return dictionary if dictionary != {} else default



def extract_resume_details(resume: str):
    print("Innnnnnnnnnnnnnnnnnnnnnnnnnnn")
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
        combined_output = get_response(prompt=resume, task=system_ins)
        print("Before parsing st dataa to JSON",combined_output)
        
        result = json.loads(combined_output)
        print("after st data json",combined_output)

        structured_data = result["structured_data"]
        print(structured_data)

        return structured_data
    except:
        return {"structured_data":"Failed to Get Due to Improper Json Data"}
# resume = "Harish KB 8248052926 # harishkb20205@gmail.com i Harish KB HARISH20205 Education Vellore Institute of Technology (VIT) Vellore, India MTECH (Integrated) in Computer Science and Engineering(CGPA: 8.46) Aug 2022 July 2027 Experience AI Research and Development Intern (Remote) Jun 2024 Oct 2024 eBramha Techworks Private Limited - Developed a speech-to-text summarization system integrating Whisper for transcription and Pegasus for summarization, enhancing processing speed and efficiency while significantly reducing overall processing time and improving system performance. - Conducted in-depth research on advanced NLP models such as PEGASUS, BERTsum and BART, contributing to the development of effective solutions for tasks like summarization and language understanding. - Built a neural network for handwritten digit classification (MNIST) from scratch, implementing core machine learning concepts like gradient descent and one-hot encoding. Projects VerbiSense: Interactive Document Retrieval System - Link - Built the VerbiSense backend with FastAPI, optimizing document uploads, query processing, and API performance for real-time interactions with the React frontend. - Integrated Retrieval-Augmented Generation (RAG) for improved document retrieval and response generation. - Applied PyTorch models for advanced NLP tasks like semantic understanding and context-based querying. Speech-to-Text Summarization - Developed a Python script that improved audio transcription accuracy by 30% and reduced post-processing time by 35%. - Designed and implemented the frontend interface to provide a seamless, user-friendly experience for individuals interacting with the speech-to-text summarization system. Technical Skills Languages: Python, Java, C/C++ Machine Learning: Supervised learning, unsupervised learning, NLP, LLMs Tools: GitHub, Docker, Linux, AWS, Hugging Face Computer Vision: OpenCV, YOLO Backend: FastAPI, Flask, MongoDB, Firebase Areas of Interest - Machine Learning and AI - Full Stack Development - Cloud Computing and DevOps Practices Certifications - Coursera: Supervised Machine Learning: Regression and Classification - Coursera: Advanced Learning Algorithms - Coursera: Generative AI with Large Language Models."

# print(extract_resume_details(resume))
