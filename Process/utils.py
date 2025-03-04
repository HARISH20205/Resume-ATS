import json
import concurrent.futures
from functools import lru_cache
from typing import Dict, List, Optional, Union
from .response import get_response

SYSTEM_INSTRUCTION = """
Provide responses in this exact JSON format:
{
    "score": <number 0-10>,
    "matching_elements": [<list of matching items>],
    "missing_elements": [<list of recommended items>],
    "explanation": "<explanation in 10-15>"
}
Ensure the score is always a number between 0-10.
"""

class ATSResumeParser:
    def __init__(self):
        self.score_weights = {
            'skills_match': 30,
            'experience_relevance': 25,
            'education_relevance': 10,
            'overall_formatting': 15,
            'keyword_optimization': 10,
            'extra_sections': 10
        }
        self.total_weight = sum(self.score_weights.values())

    @staticmethod
    @lru_cache(maxsize=128)  
    def _parse_gemini_response(response_text: str) -> Dict:
        """Parse the response from Gemini API with caching for better performance"""
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
        """Score skills with optimized processing"""
        if not skills:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No skills provided'}
            
        base_score = 70  
        
        skills_length = len(skills)
        if skills_length >= 5:
            base_score += 10
        if skills_length >= 10:
            base_score += 10
            
        if not job_description:
            return {'score': base_score, 'matching': skills, 'missing': [], 'explanation': 'No job description provided'}

        prompt = f"Skills: {','.join(skills[:20])}. Job description: {job_description[:500]}. Rate match."
        
        response = self._parse_gemini_response(
            get_response(prompt, SYSTEM_INSTRUCTION)
        )
        
        return {
            'score': (base_score + (response['score'] * 10)) >> 1,
            'matching': response['matching'],
            'missing': response['missing'],
            'explanation': response['explanation']
        }

    def _score_experience(self, experience: List[Dict], job_description: Optional[str]) -> Dict:
        """Score experience with optimized processing"""
        if not experience:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No experience provided'}
            
        base_score = 60
        
        required_keys = {'title', 'company', 'description'}
        improvement_keywords = {'increased', 'decreased', 'improved', '%', 'reduced'}
        
        for exp in experience:
            if required_keys.issubset(exp.keys()):
                base_score += 10
                
            description = exp.get('description', '')
            if description and any(keyword in description for keyword in improvement_keywords):
                base_score += 5
                
        if not job_description:
            return {'score': base_score, 'matching': [], 'missing': [], 'explanation': 'No job description provided'}
        
        simplified_exp = [{'title': e.get('title', ''), 'description': e.get('description', '')[:100]} 
                          for e in experience[:3]]
        
        prompt = f"Experience: {json.dumps(simplified_exp)}. Job description: {job_description[:500]}. Rate match."
        
        response = self._parse_gemini_response(
            get_response(prompt, SYSTEM_INSTRUCTION)
        )
        
        return {
            'score': (base_score + (response['score'] * 10)) >> 1,
            'matching': response['matching'],
            'missing': response['missing'],
            'explanation': response['explanation']
        }

    def _score_education(self, education: List[Dict]) -> Dict:
        """Score education with optimized processing"""
        if not education:
            return {'score': 0, 'matching': [], 'missing': [], 'explanation': 'No education provided'}
            
        score = 70
        matching = []
        
        required_keys = {'institution', 'degree', 'start_date', 'end_date'}
        
        for edu in education:
            gpa = edu.get('gpa')
            if gpa and float(gpa) > 3.0:
                score += 10
                matching.append(f"Strong GPA: {gpa}")
                
            if required_keys.issubset(edu.keys()):
                score += 10
                matching.append(f"{edu.get('degree', '')} from {edu.get('institution', '')}")
                
        return {
            'score': min(100, score),
            'matching': matching,
            'missing': [],
            'explanation': 'Education assessment completed'
        }

    def _score_formatting(self, structured_data: Dict) -> Dict:
        """Score formatting with optimized processing"""
        score = 100
        
        contact_fields = ('name', 'email', 'phone')
        essential_sections = ('skills', 'experience', 'education')
        
        structured_keys = set(structured_data.keys())
        
        missing_contacts = [field for field in contact_fields if field not in structured_keys]
        if missing_contacts:
            score -= 20
            
        missing_sections = [section for section in essential_sections if section not in structured_keys]
        missing_penalty = 15 * len(missing_sections)
        if missing_sections:
            score -= missing_penalty
                
        return {
            'score': max(0, score),
            'matching': [field for field in contact_fields if field in structured_keys],
            'missing': missing_contacts + missing_sections,
            'explanation': 'Format assessment completed'
        }

    def _score_extra(self, structured_data: Dict) -> Dict:
        """Score extra sections with optimized processing"""
        extra_sections = {
            "awards_and_achievements": 15,
            "volunteer_experience": 10,
            "hobbies_and_interests": 5,
            "publications": 15,
            "conferences_and_presentations": 10,
            "patents": 15,
            "professional_affiliations": 10,
            "portfolio_links": 10,
            "summary_or_objective": 10
        }
        
        total_possible = sum(extra_sections.values())
        
        structured_keys = set(structured_data.keys())
        
        score = 0
        matching = []
        missing = []
        
        for section, weight in extra_sections.items():
            if section in structured_keys and structured_data.get(section):
                score += weight
                matching.append(section.replace('_', ' ').title())
            else:
                missing.append(section.replace('_', ' ').title())
        
        normalized_score = (score * 100) // total_possible if total_possible > 0 else 0
        
        return {
            'score': normalized_score,
            'matching': matching,
            'missing': missing,
            'explanation': 'Additional sections assessment completed'
        }

    def parse_and_score(self, structured_data: Dict, job_description: Optional[str] = None) -> Dict:
        """Parse and score resume with parallel processing"""
        scores = {}
        feedback = {'strengths': [], 'improvements': []}
        detailed_feedback = {}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Define tasks to run in parallel
            tasks = {
                'skills_match': executor.submit(self._score_skills, structured_data.get('skills', []), job_description),
                'experience_relevance': executor.submit(self._score_experience, structured_data.get('experience', []), job_description),
                'education_relevance': executor.submit(self._score_education, structured_data.get('education', [])),
                'overall_formatting': executor.submit(self._score_formatting, structured_data),
                'extra_sections': executor.submit(self._score_extra, structured_data)
            }
            
            total_score = 0
            for category, future in tasks.items():
                result = future.result()
                
                scores[category] = result['score']
                
                weight = self.score_weights[category] / 100
                total_score += result['score'] * weight
                
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
    """Generate ATS score with optimized processing"""
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