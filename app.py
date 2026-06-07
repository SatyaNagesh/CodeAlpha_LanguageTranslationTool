import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

st.set_page_config(
    page_title="LinguaFlow - Language Translation Tool",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Translator
_gt = GoogleTranslator(source='en', target='hi')
lang_dict = _gt.get_supported_languages(as_dict=True)
lang_list = sorted(lang_dict.keys())

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0, 13, 255, 0.2);
    }
    .main-title { font-size: 3rem; font-weight: 600; margin: 0; }
    .subtitle { font-size: 1.2rem; font-weight: 300; margin: 0; opacity: 0.9; }
    
    /* Glassmorphism Result Box */
    .result-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    /* Dark mode text adaptation */
    @media (prefers-color-scheme: light) {
        .result-box {
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(0, 0, 0, 0.1);
            color: #333;
        }
    }
    
    .translation-text { font-size: 1.5rem; font-weight: 600; color: #4CAF50; margin-top: 1rem; }
    .history-box {
        background: rgba(0, 0, 0, 0.03);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    
    div[data-testid="stButton"] button {
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <p class="main-title">🌐 LinguaFlow</p>
    <p class="subtitle">AI-Powered Premium Translation Companion</p>
</div>
""", unsafe_allow_html=True)

# --- State Management ---
if 'history' not in st.session_state:
    st.session_state.history = []

if 'swap_trigger' not in st.session_state:
    st.session_state.swap_trigger = False

# Manage swap logic manually using session state keys
if 'src_lang_idx' not in st.session_state:
    st.session_state.src_lang_idx = lang_list.index("english")
if 'tgt_lang_idx' not in st.session_state:
    st.session_state.tgt_lang_idx = lang_list.index("hindi")

def swap_langs():
    st.session_state.src_lang_idx, st.session_state.tgt_lang_idx = st.session_state.tgt_lang_idx, st.session_state.src_lang_idx

# --- Layout ---
col1, col_swap, col2 = st.columns([10, 2, 10], vertical_alignment="bottom")

with col1:
    src_lang = st.selectbox("Source Language", lang_list, index=st.session_state.src_lang_idx)
    st.session_state.src_lang_idx = lang_list.index(src_lang)

with col_swap:
    st.button("⇄", on_click=swap_langs, help="Swap Languages", use_container_width=True)

with col2:
    tgt_lang = st.selectbox("Target Language", lang_list, index=st.session_state.tgt_lang_idx)
    st.session_state.tgt_lang_idx = lang_list.index(tgt_lang)

input_text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here to experience the flow..."
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    translate_clicked = st.button("✨ Translate", type="primary", use_container_width=True)
with col_btn2:
    tts_clicked = st.button("🔊 Pronounce", use_container_width=True)
with col_btn3:
    clear_clicked = st.button("🗑️ Clear History", use_container_width=True)

if clear_clicked:
    st.session_state.history = []
    st.rerun()

# --- Logic ---
if translate_clicked or tts_clicked:
    if not input_text.strip():
        st.warning("Please enter some text first.")
    else:
        # Fetch correct language codes (Fix for the KeyError bug)
        src_code = lang_dict[src_lang]
        tgt_code = lang_dict[tgt_lang]

        if translate_clicked:
            try:
                with st.spinner("Translating..."):
                    result = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)
                
                # Save to history
                st.session_state.history.insert(0, {"src": input_text, "tgt": result, "langs": f"{src_lang} ➝ {tgt_lang}"})
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"**{src_lang.capitalize()}**<br>{input_text}", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown(f"**{tgt_lang.capitalize()}**")
                st.markdown(f"<div class='translation-text'>{result}</div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Translation failed: {str(e)}")

        elif tts_clicked:
            try:
                with st.spinner("Generating audio..."):
                    tts = gTTS(text=input_text, lang=src_code, slow=False)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    audio_bytes = fp.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    md = f'<audio controls autoplay style="width:100%; border-radius:10px; margin-top:1rem;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
                    st.markdown(md, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio generation failed. (Note: Not all languages support TTS). Error: {str(e)}")

# --- History Section ---
if st.session_state.history:
    st.markdown("<br><br><h3>📜 Recent Translations</h3>", unsafe_allow_html=True)
    for item in st.session_state.history[:5]: # Show top 5
        st.markdown(f"""
        <div class="history-box">
            <b>{item['langs']}</b><br>
            <i>{item['src']}</i> <br>
            <span style='color:#4CAF50'>{item['tgt']}</span>
        </div>
        """, unsafe_allow_html=True)
