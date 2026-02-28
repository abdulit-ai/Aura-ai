import streamlit as st
import google.generativeai as genai
import requests
import urllib.parse

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Aura AI | Studio", page_icon="🌌", layout="wide")

# --- CUSTOM CSS (UI/UX SPECIFICATIONS) ---
st.markdown("""
    <style>
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Theme Setup */
    .stApp {
        background-color: #F8FAF8;
    }
    
    /* Sticky Navbar & Spinning Logo */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 15px 30px;
        z-index: 9999;
        display: flex;
        align-items: center;
        border-bottom: 1px solid rgba(79, 70, 229, 0.2);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .spinning-spiral {
        width: 30px;
        height: 30px;
        border: 4px solid #4F46E5;
        border-top: 4px solid transparent;
        border-radius: 50%;
        animation: spin 1.5s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .brand-name {
        color: #4F46E5;
        font-size: 24px;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
        margin: 0;
    }

    /* Padding for main content to clear sticky navbar */
    .main .block-container {
        padding-top: 100px;
    }

    /* Glassmorphism Cards for Buttons */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(79, 70, 229, 0.1);
        backdrop-filter: blur(8px);
        border-radius: 15px;
        color: #333;
        font-weight: 600;
        height: 120px;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: #4F46E5;
        color: white;
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(79, 70, 229, 0.3);
        border: 1px solid #4F46E5;
    }
    </style>
    
    <div class="navbar">
        <div class="logo-container">
            <div class="spinning-spiral"></div>
            <h1 class="brand-name">Aura AI</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SESSION STATE (SPA ROUTING) ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

def navigate(page):
    st.session_state.current_page = page

# --- HELPER FUNCTIONS ---
def generate_ai_response(prompt, model_type, system_instruction):
    api_key = st.session_state.get('api_key', '')
    if not api_key:
        return "Error: Please enter your Google API Key in the sidebar."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=model_type,
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if '429' in str(e):
            return "⚠️ **System Busy:** We are currently experiencing high traffic. Please wait a moment and try again."
        return f"Error: {str(e)}"

def generate_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    return url

# --- SIDEBAR (SECURITY) ---
with st.sidebar:
    st.markdown("### 🔐 Security & Settings")
    api_key = st.text_input("Google API Key", type="password", placeholder="Enter Gemini API Key")
    if api_key:
        st.session_state.api_key = api_key
    
    st.divider()
    if st.button("🏠 Return to Dashboard", use_container_width=True):
        navigate('Dashboard')
        st.rerun()

# --- APP ROUTING & LOGIC ---
if st.session_state.current_page == 'Dashboard':
    st.markdown("## Welcome to your Studio")
    st.markdown("Select a tool below to begin your workflow.")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🕵️ AI Detector"): navigate('AI Detector'); st.rerun()
        if st.button("💬 AI Chat"): navigate('AI Chat'); st.rerun()
    with col2:
        if st.button("🧠 Humanizer"): navigate('Humanizer'); st.rerun()
        if st.button("🎨 Image Gen"): navigate('Image Gen'); st.rerun()
    with col3:
        if st.button("🔍 Plagiarism"): navigate('Plagiarism'); st.rerun()
        if st.button("🌍 Translator"): navigate('Translator'); st.rerun()
    with col4:
        if st.button("🔄 Paraphraser"): navigate('Paraphraser'); st.rerun()
        if st.button("✂️ Summarizer"): navigate('Summarizer'); st.rerun()
    with col5:
        if st.button("✅ Grammar"): navigate('Grammar'); st.rerun()
        if st.button("📚 Citations"): navigate('Citations'); st.rerun()

else:
    # --- INDIVIDUAL TOOL WORKSPACES ---
    tool = st.session_state.current_page
    st.markdown(f"## {tool}")
    
    user_input = st.text_area("Enter your text/prompt here:", height=200)
    
    if st.button(f"Run {tool}", type="primary"):
        if not user_input:
            st.warning("Please provide input text.")
        else:
            with st.spinner("Processing..."):
                # Tool Logic Configuration
                if tool == 'Humanizer':
                    result = generate_ai_response(user_input, "gemini-1.5-pro", "You are an expert copywriter. Rewrite the provided text to maximize burstiness and perplexity, making it completely indistinguishable from high-level human writing. Remove robotic transitions.")
                elif tool == 'AI Detector':
                    result = generate_ai_response(user_input, "gemini-1.5-pro", "You are a highly advanced AI detection system. Analyze the text and provide a probability percentage of it being AI-generated, followed by a breakdown of the specific syntactic markers that led to your conclusion.")
                elif tool == 'AI Chat':
                    result = generate_ai_response(user_input, "gemini-1.5-pro", "You are Aura AI, a professional, high-end SaaS assistant. Be concise, brilliant, and helpful.")
                elif tool == 'Summarizer':
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "You are a professional editor. Summarize the text concisely, extracting only the most critical bullet points and a brief overview.")
                elif tool == 'Grammar':
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "You are a strict proofreader. Fix all grammatical, spelling, and punctuation errors in the text. Output the corrected text only.")
                elif tool == 'Translator':
                    # Simplified for demo: auto-detects and translates to English if foreign, or asks for target.
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "You are a master linguist. If the text is not English, translate it to English. If it is English, translate it to Spanish, French, and Japanese in a clean format.")
                elif tool == 'Citations':
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "Generate perfect APA, MLA, and Chicago style citations based on the provided text, link, or source details.")
                elif tool == 'Plagiarism':
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "You are a plagiarism detection tool. While you cannot search the live web, analyze the text for highly common cliches, heavily reused academic phrasing, and provide a mock originality score based on statistical likelihood.")
                elif tool == 'Paraphraser':
                    result = generate_ai_response(user_input, "gemini-1.5-flash", "You are a master wordsmith. Paraphrase the text to improve flow and clarity while retaining the exact original meaning.")
                elif tool == 'Image Gen':
                    image_url = generate_image(user_input)
                    st.image(image_url, caption="Generated by Aura AI (Pollinations Engine)", use_column_width=True)
                    result = "Image generated successfully."
                
                if tool != 'Image Gen':
                    st.markdown("### Result")
                    st.info(result)
