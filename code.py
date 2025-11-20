# --------------------------- app.py ---------------------------
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

# --------------------------- LLM Wrapper ---------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqLLM:
    """LLM wrapper using Groq SDK (ChatCompletionMessage compatible)"""
    def __init__(self, model_name="llama-3.1-8b-instant", temperature=0.2, max_tokens=800):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def run(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        # Access the content correctly
        return resp.choices[0].message.content

# --------------------------- Agents ---------------------------
class CodeAnalyzerAgent:
    """Analyzes code and explains errors"""
    def __init__(self):
        self.llm = GroqLLM()

    def analyze(self, code: str) -> str:
        prompt = f"""
You are a Code Debugging AI.
Analyze the following code, find all errors, and explain them clearly.

Code:
{code}

Explain errors in simple language, step by step.
"""
        return self.llm.run(prompt)

class CodeCorrectorAgent:
    """Suggests corrected code with explanation"""
    def __init__(self):
        self.llm = GroqLLM()

    def correct(self, code: str, analysis: str) -> str:
        prompt = f"""
You are a Code Corrector AI.
Use the following analysis to correct the code and explain the fix.

Original Code:
{code}

Analysis:
{analysis}

Provide:
1. Corrected code
2. Short explanation of the fix
"""
        return self.llm.run(prompt)

# --------------------------- Crew ---------------------------
class CodeDebugCrew:
    def __init__(self):
        self.analyzer = CodeAnalyzerAgent()
        self.corrector = CodeCorrectorAgent()

    def debug_code(self, code: str):
        analysis = self.analyzer.analyze(code)
        corrected = self.corrector.correct(code, analysis)
        return analysis, corrected

crew = CodeDebugCrew()

# --------------------------- Streamlit UI ---------------------------
st.set_page_config(page_title="🛠️ AI Code Debugging Agent", layout="wide", page_icon="🛠️")

# --- Owner Name (Top Right Using Columns) ---
col1, col2 = st.columns([8, 2])
with col2:
    st.markdown("""
        <div style="
            background:#2c3e50;
            color:white;
            padding:7px 12px;
            border-radius:8px;
            text-align:center;
            font-weight:bold;
            font-size:15px;">
            Owner: Vaishnavi Pawar
        </div>
    """, unsafe_allow_html=True)


# --- Header ---
st.markdown("""
<style>
            
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&display=swap');

.header-box {
    background: linear-gradient(135deg, #2c3e50, #2980b9, #8e44ad, #e67e22);
    padding: 30px 25px;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,0,0,0.3), inset 0 0 10px rgba(255,255,255,0.1);
    border: 2px solid rgba(255,255,255,0.2);
                margin-bottom: 30px;  /* adds space below header */
}

/* Remove horizontal bars between sections */
hr {
    display: none; /* hides all <hr>
}

.header-box h1 {
    color: #ffffff;
    font-family: 'Roboto Slab', serif;
    font-weight: 700;
    font-size: 40px;
    text-shadow: 0 0 5px #ffffff, 0 0 10px #2980b9;
    margin: 0;
}

.header-box h4 {
    color: #ecf0f1;
    font-family: 'Roboto Slab', serif;
    font-weight: 400;
    font-size: 20px;
    margin-top: 10px;
    letter-spacing: 1px;
}
</style>

<div style="background: linear-gradient(to right, #1f77b4, #00b894);
            padding: 20px; border-radius: 12px; text-align: center;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.2);">
<h1 style="color: white; font-family: 'Segoe UI', sans-serif;">AI Code Debugging Agent</h1>
<h4 style="color: #f0f0f0; font-family: 'Segoe UI', sans-serif;">Analyze, Fix & Understand Your Code Instantly!</h4>
</div>
""", unsafe_allow_html=True)

# --- Input ---
st.markdown("### 📝 Paste Your Code Below")
code_input = st.text_area("", height=220)

# --- Button Styling ---
st.markdown("""
<style>
.stButton>button {
    background: linear-gradient(90deg, #2980b9, #6dd5fa);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    width: 200px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #6dd5fa, #2980b9);
}
</style>
""", unsafe_allow_html=True)

# --- Generate Button ---
if st.button("🔍 Debug Code"):
    if not code_input.strip():
        st.warning("Please enter your code!")
    else:
        with st.spinner("Analyzing and correcting your code..."):
            analysis, corrected = crew.debug_code(code_input)

        # --- Output Columns ---
        col1, col2 = st.columns(2)

        # First Panel: Code Analysis
        with col1:
            st.markdown('<div style="background-color:#34495e; color:#ffffff; border-radius:20px; padding:20px;">', unsafe_allow_html=True)
            st.markdown("### 🐞 Code Analysis")
            st.success("Errors & Explanation")
            st.info(analysis, icon="ℹ️")
            st.download_button("📥 Download Analysis", analysis, file_name="code_analysis.txt")
            st.markdown('</div>', unsafe_allow_html=True)

        # Second Panel: Corrected Code & Explanation (Light Green)
        with col2:
            st.markdown('<div style="background-color:#a8d5ba; color:#1f3f2b; border-radius:20px; padding:20px;">', unsafe_allow_html=True)
            st.markdown("### ✅ Corrected Code & Explanation")
            st.success("Fixed code in structured format")
            st.code(corrected)
            st.download_button("📥 Download Corrected Code", corrected, file_name="corrected_code.py")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("💡 **Tip:** You can copy the corrected code and use it directly in your project.")
