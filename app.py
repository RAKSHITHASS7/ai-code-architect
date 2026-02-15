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
# CUSTOM CSS FOR BETTER UI
# ========================================
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .quality-score {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-excellent {
        background-color: #d4edda;
        color: #155724;
    }
    .score-good {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .score-fair {
        background-color: #fff3cd;
        color: #856404;
    }
    .score-poor {
        background-color: #f8d7da;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# HELPER FUNCTIONS
# ========================================

def get_openai_client():
    """
    Create and return an OpenAI client using the API key from environment variables.
    If no API key is found, returns None.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def calculate_quality_score(review_text):
    """
    Calculate a simple quality score based on the AI review.
    This is a basic implementation that looks for keywords.
    Returns a score between 0-100.
    """
    review_lower = review_text.lower()
    
    # Negative indicators (reduce score)
    negative_keywords = [
        'bug', 'error', 'issue', 'problem', 'inefficient', 
        'poor', 'bad practice', 'unnecessary', 'redundant',
        'memory leak', 'security', 'vulnerable'
    ]
    
    # Positive indicators (increase score)
    positive_keywords = [
        'good', 'well', 'clean', 'efficient', 'optimized',
        'best practice', 'excellent', 'proper'
    ]
    
    # Count occurrences
    negative_count = sum(review_lower.count(word) for word in negative_keywords)
    positive_count = sum(review_lower.count(word) for word in positive_keywords)
    
    # Calculate base score (start at 70)
    base_score = 70
    score = base_score - (negative_count * 8) + (positive_count * 5)
    
    # Clamp between 0-100
    score = max(0, min(100, score))
    
    return score


def get_score_class(score):
    """
    Return CSS class based on score value
    """
    if score >= 85:
        return "score-excellent"
    elif score >= 70:
        return "score-good"
    elif score >= 50:
        return "score-fair"
    else:
        return "score-poor"


def get_score_label(score):
    """
    Return a label based on score value
    """
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Needs Improvement"


def review_code(code, client):
    """
    Send code to OpenAI for review and analysis.
    Returns the AI's review as a string.
    """
    prompt = f"""You are an expert code reviewer helping beginners understand and improve their code.

Analyze the following Python code and provide:

1. **Code Explanation**: Explain what this code does in simple, beginner-friendly language.

2. **Issues Found**: Identify any bugs, errors, or potential problems.

3. **Code Quality Issues**: Point out poor variable names, lack of comments, code duplication, or style issues.

4. **Performance Issues**: Highlight any inefficiencies or better approaches.

5. **Best Practices**: Suggest Python best practices that should be followed.

6. **Security Concerns**: Mention any security issues if present.

Be specific, clear, and educational. Use simple language suitable for beginners.

CODE TO REVIEW:
```python
{code}
```

Please provide your analysis:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful code review assistant that explains things clearly to beginners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during code review: {str(e)}"


def refactor_code(code, client):
    """
    Send code to OpenAI for refactoring.
    Returns the refactored code as a string.
    """
    prompt = f"""You are an expert Python developer. Refactor the following code to make it:
- Cleaner and more readable
- More efficient
- Following Python best practices (PEP 8)
- Well-commented
- Using better variable/function names
- Properly structured

IMPORTANT: Return ONLY the refactored Python code with comments. Do NOT include explanations, markdown formatting, or anything else. Just the clean code.

CODE TO REFACTOR:
```python
{code}
```

Refactored code:"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Python expert who refactors code to be clean and efficient. Return only code, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        refactored = response.choices[0].message.content
        
        # Clean up the response (remove markdown code blocks if present)
        refactored = refactored.strip()
        if refactored.startswith("```python"):
            refactored = refactored[9:]  # Remove ```python
        if refactored.startswith("```"):
            refactored = refactored[3:]  # Remove ```
        if refactored.endswith("```"):
            refactored = refactored[:-3]  # Remove trailing ```
        
        return refactored.strip()
    except Exception as e:
        return f"# Error during refactoring: {str(e)}"


# ========================================
# MAIN APPLICATION
# ========================================

def main():
    # Title and description
    st.title("🤖 AI Code Review & Refactoring Agent")
    st.markdown("""
    **Improve your Python code with AI!** 
    
    This tool helps you:
    - Understand what your code does
    - Find bugs and issues
    - Learn best practices
    - Get a cleaner, refactored version
    """)
    
    st.divider()
    
    # Check for API key
    client = get_openai_client()
    
    if not client:
        st.error("⚠️ **OpenAI API Key not found!**")
        st.info("""
        **To use this app, you need to set your OpenAI API key:**
        
        1. Get your API key from: https://platform.openai.com/api-keys
        2. In Replit, go to the **Secrets** tab (🔒 icon in left sidebar)
        3. Add a new secret:
           - Key: `OPENAI_API_KEY`
           - Value: `your-api-key-here`
        4. Click "Add Secret" and refresh this page
        """)
        st.stop()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Your Code")
        
        # Option 1: Paste code
        code_input = st.text_area(
            "Paste your Python code here:",
            height=300,
            placeholder="def hello():\n    print('Hello, World!')"
        )
        
        st.markdown("**OR**")
        
        # Option 2: Upload file
        uploaded_file = st.file_uploader(
            "Upload a Python file (.py)",
            type=['py']
        )
        
        # If file is uploaded, use its content
        if uploaded_file is not None:
            code_input = uploaded_file.read().decode("utf-8")
            st.success(f"✅ Loaded: {uploaded_file.name}")
    
    with col2:
        st.subheader("🎯 Actions")
        
        # Review button
        review_clicked = st.button("🔍 Review Code", use_container_width=True)
        
        # Refactor button
        refactor_clicked = st.button("✨ Refactor Code", use_container_width=True)
        
        # Clear button
        if st.button("🗑️ Clear All", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # ========================================
    # HANDLE REVIEW BUTTON
    # ========================================
    if review_clicked:
        if not code_input or code_input.strip() == "":
            st.warning("⚠️ Please enter some code to review!")
        else:
            with st.spinner("🤖 AI is reviewing your code..."):
                review_result = review_code(code_input, client)
                
                # Calculate quality score
                quality_score = calculate_quality_score(review_result)
                score_class = get_score_class(quality_score)
                score_label = get_score_label(quality_score)
                
                # Display results
                st.success("✅ Review Complete!")
                
                # Show quality score
                st.markdown(f"""
                <div class="quality-score {score_class}">
                    {quality_score}/100
                    <div style="font-size: 20px; margin-top: 10px;">{score_label}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show review
                st.subheader("📋 Detailed Review")
                st.markdown(review_result)
                
                # Show original code for reference
                with st.expander("👀 View Original Code"):
                    st.code(code_input, language="python")
    
    # ========================================
    # HANDLE REFACTOR BUTTON
    # ========================================
    if refactor_clicked:
        if not code_input or code_input.strip() == "":
            st.warning("⚠️ Please enter some code to refactor!")
        else:
            with st.spinner("✨ AI is refactoring your code..."):
                refactored_result = refactor_code(code_input, client)
                
                # Display results in two columns
                st.success("✅ Refactoring Complete!")
                
                col_before, col_after = st.columns(2)
                
                with col_before:
                    st.subheader("📝 Before (Original)")
                    st.code(code_input, language="python")
                
                with col_after:
                    st.subheader("✨ After (Refactored)")
                    st.code(refactored_result, language="python")
                
                # Add download button
                st.download_button(
                    label="💾 Download Refactored Code",
                    data=refactored_result,
                    file_name="refactored_code.py",
                    mime="text/plain"
                )


# ========================================
# RUN THE APP
# ========================================
if __name__ == "__main__":
    main()
