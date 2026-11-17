
# ==========================================
# PERSON 3 - SCORING AGENT
# ==========================================

def score_resume(jd_dict, resume_dict):
    """
    Compare Job Description and Resume dictionaries.
    Return a score and explanation.
    """

    # Step 1: Extract skills from both dictionaries

    jd_skills = jd_dict.get("skills", [])
    resume_skills = resume_dict.get("skills", [])

    # Convert all skills to lowercase for easy comparison
    jd_skills = [skill.lower().strip() for skill in jd_skills]
    resume_skills = [skill.lower().strip() for skill in resume_skills]

    # Step 2: Convert lists into sets
    jd_skill_set = set(jd_skills)
    resume_skill_set = set(resume_skills)

    # Step 3: Find matching skills
    matched_skills = jd_skill_set.intersection(resume_skill_set)

    # Step 4: Find missing skills
    missing_skills = jd_skill_set - resume_skill_set

    # Step 5: Find additional skills
    extra_skills = resume_skill_set - jd_skill_set

    # Step 6: Calculate score
    if len(jd_skill_set) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(jd_skill_set)) * 100

    score = round(score, 2)

    # Step 7: Generate explanation
    if score >= 80:
        explanation = "Excellent match. The candidate meets most of the required skills."
        decision = "Selected"

    elif score >= 60:
        explanation = "Good match. The candidate meets many required skills but has some gaps."
        decision = "Shortlisted"

    elif score >= 40:
        explanation = "Average match. The candidate has some relevant skills but needs improvement."
        decision = "Needs Review"

    else:
        explanation = "Low match. The candidate lacks many of the required skills."
        decision = "Rejected"

    # Step 8: Return scoring dictionary
    score_dict = {
        "score": score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "extra_skills": sorted(extra_skills),
        "explanation": explanation,
        "decision": decision
    }

    return score_dict


# ==========================================
# TESTING THE SCORING AGENT
# ==========================================

if __name__ == "__main__":

    # Sample Job Description dictionary
    jd_dict = {
        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Communication",
            "Data Analysis"
        ]
    }

    # Sample Resume dictionary
    resume_dict = {
        "skills": [
            "Python",
            "SQL",
            "Data Analysis",
            "Excel",
            "Communication"
        ]
    }

    # Call scoring function
    result = score_resume(jd_dict, resume_dict)

    # Display result
    print("===== SCORING AGENT RESULT =====")
    print("Score:", result["score"], "%")
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])
    print("Extra Skills:", result["extra_skills"])
    print("Explanation:", result["explanation"])
    print("Decision:", result["decision"])
