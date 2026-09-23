from flask import Flask, render_template, request
from pypdf import PdfReader
import re

app = Flask(__name__)


# =====================================================
# JOB ROLES AND REQUIRED SKILLS
# =====================================================

jobs = {

    "Python Developer": [
        "python",
        "sql",
        "git"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel"
    ],

    "AI/ML Intern": [
        "python",
        "artificial intelligence",
        "machine learning"
    ],

    "Software Test Engineer": [
        "software testing",
        "sql",
        "jira",
        "katalon studio"
    ],

    "QA Engineer": [
        "software testing",
        "jira",
        "etl",
        "sql"
    ],

    "ETL Tester": [
        "etl",
        "sql",
        "informatica",
        "software testing"
    ]
}


# =====================================================
# SMART SKILL KEYWORDS
# =====================================================

possible_skills = {

    "python": [
        "python",
        "python programming",
        "pandas"
    ],

    "sql": [
        "sql",
        "sql server",
        "mysql",
        "postgresql"
    ],

    "git": [
        "git",
        "github",
        "version control"
    ],

    "excel": [
        "excel",
        "microsoft excel",
        "spreadsheets"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai development",
        "ai developer"
    ],

    "machine learning": [
        "machine learning",
        "ml development",
        "ml model"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "java": [
        "java programming",
        "java developer",
        "java developer intern",
        "java language",
        "core java",
        "advanced java",
        "java skills"
    ],

    "javascript": [
        "javascript",
        "javascript programming",
        "javascript developer"
    ],

    "html": [
        "html",
        "html5",
        "html programming"
    ],

    "css": [
        "css",
        "css3",
        "css styling"
    ],

    "software testing": [
        "software testing",
        "software test engineer",
        "software quality assurance",
        "quality assurance",
        "qa testing",
        "testing life cycle",
        "test case"
    ],

    "katalon studio": [
        "katalon studio",
        "katalon"
    ],

    "jira": [
        "jira",
        "atlassian jira"
    ],

    "azure": [
        "azure factory",
        "azure data factory",
        "microsoft azure"
    ],

    "informatica": [
        "informatica",
        "informatica powercenter"
    ],

    "etl": [
        "etl testing",
        "etl",
        "extract transform load"
    ]
}


# =====================================================
# LEARNING RESOURCES
# =====================================================

learning_resources = {

    "python": {
        "name": "Python Tutorial",
        "url": "https://docs.python.org/3/tutorial/"
    },

    "sql": {
        "name": "SQL Tutorial",
        "url": "https://www.w3schools.com/sql/"
    },

    "git": {
        "name": "Git Documentation",
        "url": "https://git-scm.com/doc"
    },

    "excel": {
        "name": "Microsoft Excel Learning",
        "url": "https://support.microsoft.com/en-us/excel/"
    },

    "artificial intelligence": {
        "name": "Google Machine Learning Resources",
        "url": "https://developers.google.com/machine-learning"
    },

    "machine learning": {
        "name": "Google Machine Learning Crash Course",
        "url": "https://developers.google.com/machine-learning/crash-course"
    },

    "software testing": {
        "name": "Software Testing Learning",
        "url": "https://www.guru99.com/software-testing.html"
    },

    "jira": {
        "name": "Atlassian Jira Learning",
        "url": "https://www.atlassian.com/software/jira/guides"
    },

    "katalon studio": {
        "name": "Katalon Learning",
        "url": "https://academy.katalon.com/"
    },

    "informatica": {
        "name": "Informatica Learning",
        "url": "https://knowledge.informatica.com/"
    },

    "etl": {
        "name": "ETL Testing Tutorial",
        "url": "https://www.guru99.com/etl-testing.html"
    }
}


# =====================================================
# JOB SEARCH LINKS
# =====================================================

job_search_links = {

    "Python Developer":
        "https://in.linkedin.com/jobs/python-developer-jobs-pune",

    "Data Analyst":
        "https://www.linkedin.com/jobs/data-analyst-jobs-pune",

    "AI/ML Intern":
        "https://www.linkedin.com/jobs/artificial-intelligence-intern-jobs-pune",

    "Software Test Engineer":
        "https://in.linkedin.com/jobs/software-test-engineer-jobs-pune",

    "QA Engineer":
        "https://in.linkedin.com/jobs/qa-engineer-jobs-pune",

    "ETL Tester":
        "https://www.linkedin.com/jobs/etl-tester-jobs-pune"
}


# =====================================================
# CAREER ROADMAP
# =====================================================

def create_roadmap(job, matching, missing):

    roadmap = []

    if matching:

        roadmap.append(
            "Strengthen your existing skills: "
            + ", ".join(matching)
            + "."
        )

    else:

        roadmap.append(
            "Start building the core skills required for "
            + job
            + "."
        )


    if missing:

        roadmap.append(
            "Learn the missing skills: "
            + ", ".join(missing)
            + "."
        )

    else:

        roadmap.append(
            "Continue practicing all required skills through hands-on work."
        )


    roadmap.append(
        "Build at least one practical project related to "
        + job
        + "."
    )


    roadmap.append(
        "Add your projects, skills, certifications, and practical experience to your resume."
    )


    roadmap.append(
        "Review suitable job opportunities and prepare for interviews."
    )


    return roadmap


# =====================================================
# RESUME STRENGTH ANALYZER
# =====================================================

def analyze_resume(resume_text, detected_skills):

    text = resume_text.lower().strip()

    score = 0

    checks = []

    suggestions = []


    # =================================================
    # COMMON SECTION KEYWORDS
    # =================================================

    section_keywords = {

        "skills": [
            "skills",
            "technical skills",
            "technical skill",
            "key skills",
            "core skills",
            "core competencies",
            "technical competencies",
            "skill set"
        ],

        "education": [
            "education",
            "educational qualifications",
            "academic qualifications",
            "qualifications",
            "bachelor",
            "b.tech",
            "btech",
            "degree",
            "college",
            "university",
            "higher secondary"
        ],

        "projects": [
            "projects",
            "project",
            "academic projects",
            "academic project",
            "personal projects",
            "personal project",
            "technical projects",
            "technical project"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "work history",
            "internship",
            "internships",
            "intern",
            "training experience"
        ],

        "certifications": [
            "certification",
            "certifications",
            "certificate",
            "certificates",
            "courses",
            "training and certifications",
            "professional certifications"
        ],

        "profile": [
            "summary",
            "profile",
            "profile summary",
            "professional summary",
            "career objective",
            "objective",
            "about me",
            "professional profile"
        ]
    }


    # =================================================
    # HELPER
    # =================================================

    def section_found(words):

        for word in words:

            if re.search(
                r"\b" + re.escape(word) + r"\b",
                text
            ):
                return True

        return False


    # =================================================
    # 1. CONTACT INFORMATION
    # =================================================

    has_email = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    has_phone = bool(
        re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            text
        )
    )


    if has_email or has_phone:

        score += 10

        checks.append({
            "name": "Contact information",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Contact information",
            "status": "missing"
        })

        suggestions.append(
            "Make sure your email address and phone number are easy to find."
        )


    # =================================================
    # 2. SKILLS SECTION
    # =================================================

    if section_found(section_keywords["skills"]):

        score += 10

        checks.append({
            "name": "Skills section",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Skills section",
            "status": "missing"
        })

        suggestions.append(
            "Add a clear Technical Skills or Core Skills section."
        )


    # =================================================
    # 3. EDUCATION
    # =================================================

    if section_found(section_keywords["education"]):

        score += 10

        checks.append({
            "name": "Education",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Education",
            "status": "missing"
        })

        suggestions.append(
            "Add your degree, institution, qualification, and relevant dates."
        )


    # =================================================
    # 4. PROJECTS
    # =================================================

    if section_found(section_keywords["projects"]):

        score += 10

        checks.append({
            "name": "Projects section",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Projects section",
            "status": "missing"
        })

        suggestions.append(
            "Add at least one academic, personal, or technical project."
        )


    # =================================================
    # 5. EXPERIENCE
    # =================================================

    if section_found(section_keywords["experience"]):

        score += 10

        checks.append({
            "name": "Experience",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Experience",
            "status": "missing"
        })

        suggestions.append(
            "Add internships, training, work experience, or practical experience when applicable."
        )


    # =================================================
    # 6. CERTIFICATIONS
    # =================================================

    if section_found(section_keywords["certifications"]):

        score += 10

        checks.append({
            "name": "Certifications",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Certifications",
            "status": "missing"
        })

        suggestions.append(
            "Add relevant certifications, courses, or training you have completed."
        )


    # =================================================
    # 7. PROFILE / SUMMARY
    # =================================================

    if section_found(section_keywords["profile"]):

        score += 10

        checks.append({
            "name": "Profile / Summary",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Profile / Summary",
            "status": "missing"
        })

        suggestions.append(
            "Add a short professional summary or career objective."
        )


    # =================================================
    # 8. ACTION-ORIENTED CONTENT
    # =================================================

    action_words = [

        "developed",
        "implemented",
        "tested",
        "designed",
        "analyzed",
        "created",
        "built",
        "automated",
        "managed",
        "improved",
        "configured",
        "optimized"

    ]


    action_count = 0

    for word in action_words:

        action_count += len(
            re.findall(
                r"\b" + re.escape(word) + r"\b",
                text
            )
        )


    if action_count >= 3:

        score += 10

        checks.append({
            "name": "Action-oriented content",
            "status": "strong"
        })

    else:

        checks.append({
            "name": "Action-oriented content",
            "status": "improve"
        })

        suggestions.append(
            "Use stronger action words such as developed, implemented, tested, analyzed, automated, and built."
        )


    # =================================================
    # 9. QUANTIFIED ACHIEVEMENTS
    # =================================================

    number_patterns = [

        r"\b\d+%",
        r"\b\d+\+",
        r"\b\d+\s*(?:users|projects|cases|tests|clients|records|reports)",
        r"\b(?:increased|decreased|improved|reduced|saved|grew)\b.{0,50}\d+"

    ]


    quantified_found = False

    for pattern in number_patterns:

        if re.search(pattern, text):

            quantified_found = True

            break


    if quantified_found:

        score += 5

        checks.append({
            "name": "Quantified achievements",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Quantified achievements",
            "status": "improve"
        })

        suggestions.append(
            "Where appropriate, add measurable results such as percentages, counts, time saved, or number of users."
        )


    # =================================================
    # 10. PROFESSIONAL LINKS
    # =================================================

    has_linkedin = (
        "linkedin.com" in text
        or "linkedin" in text
    )

    has_github = (
        "github.com" in text
        or "github" in text
    )


    if has_linkedin or has_github:

        score += 5

        checks.append({
            "name": "Professional links",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Professional links",
            "status": "improve"
        })

        suggestions.append(
            "Consider adding a professional LinkedIn or GitHub link when relevant."
        )


    # =================================================
    # 11. RELEVANT KEYWORDS
    # =================================================

    keyword_count = len(detected_skills)


    if keyword_count >= 5:

        score += 5

        checks.append({
            "name": "Relevant technical keywords",
            "status": "strong"
        })

    elif keyword_count >= 2:

        score += 3

        checks.append({
            "name": "Relevant technical keywords",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Relevant technical keywords",
            "status": "improve"
        })

        suggestions.append(
            "Include relevant technical skills and tools that match your target career."
        )


    # =================================================
    # 12. CONTENT LENGTH
    # =================================================

    word_count = len(
        re.findall(
            r"\b[\w+#.-]+\b",
            text
        )
    )


    if word_count >= 250:

        score += 5

        checks.append({
            "name": "Resume content length",
            "status": "found"
        })

    else:

        checks.append({
            "name": "Resume content length",
            "status": "improve"
        })

        suggestions.append(
            "Your extracted resume text is quite short; make sure important education, projects, skills, and experience are included."
        )


    # =================================================
    # SCORE LIMIT
    # =================================================

    score = min(score, 100)


    # =================================================
    # RESUME LEVEL
    # =================================================

    if score >= 85:

        level = "Excellent Resume"

    elif score >= 70:

        level = "Strong Resume"

    elif score >= 55:

        level = "Good Resume"

    elif score >= 40:

        level = "Needs Improvement"

    else:

        level = "Needs Major Improvement"


    # =================================================
    # DEFAULT SUGGESTION
    # =================================================

    if not suggestions:

        suggestions.append(
            "Your resume contains the major elements being checked. Keep improving it with measurable achievements and strong project descriptions."
        )


    return {

        "score": score,

        "level": level,

        "checks": checks,

        "suggestions": suggestions

    }


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# MATCH PAGE
# =====================================================

@app.route("/match", methods=["POST"])
def match():

    name = request.form.get(
        "name",
        ""
    ).strip()


    skills_text = request.form.get(
        "skills",
        ""
    )


    # =================================================
    # MANUAL SKILLS
    # =================================================

    student_skills = [

        skill.strip().lower()

        for skill in skills_text.split(",")

        if skill.strip()

    ]


    # =================================================
    # READ RESUME PDF
    # =================================================

    resume = request.files.get(
        "resume"
    )


    resume_text = ""


    if resume and resume.filename:

        try:

            reader = PdfReader(resume)

            for page in reader.pages:

                text = page.extract_text() or ""

                resume_text += text + "\n"

        except Exception as error:

            print(
                "Could not read PDF:",
                error
            )


    resume_lower = resume_text.lower()


    # =================================================
    # CHECK RESUME TEXT
    # =================================================

    resume_available = bool(resume_text.strip())

    if not resume_available:
        print("WARNING: No readable text was extracted from the PDF.")


    # =================================================
    # SMART SKILL DETECTION
    # =================================================

    for skill, keywords in possible_skills.items():

        for keyword in keywords:

            pattern = (
                r"\b"
                + re.escape(keyword.lower())
                + r"\b"
            )


            if re.search(
                pattern,
                resume_lower
            ):

                if skill not in student_skills:

                    student_skills.append(skill)

                break


    # =================================================
    # RESUME STRENGTH ANALYSIS
    # =================================================

    resume_analysis = analyze_resume(

        resume_text,

        student_skills

    )


    # =================================================
    # JOB MATCHING
    # =================================================

    results = []


    for job, required_skills in jobs.items():

        matching = []


        for skill in required_skills:

            if skill in student_skills:

                matching.append(skill)


        # ---------------------------------------------
        # MATCH PERCENTAGE
        # ---------------------------------------------

        percentage = (

            len(matching)
            /
            len(required_skills)

        ) * 100


        # ---------------------------------------------
        # MISSING SKILLS
        # ---------------------------------------------

        missing = []


        for skill in required_skills:

            if skill not in student_skills:

                missing.append(skill)


        # ---------------------------------------------
        # LEARNING RECOMMENDATIONS
        # ---------------------------------------------

        recommendations = []


        for skill in missing:

            if skill in learning_resources:

                recommendations.append({

                    "name":
                    learning_resources[skill]["name"],

                    "url":
                    learning_resources[skill]["url"]

                })


        # ---------------------------------------------
        # RESUME SUGGESTIONS
        # ---------------------------------------------

        resume_suggestions = []


        for skill in matching:

            resume_suggestions.append(

                "Highlight your "
                + skill
                + " experience in your resume."

            )


        for skill in missing:

            resume_suggestions.append(

                "Consider adding projects or experience related to "
                + skill
                + "."

            )


        if not resume_suggestions:

            resume_suggestions.append(

                "Add relevant projects, certifications, and practical experience."

            )


        # ---------------------------------------------
        # CAREER ROADMAP
        # ---------------------------------------------

        roadmap = create_roadmap(

            job,

            matching,

            missing

        )


        # ---------------------------------------------
        # JOB SEARCH
        # ---------------------------------------------

        job_search_url = job_search_links.get(

            job,

            "https://www.linkedin.com/jobs/"

        )


        # ---------------------------------------------
        # STORE RESULT
        # ---------------------------------------------

        results.append({

            "job": job,

            "percentage":
            round(percentage, 2),

            "matching":
            matching,

            "missing":
            missing,

            "recommendations":
            recommendations,

            "resume_suggestions":
            resume_suggestions,

            "roadmap":
            roadmap,

            "job_search_url":
            job_search_url

        })


    # =================================================
    # BEST MATCH
    # =================================================

    best_job = max(

        results,

        key=lambda x:
        x["percentage"]

    )


    # =================================================
    # BEST MATCH RESUME SUGGESTIONS
    # =================================================

    best_resume_suggestions = []


    for skill in best_job["matching"]:

        best_resume_suggestions.append(

            "Make your "
            + skill
            + " experience clearly visible in your resume."

        )


    for skill in best_job["missing"]:

        best_resume_suggestions.append(

            "Add a project, certification, or experience related to "
            + skill
            + " when you develop that skill."

        )


    if not best_resume_suggestions:

        best_resume_suggestions.append(

            "Your resume already highlights the skills required for this role."

        )


    best_job[
        "resume_suggestions"
    ] = best_resume_suggestions


    # =================================================
    # BEST MATCH ROADMAP
    # =================================================

    best_job["roadmap"] = create_roadmap(

        best_job["job"],

        best_job["matching"],

        best_job["missing"]

    )


    # =================================================
    # DETECTED SKILLS
    # =================================================

    detected_skills = student_skills


    # =================================================
    # SEND RESULTS
    # =================================================

    return render_template(

        "result.html",

        name=name,

        results=results,

        best_job=best_job,

        detected_skills=detected_skills,

        resume_analysis=resume_analysis,

        resume_available=resume_available

    )


# =====================================================
# START FLASK
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )