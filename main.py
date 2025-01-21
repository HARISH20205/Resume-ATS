from transformers import AutoTokenizer, AutoModel
import torch
from scipy.spatial.distance import cosine
import fitz 



def get_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num) 
        text += page.get_text() 
    return text



def get_embeddings(texts, tokenizer, model):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model(**inputs)
    embeddings = model_output.last_hidden_state.mean(dim=1)
    return embeddings

def calculate_similarity(job_description, resume):
    jd_embedding = get_embeddings([job_description], tokenizer, model)
    resume_embedding = get_embeddings([resume], tokenizer, model)

    jd_embedding = jd_embedding / jd_embedding.norm(dim=1, keepdim=True)
    resume_embedding = resume_embedding / resume_embedding.norm(dim=1, keepdim=True)
    print(jd_embedding)
    similarity = torch.mm(jd_embedding, resume_embedding.T).item()
    return similarity


model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

pdf_path = "Data/Resume.pdf"
extracted_text = get_text(pdf_path)
print(extracted_text)


job_description = """
Job Title: AI/ML Engineer - NLP and Backend Development

Job Description:
We are seeking an AI/ML Engineer skilled in NLP, machine learning, and backend development to design and implement advanced AI solutions.

Responsibilities:

Develop speech-to-text summarization systems using Whisper, PEGASUS, and BERT.
Research and apply NLP models (e.g., PEGASUS, BERTsum, BART) for summarization and language tasks.
Build neural networks for tasks like MNIST handwritten digit classification.
Design scalable backends using FastAPI and integrate RAG and PyTorch models for document retrieval.
Optimize and deploy AI models on AWS and Hugging Face platforms.
Skills and Tools:

Languages: Python, Java, C/C++.
ML/NLP: Supervised/unsupervised learning, LLMs.
Backend: FastAPI, Flask, MongoDB, Firebase.
Tools: GitHub, Docker, Linux, AWS, Hugging Face.
Computer Vision: OpenCV, YOLO.
Preferred:

Certifications in ML and Generative AI.
Experience with cloud and DevOps practices.
Join us to build innovative AI systems and work on cutting-edge projects!
"""

similarity_score = calculate_similarity(job_description, extracted_text)
print(f"Cosine Similarity: {similarity_score:.4f}")
