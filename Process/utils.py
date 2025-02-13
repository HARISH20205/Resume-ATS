import json
from typing import Dict, List, Optional, Union
from .response import get_response

SYSTEM_INSTRUCTION = """
Provide responses in this exact JSON format:
{
    "score": <number 0-10>,
    "matching_elements": [<list of matching items>],
    "missing_elements": [<list of recommended items>],
    "explanation": "<detailed explanation>"
}
Ensure the score is always a number between 0-10.
"""

class ATSResumeParser:
    def __init__(self):
        self.score_weights = {
            'skills_match': 25,
            'experience_relevance': 30,
            'education_relevance': 20,
            'overall_formatting': 15,
            'keyword_optimization': 10
        }

    def _parse_gemini_response(self, response_text: str) -> Dict:
        try:
            response = json.loads(response_text)
            return {
                'score': float(response['score']),
                'matching': response.get('matching_elements', []),
                'missing': response.get('missing_elements', []),
                'explanation': response.get('explanation', '')
            }
        except (json.JSONDecodeError, KeyError, ValueError):
            return {'score': 5.0, 'matching': [], 'missing': [], 'explanation': ''}

    def _score_skills(self, skills: List[str], job_description: Optional[str]) -> Dict:
        if not skills:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No skills provided'}
            
        base_score = 70  
        
        if len(skills) >= 5:
            base_score += 10
        if len(skills) >= 10:
            base_score += 10
            
        if job_description:
            prompt = f"""
            Analyze these skills: {', '.join(skills)}
            for the job description: {job_description}
            Consider relevance, importance, and skill level required.
            """
            response = self._parse_gemini_response(
                get_response(prompt, SYSTEM_INSTRUCTION)
            )
            return {
                'score': (base_score + (response['score'] * 10)) / 2,
                'matching': response['matching'],
                'missing': response['missing'],
                'explanation': response['explanation']
            }
            
        return {'score': base_score, 'matching': skills, 'missing': [], 'explanation': 'No job description provided'}

    def _score_experience(self, experience: List[Dict], job_description: Optional[str]) -> Dict:
        if not experience:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No experience provided'}
            
        base_score = 60
        
        for exp in experience:
            if all(key in exp for key in ['title', 'company', 'description']):
                base_score += 10
            if any(keyword in exp.get('description', '').lower() for keyword in 
                  ['increased', 'decreased', 'improved', '%', 'reduced']):
                base_score += 5
                
        if job_description:
            prompt = f"""
            Analyze this work experience:
            {json.dumps(experience)}
            for the job description: {job_description}
            Consider relevance, duration, and responsibilities.
            """
            response = self._parse_gemini_response(
                get_response(prompt, SYSTEM_INSTRUCTION)
            )
            return {
                'score': (base_score + (response['score'] * 10)) / 2,
                'matching': response['matching'],
                'missing': response['missing'],
                'explanation': response['explanation']
            }
            
        return {'score': base_score, 'matching': [], 'missing': [], 'explanation': 'No job description provided'}

    def _score_education(self, education: List[Dict]) -> Dict:
        if not education:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No education provided'}
            
        score = 70
        matching = []
        
        for edu in education:
            if 'gpa' in edu and float(edu['gpa']) > 3.0:
                score += 10
                matching.append(f"Strong GPA: {edu['gpa']}")
            if all(key in edu for key in ['institution', 'degree', 'start_date', 'end_date']):
                score += 10
                matching.append(f"{edu['degree']} from {edu['institution']}")
                
        return {
            'score': min(100, score),
            'matching': matching,
            'missing': [],
            'explanation': 'Education assessment completed'
        }

    def _score_formatting(self, structured_data: Dict) -> Dict:
        score = 100
        missing = []
        
        contact_fields = ['name', 'email', 'phone']
        missing_contacts = [field for field in contact_fields if field not in structured_data]
        if missing_contacts:
            score -= 20
            missing.extend(missing_contacts)
            
        essential_sections = ['skills', 'experience', 'education']
        missing_sections = [section for section in essential_sections if section not in structured_data]
        if missing_sections:
            score -= 15 * len(missing_sections)
            missing.extend(missing_sections)
                
        return {
            'score': max(0, score),
            'matching': [field for field in contact_fields if field in structured_data],
            'missing': missing,
            'explanation': 'Format assessment completed'
        }

    def parse_and_score(self, structured_data: Dict, job_description: Optional[str] = None) -> Dict:
        scores = {}
        feedback = {'strengths': [], 'improvements': []}
        detailed_feedback = {}
        
        score_components = {
            'skills_match': self._score_skills(structured_data.get('skills', []), job_description),
            'experience_relevance': self._score_experience(structured_data.get('experience', []), job_description),
            'education_relevance': self._score_education(structured_data.get('education', [])),
            'overall_formatting': self._score_formatting(structured_data),
        }
        
        total_score = 0
        for category, result in score_components.items():
            scores[category] = result['score']
            total_score += result['score'] * (self.score_weights[category] / 100)
            
            detailed_feedback[category] = {
                'matching_elements': result['matching'],
                'missing_elements': result['missing'],
                'explanation': result['explanation']
            }
            
            if result['score'] >= 80:
                feedback['strengths'].append(f"Strong {category.replace('_', ' ')}")
            elif result['score'] < 60:
                feedback['improvements'].append(f"Improve {category.replace('_', ' ')}")
        
        return {
            'total_score': round(total_score, 2),
            'detailed_scores': scores,
            'feedback': feedback,
            'detailed_feedback': detailed_feedback
        }

def generate_ats_score(structured_data: Union[Dict, str], job_des_text: Optional[str] = None) -> Dict:
    try:
        if not structured_data:
            return {"error": "No resume data provided"}
            
        if isinstance(structured_data, str):
            try:
                structured_data = json.loads(structured_data)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format in resume data"}
        
        parser = ATSResumeParser()
        result = parser.parse_and_score(structured_data, job_des_text)
        
        return {
            'ats_score': result['total_score'],
            'detailed_scores': result['detailed_scores'],
            'feedback': result['feedback'],
            'detailed_feedback': result['detailed_feedback']
        }
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}