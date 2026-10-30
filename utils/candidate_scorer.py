import re


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience_years(resume_text):
    """
    Extract only explicit professional/work experience.
    Does not count education, projects, internships, certifications,
    graduation years, or unrelated numbers.
    """

    text = resume_text.lower()
    text = re.sub(r"\s+", " ", text)

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+professional\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+professional\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+work\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+work\s+experience",
        r"professional\s+experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"work\s+experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"relevant\s+work\s+experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+relevant\s+experience",
    ]

    found_years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                years = float(match)

                if 0 < years <= 50:
                    found_years.append(years)

            except ValueError:
                pass

    return max(found_years) if found_years else 0.0


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(resume_text, minimum_experience):
    """
    Calculate professional experience score.

    If no experience is required, score is 100%.
    Otherwise only explicit professional experience is counted.
    """

    if minimum_experience == 0:
        return 100.0

    candidate_years = extract_experience_years(resume_text)

    if candidate_years == 0:
        return 0.0

    if candidate_years >= minimum_experience:
        return 100.0

    return round(
        (candidate_years / minimum_experience) * 100,
        2
    )


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Normalize text for reliable matching."""

    text = str(text).lower()

    # Convert punctuation such as ".", "-", "/" into spaces.
    text = re.sub(r"[^a-z0-9]+", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# EDUCATION SCORE
# ============================================================

def calculate_education_score(resume_text, required_education):
    """
    Match the recruiter's education requirement against the resume.

    Examples treated as equivalent:
        B.Tech
        B Tech
        B.Tech.
        Bachelor of Technology
        Bachelor Technology

    Also supports:
        B.E. / Bachelor of Engineering
        M.Tech / Master of Technology
        M.E. / Master of Engineering
        MCA / Master of Computer Applications
        BCA / Bachelor of Computer Applications
        B.Sc / Bachelor of Science
        M.Sc / Master of Science
        B.Com / Bachelor of Commerce
        MBA / Master of Business Administration
    """

    if not str(required_education).strip():
        return 100.0

    resume = normalize_text(resume_text)

    # Compact version makes "B.Tech" and "B Tech" equivalent.
    resume_compact = resume.replace(" ", "")

    education_aliases = {
        "btech": [
            "btech",
            "b tech",
            "b.tech",
            "bachelor of technology",
            "bachelor technology",
        ],
        "be": [
            "be",
            "b e",
            "b.e",
            "bachelor of engineering",
            "bachelor engineering",
        ],
        "mtech": [
            "mtech",
            "m tech",
            "m.tech",
            "master of technology",
            "master technology",
        ],
        "me": [
            "me",
            "m e",
            "m.e",
            "master of engineering",
            "master engineering",
        ],
        "mca": [
            "mca",
            "m ca",
            "m.c.a",
            "master of computer applications",
            "master computer applications",
        ],
        "bca": [
            "bca",
            "b ca",
            "b.c.a",
            "bachelor of computer applications",
            "bachelor computer applications",
        ],
        "bsc": [
            "bsc",
            "b sc",
            "b.sc",
            "bachelor of science",
            "bachelor science",
        ],
        "msc": [
            "msc",
            "m sc",
            "m.sc",
            "master of science",
            "master science",
        ],
        "bcom": [
            "bcom",
            "b com",
            "b.com",
            "bachelor of commerce",
            "bachelor commerce",
        ],
        "mba": [
            "mba",
            "m ba",
            "m.b.a",
            "master of business administration",
            "master business administration",
        ],
    }

    # Split alternatives such as:
    # "B.Tech / B.E. / MCA"
    requirements = re.split(
        r"[/,|;]",
        str(required_education)
    )

    for requirement in requirements:

        requirement = normalize_text(requirement)

        if not requirement:
            continue

        requirement_compact = requirement.replace(" ", "")

        # ----------------------------------------------------
        # CHECK KNOWN DEGREE
        # ----------------------------------------------------

        for degree, aliases in education_aliases.items():

            normalized_aliases = [
                normalize_text(alias)
                for alias in aliases
            ]

            aliases_compact = [
                alias.replace(" ", "")
                for alias in normalized_aliases
            ]

            # Determine whether the recruiter's requirement
            # refers to this degree.
            requirement_matches_degree = (
                requirement_compact in aliases_compact
            )

            if not requirement_matches_degree:
                continue

            # Candidate has this degree if ANY equivalent
            # representation occurs in the resume.
            for alias, alias_compact in zip(
                normalized_aliases,
                aliases_compact
            ):

                if alias in resume:
                    return 100.0

                if alias_compact in resume_compact:
                    return 100.0

        # ----------------------------------------------------
        # CUSTOM EDUCATION REQUIREMENT
        # ----------------------------------------------------

        if (
            requirement in resume
            or requirement_compact in resume_compact
        ):
            return 100.0

    return 0.0


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_overall_score(
    skill_score,
    semantic_score,
    experience_score,
    education_score
):
    """
    Overall score weights:

    Skill Match       = 40%
    Semantic Match    = 30%
    Experience Match  = 20%
    Education Match   = 10%
    """

    overall_score = (
        float(skill_score) * 0.40
        + float(semantic_score) * 0.30
        + float(experience_score) * 0.20
        + float(education_score) * 0.10
    )

    return round(float(overall_score), 2)
