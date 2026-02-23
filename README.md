
# 🤖 AI Code Architect

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An intelligent AI-powered tool that analyzes Python code, identifies issues, provides quality scores, and generates refactored versions using GPT-3.5.

## 🚀 Live Demo

**[Try it now!](https://https://ai-code-architect.streamlit.app/**

> Replace the URL above with your actual Streamlit app URL after deployment

## ✨ Features

- 🔍 **AI Code Review**: Get detailed analysis of your Python code with beginner-friendly explanations
- 📊 **Quality Scoring**: Overall code quality score (0-100) with color-coded feedback
- 🎯 **5 Detailed Metrics**: 
  - Readability
  - Maintainability
  - Performance
  - Security
  - Best Practices
- ✨ **Code Refactoring**: Get a cleaner, improved version of your code automatically
- 🔍 **PEP 8 Style Checks**: Instant local validation (line length, whitespace, naming conventions)
- 💾 **Session Persistence**: Your code and results stay while you work
- 📥 **File Upload**: Upload `.py` files directly
- 📥 **Download Results**: Export refactored code

## 📸 Screenshots

![AI Code Architect Homepage](screenshots/homepage.png)
*Main interface with code input*

![Code Review Results](screenshots/review.png)
*Detailed AI analysis with quality scores*

![Before After Comparison](screenshots/refactor.png)
*Side-by-side code comparison*

> Add your own screenshots in a `screenshots` folder

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web framework for data apps
- **OpenAI GPT-3.5-turbo** - AI-powered code analysis
- **Regex & JSON** - Data parsing and extraction

## 📖 How to Use

### Online (Recommended)

1. Visit the [live app](https://your-app-url.streamlit.app)
2. Enter your OpenAI API key in the left sidebar
3. Paste your Python code or upload a `.py` file
4. Click **"Review Code"** for detailed analysis
5. Click **"Refactor Code"** for an improved version

### Running Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-architect.git
cd ai-code-architect

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key (choose one method)
# Method 1: Environment variable
export OPENAI_API_KEY='your-api-key-here'  # Mac/Linux
set OPENAI_API_KEY=your-api-key-here      # Windows

# Method 2: Enter in the app sidebar when it starts

# Run the app
streamlit run app.py

# Open browser to http://localhost:8501
```

## 🔑 Getting an API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click **"Create new secret key"**
4. Give it a name (e.g., "ai-code-architect")
5. Copy the key (starts with `sk-`)
6. Paste it into the app's sidebar

## 💰 Cost

- **Approximate cost**: $0.001 per code review (less than a penny!)
- **Model**: GPT-3.5-turbo (cost-effective and fast)
- **Free credits**: OpenAI provides $5 in free credits for new users
- **Estimate**: ~4,000-5,000 code reviews with free credits

## 🎯 Use Cases

- **Learning**: Understand what your code does and how to improve it
- **Code Quality**: Get objective quality scores for your projects
- **Refactoring**: Quickly improve code readability and structure
- **Best Practices**: Learn Python conventions and standards
- **Bug Detection**: Find potential issues before they cause problems
- **Interview Prep**: Practice explaining and improving code

## 🎨 Key Improvements in This Version

✅ **AI-based quality scoring** - Uses structured JSON responses from GPT  
✅ **Sidebar API key input** - Easy setup without environment variables  
✅ **Session state persistence** - No data loss between interactions  
✅ **Local PEP 8 checks** - Instant feedback without API calls  
✅ **Detailed metrics breakdown** - 5 separate quality dimensions  
✅ **Professional UI** - Clean sidebar organization and styling  

## 📂 Project Structure

```
ai-code-architect/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── screenshots/          # App screenshots (optional)
    ├── homepage.png
    ├── review.png
    └── refactor.png
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests

## 📝 Example Usage

### Input Code:
```python
def calc(x,y,op):
    if op=='/':
        return x/y
    return 0

result=calc(10,0,'/')
print(result)
```

### AI Analysis:
- **Overall Score**: 40/100 (Needs Improvement)
- **Issues Found**: Division by zero error, poor variable names
- **Suggestions**: Add error handling, use better names, add docstrings

### Refactored Code:
```python
def calculate(dividend: int, divisor: int, operation: str) -> float:
    """
    Perform a calculation based on the specified operation.
    
    Args:
        dividend: The number to be divided
        divisor: The number to divide by
        operation: The operation to perform ('/')
        
    Returns:
        The result of the calculation
        
    Raises:
        ValueError: If divisor is zero
    """
    if operation == '/':
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        return dividend / divisor
    return 0
```

## 🔐 Security & Privacy

- ✅ **API keys are never stored** - Entered via secure password field
- ✅ **No data persistence** - Code is not saved or logged
- ✅ **User responsibility** - Each user uses their own API key
- ✅ **No code execution** - Only static analysis (safe!)

## 👨‍💻 Author
RAKSHITHA SS
- GitHub: [@RAKSHITHASS7](https://github.com/RAKSHITHASS7)
- LinkedIn: [RAKSHITHA S S](https://linkedin.com/in/RAKSHITHA S S)
- Email: rakshithasnaik16@gmail.com

## 📄 License

This project is licensed under the MIT License.

## 🌟 Show Your Support

If you found this project helpful, please ⭐ star this repository!

---

<p align="center">
  <strong>Made with ❤️ and AI</strong>
  <br>
  <sub>Transform your code with artificial intelligence</sub>
</p>

---

**Last Updated**: January 2024  
**Version**: 2.0  
**Status**: ✅ Active
