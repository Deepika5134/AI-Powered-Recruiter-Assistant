import streamlit as st
import pandas as pd
from io import BytesIO

# Safe defaults for Streamlit reruns
shortlist_df = pd.DataFrame()
ranking_df = pd.DataFrame()

from utils.resume_parser import extract_text

from utils.skill_extractor import (
    get_required_skills,
    find_matching_skills,
    calculate_skill_score
)

from utils.resume_matcher import (
    calculate_semantic_similarity
)

from utils.candidate_scorer import (
    calculate_experience_score,
    calculate_education_score,
    calculate_overall_score
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Recruiter Assistant",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI-Powered Recruiter Assistant")

st.write(
    "Intelligent Resume Screening, Candidate Ranking "
    "& Resume Similarity Detection"
)

st.divider()


# ============================================================
# JOB DETAILS
# ============================================================

st.header("💼 Job Details")


job_title = st.text_input(
    "Job Title",
    placeholder="Example: Python Developer"
)


job_description = st.text_area(
    "Job Description",
    placeholder="""Example:

We are looking for a Python Developer
with experience in Machine Learning,
SQL and NLP.

The candidate should be able to build
and maintain Python applications.""",
    height=200
)


required_skills = st.text_input(
    "Required Skills",
    placeholder=(
        "Example: Python, SQL, Machine Learning, "
        "NLP, Pandas"
    )
)


# ============================================================
# EXPERIENCE & EDUCATION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    experience = st.number_input(
        "Minimum Experience (Years)",
        min_value=0,
        max_value=30,
        value=0,
        step=1
    )


with col2:

    education = st.text_input(
        "Required Education",
        placeholder="Example: B.Tech / B.E. / MCA"
    )


st.divider()


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header("📄 Upload Candidate Resumes")


uploaded_files = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


st.divider()


# ============================================================
# START SCREENING
# ============================================================

if st.button(
    "🔍 Start Resume Screening",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not job_title.strip():

        st.warning(
            "⚠️ Please enter the Job Title."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please enter the Job Description."
        )

    elif not required_skills.strip():

        st.warning(
            "⚠️ Please enter the Required Skills."
        )

    elif not uploaded_files:

        st.warning(
            "⚠️ Please upload at least one resume."
        )

    else:

        # ----------------------------------------------------
        # REQUIRED SKILLS
        # ----------------------------------------------------

        required_skill_list = get_required_skills(
            required_skills
        )


        st.success(
            "Job details and resumes are ready "
            "for AI analysis! ✅"
        )


        # ====================================================
        # JOB INFORMATION
        # ====================================================

        st.header("📋 Job Information")


        info_col1, info_col2 = st.columns(2)


        with info_col1:

            st.write(
                f"**Job Title:** {job_title}"
            )

            st.write(
                f"**Minimum Experience:** "
                f"{experience} years"
            )


        with info_col2:

            st.write(
                f"**Education:** "
                f"{education if education else 'Not specified'}"
            )

            st.write(
                f"**Required Skills:** "
                f"{required_skills}"
            )


        st.divider()


        # ====================================================
        # RESULTS STORAGE
        # ====================================================

        candidate_results = []


        # ====================================================
        # CANDIDATE ANALYSIS
        # ====================================================

        st.header("🎯 Candidate Analysis")


        for file in uploaded_files:

            st.subheader(
                f"📄 {file.name}"
            )


            # ------------------------------------------------
            # EXTRACT TEXT
            # ------------------------------------------------

            try:

                resume_text = extract_text(file)

            except Exception as error:

                st.error(
                    f"Could not read {file.name}: {error}"
                )

                continue


            # ------------------------------------------------
            # CHECK TEXT
            # ------------------------------------------------

            if not resume_text.strip():

                st.warning(
                    f"⚠️ Could not extract text "
                    f"from {file.name}."
                )

                continue


            st.success(
                "Resume text extracted successfully! ✅"
            )


            # ------------------------------------------------
            # SKILL MATCHING
            # ------------------------------------------------

            matched, not_found = find_matching_skills(
                resume_text,
                required_skill_list
            )


            # ------------------------------------------------
            # SKILL SCORE
            # ------------------------------------------------

            skill_score = calculate_skill_score(
                matched,
                required_skill_list
            )


            # ------------------------------------------------
            # SEMANTIC MATCH
            # ------------------------------------------------

            with st.spinner(
                "🤖 AI is understanding the resume..."
            ):

                semantic_score = (
                    calculate_semantic_similarity(
                        resume_text,
                        job_description
                    )
                )


            # ------------------------------------------------
            # EXPERIENCE
            # ------------------------------------------------

            experience_score = calculate_experience_score(
                resume_text,
                experience
            )


            # ------------------------------------------------
            # EDUCATION
            # ------------------------------------------------

            education_score = calculate_education_score(
                resume_text,
                education
            )


            # ------------------------------------------------
            # OVERALL SCORE
            # ------------------------------------------------

            overall_score = calculate_overall_score(
                skill_score,
                semantic_score,
                experience_score,
                education_score
            )


            # ------------------------------------------------
            # STORE RESULT
            # ------------------------------------------------

            candidate_results.append({

                "Candidate": file.name,

                "Skill Match": float(skill_score),

                "Semantic Match": float(semantic_score),

                "Experience": float(experience_score),

                "Education": float(education_score),

                "Overall Score": float(overall_score),

                "Matched Skills": matched,

                "Missing Skills": not_found

            })


            # =================================================
            # INDIVIDUAL SCORE
            # =================================================

            st.write("## 🎯 Candidate Score")


            score_col1, score_col2, score_col3, score_col4 = (
                st.columns(4)
            )


            with score_col1:

                st.metric(
                    "🎯 Skill Match",
                    f"{float(skill_score):.2f}%"
                )


            with score_col2:

                st.metric(
                    "🧠 Semantic Match",
                    f"{float(semantic_score):.2f}%"
                )


            with score_col3:

                st.metric(
                    "💼 Experience",
                    f"{float(experience_score):.2f}%"
                )


            with score_col4:

                st.metric(
                    "🎓 Education",
                    f"{float(education_score):.2f}%"
                )


            # ------------------------------------------------
            # OVERALL
            # ------------------------------------------------

            st.subheader(
                f"🏆 Overall Match: "
                f"{float(overall_score):.2f}%"
            )


            st.progress(
                float(
                    min(
                        float(overall_score) / 100,
                        1.0
                    )
                )
            )


            # =================================================
            # SCORE EXPLANATION
            # =================================================

            st.write(
                "### 📊 How the Score Was Calculated"
            )


            st.write(
                f"""
                **Skill Match:** {float(skill_score):.2f}% × 40%

                **Semantic Match:** {float(semantic_score):.2f}% × 30%

                **Experience Match:** {float(experience_score):.2f}% × 20%

                **Education Match:** {float(education_score):.2f}% × 10%
                """
            )


            # =================================================
            # SKILL RESULTS
            # =================================================

            if not_found:

                skill_col1, skill_col2 = st.columns(2)


                with skill_col1:

                    st.write(
                        "### ✅ Matched Skills"
                    )

                    for skill in matched:

                        st.write(
                            f"✅ {skill.title()}"
                        )


                with skill_col2:

                    st.write(
                        "### ⚠️ Not Found / "
                        "Not Clearly Mentioned"
                    )

                    for skill in not_found:

                        st.write(
                            f"⚠️ {skill.title()}"
                        )

            else:

                st.success(
                    "🎉 All Required Skills Found!"
                )


            # =================================================
            # RESUME TEXT
            # =================================================

            with st.expander(
                "📖 View Extracted Resume Text"
            ):

                st.text(
                    resume_text
                )


            st.divider()


        # ====================================================
        # CANDIDATE RANKING
        # ====================================================

        if candidate_results:

            st.header(
                "🏆 Candidate Ranking"
            )


            # ------------------------------------------------
            # DATAFRAME
            # ------------------------------------------------

            ranking_df = pd.DataFrame(
                candidate_results
            )


            # ------------------------------------------------
            # SORT
            # ------------------------------------------------

            ranking_df = ranking_df.sort_values(
                by="Overall Score",
                ascending=False
            ).reset_index(
                drop=True
            )


            # ------------------------------------------------
            # RANK
            # ------------------------------------------------

            ranking_df.insert(
                0,
                "Rank",
                ranking_df.index + 1
            )


            # ------------------------------------------------
            # DISPLAY COLUMNS
            # ------------------------------------------------

            display_df = ranking_df[
                [
                    "Rank",
                    "Candidate",
                    "Skill Match",
                    "Semantic Match",
                    "Experience",
                    "Education",
                    "Overall Score"
                ]
            ].copy()


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            st.dataframe(
                display_df.style.format({

                    "Skill Match": "{:.2f}%",

                    "Semantic Match": "{:.2f}%",

                    "Experience": "{:.2f}%",

                    "Education": "{:.2f}%",

                    "Overall Score": "{:.2f}%"

                }),
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # TOP CANDIDATE
            # =================================================

            top_candidate = ranking_df.iloc[0]


            st.success(
                f"🥇 Top Matching Candidate: "
                f"{top_candidate['Candidate']} "
                f"with an overall match of "
                f"{top_candidate['Overall Score']:.2f}%"
            )


            # =================================================
            # STEP 9 — SMART SHORTLISTING
            # =================================================

            st.divider()

            st.header(
                "🤖 Smart Shortlisting"
            )


            st.write(
                "Configure the shortlist criteria below. "
                "The system will recommend candidates for "
                "recruiter review."
            )


            shortlist_col1, shortlist_col2 = st.columns(2)


            # ------------------------------------------------
            # TOP N
            # ------------------------------------------------

            with shortlist_col1:

                max_candidates = len(
                    ranking_df
                )

                top_n = st.number_input(
                    "Number of Candidates to Shortlist",
                    min_value=1,
                    max_value=max_candidates,
                    value=min(3, max_candidates),
                    step=1
                )


            # ------------------------------------------------
            # MINIMUM SCORE
            # ------------------------------------------------

            with shortlist_col2:

                minimum_score = st.slider(
                    "Minimum Overall Match Score (%)",
                    min_value=0,
                    max_value=100,
                    value=60,
                    step=5
                )


            # ------------------------------------------------
            # CREATE SHORTLIST
            # ------------------------------------------------

            shortlist_df = ranking_df[
                ranking_df["Overall Score"]
                >= minimum_score
            ].head(
                int(top_n)
            )


            # =================================================
            # SHORTLIST RESULTS
            # =================================================

            st.subheader(
                "📋 AI Recommended Shortlist"
            )


            if shortlist_df.empty:

                st.warning(
                    "⚠️ No candidates meet the "
                    "selected shortlist criteria."
                )

                st.info(
                    "Try lowering the minimum match "
                    "score or increasing the number "
                    "of candidates."
                )

            else:

                st.success(
                    f"✅ {len(shortlist_df)} candidate(s) "
                    f"recommended for recruiter review."
                )


                # ------------------------------------------------
                # SHORTLIST TABLE
                # ------------------------------------------------

                shortlist_display = shortlist_df[
                    [
                        "Rank",
                        "Candidate",
                        "Skill Match",
                        "Semantic Match",
                        "Experience",
                        "Education",
                        "Overall Score"
                    ]
                ].copy()


                st.dataframe(
                    shortlist_display.style.format({

                        "Skill Match": "{:.2f}%",

                        "Semantic Match": "{:.2f}%",

                        "Experience": "{:.2f}%",

                        "Education": "{:.2f}%",

                        "Overall Score": "{:.2f}%"

                    }),
                    use_container_width=True,
                    hide_index=True
                )


                # =================================================
                # SHORTLIST EXPLANATIONS
                # =================================================

                st.subheader(
                    "💡 Shortlist Explanation"
                )


                for _, candidate in shortlist_df.iterrows():

                    st.write(
                        f"### 👤 {candidate['Candidate']}"
                    )


                    reasons = []


                    # Skill reason
                    if candidate["Skill Match"] >= 80:

                        reasons.append(
                            f"Strong skill match "
                            f"({candidate['Skill Match']:.2f}%)"
                        )

                    elif candidate["Skill Match"] >= 50:

                        reasons.append(
                            f"Moderate skill match "
                            f"({candidate['Skill Match']:.2f}%)"
                        )

                    else:

                        reasons.append(
                            f"Limited skill match "
                            f"({candidate['Skill Match']:.2f}%)"
                        )


                    # Semantic reason
                    if candidate["Semantic Match"] >= 70:

                        reasons.append(
                            f"Strong JD/resume semantic similarity "
                            f"({candidate['Semantic Match']:.2f}%)"
                        )

                    elif candidate["Semantic Match"] >= 50:

                        reasons.append(
                            f"Moderate JD/resume semantic similarity "
                            f"({candidate['Semantic Match']:.2f}%)"
                        )


                    # Experience reason
                    if candidate["Experience"] >= 100:

                        reasons.append(
                            "Meets the experience requirement"
                        )

                    elif candidate["Experience"] > 0:

                        reasons.append(
                            "Has some relevant experience "
                            "but may not meet the full requirement"
                        )

                    else:

                        reasons.append(
                            "No qualifying professional experience "
                            "was detected"
                        )


                    # Education reason
                    if candidate["Education"] >= 100:

                        reasons.append(
                            "Education requirement matched"
                        )

                    else:

                        reasons.append(
                            "Required education was not detected"
                        )


                    for reason in reasons:

                        st.write(
                            f"• {reason}"
                        )


                    st.divider()


            # =================================================
            # HUMAN REVIEW NOTICE
            # =================================================

            # =================================================
            # STEP 12 — RECRUITER DASHBOARD
            # =================================================

            st.divider()

            st.header("📊 Recruiter Dashboard")

            st.write(
                "A quick overview of candidate performance, "
                "ranking, and shortlist results."
            )

            # ------------------------------------------------
            # DASHBOARD METRICS
            # ------------------------------------------------

            total_candidates = len(ranking_df)

            average_score = ranking_df["Overall Score"].mean()

            top_candidate_name = ranking_df.iloc[0]["Candidate"]

            shortlisted_count = len(shortlist_df)

            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

            with metric_col1:
                st.metric(
                    "👥 Total Candidates",
                    total_candidates
                )

            with metric_col2:
                st.metric(
                    "📈 Average Match Score",
                    f"{average_score:.2f}%"
                )

            with metric_col3:
                st.metric(
                    "🏆 Top Candidate",
                    top_candidate_name
                )

            with metric_col4:
                st.metric(
                    "✅ Shortlisted",
                    shortlisted_count
                )

            # ------------------------------------------------
            # SCORE COMPARISON
            # ------------------------------------------------

            st.subheader("📈 Candidate Score Comparison")

            chart_df = ranking_df[
                ["Candidate", "Overall Score"]
            ].copy()

            chart_df = chart_df.set_index("Candidate")

            st.bar_chart(
                chart_df,
                y="Overall Score",
                use_container_width=True
            )

            # ------------------------------------------------
            # DASHBOARD SUMMARY TABLE
            # ------------------------------------------------

            st.subheader("📋 Candidate Summary")

            dashboard_df = ranking_df[
                [
                    "Rank",
                    "Candidate",
                    "Skill Match",
                    "Semantic Match",
                    "Experience",
                    "Education",
                    "Overall Score"
                ]
            ].copy()

            st.dataframe(
                dashboard_df.style.format({
                    "Skill Match": "{:.2f}%",
                    "Semantic Match": "{:.2f}%",
                    "Experience": "{:.2f}%",
                    "Education": "{:.2f}%",
                    "Overall Score": "{:.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # DASHBOARD NOTE
            # ------------------------------------------------

            st.info(
                "ℹ️ The dashboard summarizes AI-generated matching "
                "results. Recruiters should review candidate resumes "
                "and make the final hiring decision."
            )

            st.info(
                """
                ℹ️ **Recruiter Review Required**

                The shortlist is an AI recommendation based
                only on the job requirements and resume content.

                It should be used as a decision-support tool,
                not as an automatic hiring or rejection system.

                Recruiters should review shortlisted candidates
                before making employment decisions.
                """
            )

            # ============================================================
            # STEP 13 — COMPARE ALL SHORTLISTED CANDIDATES
            # ============================================================

            st.divider()

            st.header("🔎 Compare Shortlisted Candidates")

            st.write(
                "Compare all AI-shortlisted candidates together using "
                "job-relevant matching scores."
            )

            # ------------------------------------------------------------
            # CHECK SHORTLIST
            # ------------------------------------------------------------

            if shortlist_df.empty:

                st.info(
                    "Run Resume Screening and create a shortlist first "
                    "to compare shortlisted candidates."
                )

            elif len(shortlist_df) < 2:

                st.info(
                    "At least 2 shortlisted candidates are required "
                    "for candidate comparison."
                )

            else:

                # --------------------------------------------------------
                # ALL SHORTLISTED CANDIDATES
                # --------------------------------------------------------

                comparison_df = shortlist_df[
                    [
                        "Rank",
                        "Candidate",
                        "Skill Match",
                        "Semantic Match",
                        "Experience",
                        "Education",
                        "Overall Score"
                    ]
                ].copy()

                st.subheader(
                    f"👥 Shortlisted Candidates ({len(comparison_df)})"
                )

                st.dataframe(
                    comparison_df.style.format({
                        "Skill Match": "{:.2f}%",
                        "Semantic Match": "{:.2f}%",
                        "Experience": "{:.2f}%",
                        "Education": "{:.2f}%",
                        "Overall Score": "{:.2f}%"
                    }),
                    use_container_width=True,
                    hide_index=True
                )

                # --------------------------------------------------------
                # OVERALL SCORE CHART
                # --------------------------------------------------------

                st.subheader("📊 Shortlisted Candidate Score Comparison")

                comparison_chart = comparison_df[
                    ["Candidate", "Overall Score"]
                ].copy()

                comparison_chart = comparison_chart.set_index(
                    "Candidate"
                )

                st.bar_chart(
                    comparison_chart,
                    y="Overall Score",
                    use_container_width=True
                )

                # --------------------------------------------------------
                # TOP SHORTLISTED CANDIDATE
                # --------------------------------------------------------

                top_shortlisted = comparison_df.iloc[
                    comparison_df["Overall Score"].idxmax()
                ]

                st.success(
                    f"🏆 Highest Overall Score: "
                    f"**{top_shortlisted['Candidate']}** "
                    f"({top_shortlisted['Overall Score']:.2f}%)"
                )

                # --------------------------------------------------------
                # CANDIDATE-BY-CANDIDATE STRENGTHS
                # --------------------------------------------------------

                st.subheader("💡 Candidate Strengths")

                for _, candidate in comparison_df.iterrows():

                    candidate_name = candidate["Candidate"]

                    with st.expander(
                        f"👤 {candidate_name} — "
                        f"{candidate['Overall Score']:.2f}%"
                    ):

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                f"**Skill Match:** "
                                f"{candidate['Skill Match']:.2f}%"
                            )

                            st.write(
                                f"**Semantic Match:** "
                                f"{candidate['Semantic Match']:.2f}%"
                            )

                        with col2:

                            st.write(
                                f"**Experience Match:** "
                                f"{candidate['Experience']:.2f}%"
                            )

                            st.write(
                                f"**Education Match:** "
                                f"{candidate['Education']:.2f}%"
                            )

                        candidate_details = next(
                            (
                                result
                                for result in candidate_results
                                if result["Candidate"] == candidate_name
                            ),
                            None
                        )

                        if candidate_details:

                            matched_skills = candidate_details[
                                "Matched Skills"
                            ]

                            missing_skills = candidate_details[
                                "Missing Skills"
                            ]

                            st.write("**Matched Skills:**")

                            if matched_skills:
                                st.success(
                                    ", ".join(matched_skills)
                                )
                            else:
                                st.write("No required skills matched.")

                            st.write("**Missing / Unclear Skills:**")

                            if missing_skills:
                                st.warning(
                                    ", ".join(missing_skills)
                                )
                            else:
                                st.success(
                                    "All required skills were matched."
                                )

                # --------------------------------------------------------
                # RECRUITER REVIEW NOTICE
                # --------------------------------------------------------

                st.info(
                    """
                    ℹ️ **Recruiter Review Required**

                    This comparison is an AI-assisted decision-support feature.
                    It compares candidates using job-relevant resume information
                    such as skills, semantic relevance, experience, education,
                    and overall matching score.

                    Recruiters should review the actual resumes and make the
                    final hiring decision. The system does not automatically
                    hire or reject candidates.
                    """
                )

            # ============================================================
            # STEP 14 — EXPORT RECRUITER REPORT
            # ============================================================

            st.divider()

            st.header("📥 Export Recruiter Report")

            st.write(
                "Download the candidate ranking and shortlist results "
                "for recruiter review."
            )

            if not ranking_df.empty:

                # --------------------------------------------------------
                # EXCEL REPORT
                # --------------------------------------------------------

                export_df = ranking_df[
                    [
                        "Rank",
                        "Candidate",
                        "Skill Match",
                        "Semantic Match",
                        "Experience",
                        "Education",
                        "Overall Score"
                    ]
                ].copy()

                excel_buffer = BytesIO()

                with pd.ExcelWriter(
                    excel_buffer,
                    engine="openpyxl"
                ) as writer:

                    export_df.to_excel(
                        writer,
                        sheet_name="Candidate Ranking",
                        index=False
                    )

                    if not shortlist_df.empty:

                        shortlist_export = shortlist_df[
                            [
                                "Rank",
                                "Candidate",
                                "Skill Match",
                                "Semantic Match",
                                "Experience",
                                "Education",
                                "Overall Score"
                            ]
                        ].copy()

                        shortlist_export.to_excel(
                            writer,
                            sheet_name="Shortlist",
                            index=False
                        )

                excel_buffer.seek(0)

                st.download_button(
                    label="📊 Download Excel Report",
                    data=excel_buffer.getvalue(),
                    file_name="AI_Recruiter_Candidate_Report.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )
                )

                st.caption(
                    "The Excel report contains candidate ranking and, "
                    "when available, the shortlist."
                )

            else:

                st.info(
                    "Run Resume Screening first to generate an exportable report."
                )
