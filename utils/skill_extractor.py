import re


def clean_skill(skill):
    """Clean a skill entered by the recruiter."""

    skill = skill.strip().lower()

    skill = re.sub(r"\s+", " ", skill)

    return skill


def get_required_skills(skills_text):
    """Convert comma-separated skills into a list."""

    skills = skills_text.split(",")

    skills = [
        clean_skill(skill)
        for skill in skills
        if skill.strip()
    ]

    return skills


def find_matching_skills(resume_text, required_skills):

    resume_text = resume_text.lower()

    matched = []
    not_found = []

    for skill in required_skills:

        if skill in resume_text:

            matched.append(skill)

        else:

            not_found.append(skill)

    return matched, not_found


def calculate_skill_score(matched, required):

    if not required:

        return 0

    score = (len(matched) / len(required)) * 100

    return round(score, 2)