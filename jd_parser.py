import re


# ==========================================
# JD PARSER AGENT
# Person 1 - Resume Shortlisting Project
# ==========================================


def parse_jd(jd_text):

    # Step 1: Convert text into lowercase
    text = jd_text.lower()

    # Step 2: Extract Job Title
    title_match = re.search(
        r"(?:job title|position|role)\s*:\s*(.+)",
        text
    )

    if title_match:
        title = title_match.group(1).strip()
    else:
        lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
        title = lines[0] if lines else "Not specified"

    # Step 3: Define available skills
    all_skills = [
        "python", "java", "c++", "c",
        "sql", "mysql", "django", "flask",
        "html", "css", "javascript",
        "react", "machine learning",
        "deep learning", "aws", "azure",
        "git", "docker", "excel",
        "power bi", "data analysis",
        "pandas", "numpy", "communication",
        "problem solving"
    ]

    # Step 4: Extract Nice-to-Have section
    nice_match = re.search(
        r"(?:nice to have|good to have|preferred skills)"
        r"\s*:\s*(.*?)(?=\n\s*(?:required skills|requirements|"
        r"minimum experience|experience|education)\s*:|\Z)",
        text,
        re.S
    )

    nice_text = nice_match.group(1) if nice_match else ""

    # Step 5: Extract Required Skills section
    required_match = re.search(
        r"(?:required skills|mandatory skills)"
        r"\s*:\s*(.*?)(?=\n\s*(?:nice to have|good to have|"
        r"preferred skills|minimum experience|experience|education)\s*:|\Z)",
        text,
        re.S
    )

    required_text = required_match.group(1) if required_match else ""

    # Step 6: Find skills
    required_skills = []
    nice_to_have_skills = []

    def find_skills(section):

        found = []

        for skill in all_skills:

            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

            if re.search(pattern, section):
                found.append(skill)

        return found

    if required_match:
        required_skills = find_skills(required_text)

    if nice_match:
        nice_to_have_skills = find_skills(nice_text)

    # Fallback if no required skills section exists
    if not required_match:

        nice_skills = find_skills(nice_text)

        for skill in find_skills(text):

            if skill not in nice_skills:
                required_skills.append(skill)

    # Step 7: Extract Minimum Experience
    min_experience_years = 0

    experience_match = re.search(
        r"(?:minimum experience|min experience|at least|minimum|min)"
        r"\s*:?\s*(\d+)\s*\+?\s*(?:years|yrs)",
        text
    )

    if not experience_match:
        experience_match = re.search(
            r"(\d+)\s*\+?\s*(?:years|yrs)",
            text
        )

    if experience_match:
        min_experience_years = int(experience_match.group(1))

    # Step 8: Extract Education
    education_requirement = ""

    education_options = [
        ("bachelor's degree", ["bachelor's degree", "bachelors degree"]),
        ("master's degree", ["master's degree", "masters degree"]),
        ("b.tech", ["b.tech"]),
        ("m.tech", ["m.tech"]),
        ("b.e.", ["b.e."]),
        ("mba", ["mba"]),
        ("phd", ["phd", "ph.d."]),
        ("diploma", ["diploma"])
    ]

    for education, keywords in education_options:

        for keyword in keywords:

            if keyword in text:
                education_requirement = education
                break

        if education_requirement:
            break

    # Step 9: Create Final Dictionary
    result = {

        "title": title,

        "required_skills": required_skills,

        "nice_to_have_skills": nice_to_have_skills,

        "min_experience_years": min_experience_years,

        "education_requirement": education_requirement

    }

    return result


# ==========================================
# TESTING THE JD PARSER
# ==========================================

if __name__ == "__main__":

    jd_text = """
    Job Title: Python Developer

    Required Skills:
    Python, SQL, Django, Git

    Nice to Have:
    Machine Learning, AWS

    Minimum Experience: 2 years

    Education: Bachelor's degree
    """

    output = parse_jd(jd_text)

    print("\n========== JD PARSER OUTPUT ==========\n")

    for key, value in output.items():

        print(f"{key}: {value}")

    print("\n======================================")