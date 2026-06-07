import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import base64

st.set_page_config(
    page_title="LinguaFlow - Language Translation Tool",
    page_icon="🌐",
    layout="centered"
)

_gt = GoogleTranslator(source='en', target='hi')
lang_dict = _gt.get_supported_languages(as_dict=True)
lang_list = sorted(lang_dict.keys())
lang_codes = {v: k for k, v in lang_dict.items()}

st.markdown("""
<style>
    .main-title { text-align: center; font-size: 2.5rem; margin-bottom: 0.3rem; }
    .subtitle { text-align: center; color: #6c757d; margin-bottom: 2rem; }
    .result-box {
        background: #f0f2f6; border-radius: 12px; padding: 1.5rem;
        margin-top: 1rem; border-left: 4px solid #4CAF50;
    }
    .result-box p { margin: 0; font-size: 1.1rem; }
    .footer { text-align: center; color: #adb5bd; font-size: 0.85rem; margin-top: 3rem; }
    .stTextArea textarea { font-size: 1rem; }
    .copy-btn { margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌐 LinguaFlow</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI-Powered Language Translation Companion</p>', unsafe_allow_html=True)



col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("Source Language", lang_list, index=lang_list.index("english"))
with col2:
    tgt_lang = st.selectbox("Target Language", lang_list, index=lang_list.index("hindi"))

input_text = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here..."
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    translate_clicked = st.button("🌍 Translate", type="primary", use_container_width=True)
with col_btn2:
    clear_clicked = st.button("🗑️ Clear", use_container_width=True)
with col_btn3:
    tts_clicked = st.button("🔊 Speak", use_container_width=True)

if clear_clicked:
    st.rerun()

if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            src_code = lang_codes[src_lang]
            tgt_code = lang_codes[tgt_lang]

            with st.spinner("Translating..."):
                result = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(f"**Source ({src_lang}):**\n\n{input_text}")
            st.markdown("---")
            st.markdown(f"**Translation ({tgt_lang}):**")
            st.markdown(f"<p style='font-size:1.3rem; font-weight:500; color:#2e7d32;'>{result}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Translation failed: {str(e)}")

if tts_clicked:
    if not input_text.strip():
        st.warning("Enter some text first, then click Speak.")
    else:
        try:
            tgt_code = lang_codes[tgt_lang]
            tts = gTTS(text=input_text, lang=tgt_code, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()
            b64 = base64.b64encode(audio_bytes).decode()
            md = f'<audio controls autoplay style="width:100%; margin-top:0.5rem;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Text-to-speech failed: {str(e)}")

st.markdown('<p class="footer">Built with ❤️ for CodeAlpha AI Internship • Task 1: Language Translation Tool</p>', unsafe_allow_html=True)
