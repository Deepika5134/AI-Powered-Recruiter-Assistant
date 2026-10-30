# AI-Powered Recruiter Assistant – Resume Screening & Smart Shortlisting

## Overview

The AI-Powered Recruiter Assistant is a Python-based application built with Streamlit to support resume screening and candidate shortlisting. It uses natural language processing (NLP) and semantic similarity techniques to help compare candidate resumes against job requirements.

## Features

- **Resume Screening:** Process resumes and extract relevant information.
- **Skill Extraction:** Identify skills from candidate resumes.
- **Semantic Matching:** Compare resumes with job requirements using Sentence Transformers.
- **Candidate Scoring:** Rank candidates based on the implemented matching logic.
- **Candidate Comparison:** Support comparisons between shortlisted candidates.
- **Excel Reports:** Generate recruiter reports for further review.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Sentence Transformers
- PyPDF
- python-docx

## Project Structure

```text
AI_Recruiter_Assistant/
├── app.py
├── requirements.txt
├── .gitignore
└── utils/
    ├── candidate_scorer.py
    ├── resume_matcher.py
    ├── resume_parser.py
    └── skill_extractor.py
```

## Installation

1. Clone this repository.
2. Open a terminal in the project directory.
3. Create and activate a virtual environment.
4. Install the dependencies.

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Open the local address displayed in the terminal.

## Responsible Use

This application is intended to assist recruiters, not replace human judgment. Candidate scores and automated matches should be reviewed by a human. Resume data can contain sensitive personal information, so use appropriate access controls and avoid publishing candidate documents or personal data.

## License

No license has been specified yet. Please add a license after deciding how you want others to use this project.