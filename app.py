"""
AI Code Review & Refactoring Agent
A beginner-friendly tool to analyze and improve Python code using AI
"""

import streamlit as st
import os
from openai import OpenAI

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🤖",
    layout="wide"
)

# ========================================
# CUSTOM CSS
# ========================================
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton>button:hover { background-color: #45a049; }
    .quality-score {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-excellent { background-color: #d4edda; color: #155724; }
    .score-good { background-color: #d1ecf1; color: #0c5460; }
    .score-fair { background-color: #fff3cd; color: #856404; }
    .score-poor { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

# ========================================
# OPENAI CLIENT SETUP (FIXED)
# ========================================

def get_openai_client():
    """
    Create and return an OpenAI client.
    First try Streamlit secrets (for Streamlit Cloud),
    then fallback to environment variables (for local/Replit).
    """
    api_key = None

    # Streamlit Cloud secrets
    if "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
    else:
        # Local / Replit
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)

# ========================================
# HELPER FUNCTIONS
# ========================================

def calculate_quality_score(review_text):
    review_lower = review_text.lower()

    negative_keywords = [
        'bug', 'error', 'issue', 'problem', 'inefficient',
        'poor', 'bad practice', 'unnecessary', 'redundant',
        'memory leak', 'security', 'vulnerable'
    ]

    positive_keywords = [
        'good', 'well', 'clean', 'efficient', 'optimized',
        'best practice', 'excellent', 'proper'
    ]

    negative_count = sum(review_lower.count(word) for word in negative_keywords)
    positive_count = sum(review_lower.count(word) for word in positive_keywords)

    score = 70 - (negative_count * 8) + (positive_count * 5)
    return max(0, min(100, score))


def get_score_class(score):
    if score >= 85:
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 50:
        return "score-fair"
    return "score-poor"


def get_score_label(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    return "Needs Improvement"


# ========================================
# OPENAI FUNCTIONS
# ========================================

def review_code(code, client):
    prompt = f"""
You are an expert code reviewer helping beginners understand and improve their code.

Analyze this Python code and provide:
1. Code explanation (simple language)
2. Bugs or issues
3. Code quality problems
4. Performance issues
5. Best practices
6. Security concerns

CODE:
{code}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful beginner-friendly code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error during code review: {str(e)}"


def refactor_code(code, client):
    prompt = f"""
Refactor this Python code to:
- Be cleaner
- Follow PEP8
- Be efficient
- Add helpful comments

Return ONLY Python code.

CODE:
{code}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Python expert. Return only refactored code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"# Error during refactoring: {str(e)}"


# ========================================
# MAIN APP
# ========================================

def main():
    st.title("🤖 AI Code Review & Refactoring Agent")

    st.markdown("""
    Improve your Python code with AI!
    - Understand your code
    - Find bugs
    - Learn best practices
    - Get refactored version
    """)

    st.divider()

    client = get_openai_client()

    if not client:
        st.error("⚠️ OpenAI API Key not found!")
        st.info("Add OPENAI_API_KEY in Streamlit Cloud → App Settings → Secrets")
        st.stop()

    col1, col2 = st.columns(2)

    with col1:
        code_input = st.text_area(
            "Paste your Python code:",
            height=300,
            placeholder="def hello():\n    print('Hello World')"
        )

        uploaded_file = st.file_uploader("Upload .py file", type=["py"])

        if uploaded_file:
            code_input = uploaded_file.read().decode("utf-8")
            st.success(f"Loaded: {uploaded_file.name}")

    with col2:
        review_clicked = st.button("🔍 Review Code", use_container_width=True)
        refactor_clicked = st.button("✨ Refactor Code", use_container_width=True)

    st.divider()

    if review_clicked and code_input:
        with st.spinner("AI reviewing your code..."):
            review_result = review_code(code_input, client)
            score = calculate_quality_score(review_result)

            st.success("Review Complete!")
            st.markdown(f"### Quality Score: {score}/100 ({get_score_label(score)})")
            st.markdown(review_result)

    if refactor_clicked and code_input:
        with st.spinner("AI refactoring your code..."):
            refactored = refactor_code(code_input, client)
            st.success("Refactoring Complete!")
            st.code(refactored, language="python")


# ========================================
# RUN
# ========================================

if __name__ == "__main__":
    main()
