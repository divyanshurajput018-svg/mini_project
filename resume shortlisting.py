
import re


# ==========================================
# PERSON 2 - RESUME PARSER AGENT
# ==========================================

def parse_resume(resume_text):
    """
    Takes raw resume text and returns
    a structured dictionary.
    """

    # Step 1: Clean resume text
    resume_text = resume_text.strip()

    # Step 2: Extract candidate name
    lines = resume_text.split("\n")

    candidate_name = ""

    if lines:
        candidate_name = lines[0].strip()

    # Step 3: Extract email
    email_match = re.search(
        r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}',
        resume_text
    )

    email = email_match.group(0) if email_match else ""

    # Step 4: Extract phone number
    phone_match = re.search(
        r'(\+?\d[\d\s()-]{8,}\d)',
        resume_text
    )

    phone = phone_match.group(0).strip() if phone_match else ""

    # Step 5: Extract skills
    common_skills = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Machine Learning",
        "Deep Learning",
        "Data Analysis",
        "Data Science",
        "Excel",
        "Power BI",
        "Tableau",
        "Communication",
        "Leadership",
        "Problem Solving",
        "Teamwork",
        "AWS",
        "Cloud Computing",
        "Django",
        "Flask",
        "Git",
        "Linux"
    ]

    resume_lower = resume_text.lower()

    skills = []

    for skill in common_skills:
        if re.search(
            r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)',
            resume_lower
        ):
            skills.append(skill)

    # Step 6: Extract education
    education_keywords = [
        "B.Tech",
        "M.Tech",
        "B.E",
        "M.E",
        "BCA",
        "MCA",
        "B.Sc",
        "M.Sc",
        "MBA",
        "Bachelor",
        "Master",
        "PhD"
    ]

    education = []

    for item in education_keywords:
        if item.lower() in resume_lower:
            education.append(item)

    # Step 7: Extract experience
    experience = []

    experience_patterns = [
        r'\d+\+?\s+years?\s+of\s+experience',
        r'\d+\+?\s+years?\s+experience'
    ]

    for pattern in experience_patterns:
        matches = re.findall(
            pattern,
            resume_text,
            re.IGNORECASE
        )
        experience.extend(matches)

    # Step 8: Create final dictionary
    resume_dict = {
        "candidate_name": candidate_name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience
    }

    return resume_dict


# ==========================================
# TESTING THE RESUME PARSER
# ==========================================

if __name__ == "__main__":

    sample_resume = """
    Rahul Sharma

    Email: rahul@gmail.com
    Phone: 9876543210

    Education:
    B.Tech Computer Science

    Skills:
    Python, Java, SQL, Machine Learning,
    Data Analysis, Communication, Excel

    Experience:
    2 years of experience in Python development.
    """

    result = parse_resume(sample_resume)

    print("======= RESUME PARSER RESULT =======")

    for key, value in result.items():
        print(key, ":", value)
