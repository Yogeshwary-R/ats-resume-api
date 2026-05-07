import re

TECH_SKILLS = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "ruby", "php", "swift", "kotlin", "golang", "rust", "scala", "r",
    # Frameworks
    "fastapi", "django", "flask", "react", "angular", "vue", "nodejs",
    "express", "spring", "laravel", "rails", "nextjs", "nuxtjs",
    # Databases
    "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "sqlite",
    "cassandra", "dynamodb", "oracle", "firebase",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git",
    "github", "gitlab", "cicd", "terraform", "ansible", "linux",
    "devops", "cloud",
    # AI & Data
    "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "tensorflow", "pytorch", "scikit", "keras", "matplotlib",
    "data analysis", "data science", "big data", "hadoop", "spark",
    # Concepts
    "oop", "object oriented", "data structures", "algorithms",
    "microservices", "rest", "restful", "api", "graphql",
    "version control", "agile", "scrum", "tdd", "ci/cd",
    "design patterns", "solid principles", "system design",
    # Web & Others
    "html", "css", "jwt", "oauth", "websocket", "celery",
    "rabbitmq", "kafka", "elasticsearch",
    # Soft skills
    "communication", "teamwork", "leadership", "problem solving",
    "analytical", "management", "collaboration"
}

def extract_skills(text: str) -> set:
    text = text.lower()
    found = set()
    for skill in TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

def calculate_ats_score(resume_text: str, job_description: str) -> dict:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_skills)) * 100)

    return {
        "ats_score": score,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "total_jd_keywords": len(jd_skills),
        "total_matched": len(matched),
        "total_missing": len(missing)
    }