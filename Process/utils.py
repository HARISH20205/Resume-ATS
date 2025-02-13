

def generate_ats_score(resume_text,job_des_text):
    if not resume_text or not job_des_text:
        return {"error": "Invalid data"}
    print(resume_text)
    score = 100
    return {'ats_score':score}

