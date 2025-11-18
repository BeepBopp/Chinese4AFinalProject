import streamlit as st
import pandas as pd
import unicodedata
from difflib import get_close_matches
from openai import OpenAI

@st.cache_data
def load_vocab(file_path):
    df = pd.read_csv(file_path, encoding="utf-8-sig", dtype=str)
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).fillna("").apply(lambda x: unicodedata.normalize("NFKC", x).strip())
    return df

def norm(x):
    if x is None:
        return ""
    return unicodedata.normalize("NFKC", str(x)).strip()

vocab_df = load_vocab("vocab.csv")
if "Chinese" not in vocab_df.columns or "English" not in vocab_df.columns:
    st.error("CSV must have columns named 'Chinese' and 'English'.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Translate to English 🦅")
st.write("Enter a Chinese word to get the English translation! This app only recognizes (most of) the vocab we learned so far.")

chinese_word = st.text_input("Enter a word:")

if st.button("Translate"):
    w = norm(chinese_word)
    if w:
        vocab_df["Chinese_norm"] = vocab_df["Chinese"].apply(norm)
        mask = vocab_df["Chinese_norm"] == w
        if mask.any():
            english_meaning = vocab_df.loc[mask, "English"].iloc[0]
            st.success(f"**English meaning:** {english_meaning}")
            with st.spinner("Generating image..."):
                prompt = f"A realistic, high-quality image representing '{english_meaning}'"
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024"
                )
                try:
                    b64 = image_response.data[0].b64_json
                    import base64
                    import io
                    from PIL import Image
                    img_bytes = base64.b64decode(b64)
                    img = Image.open(io.BytesIO(img_bytes))
                    st.image(img, caption=f"Image of '{english_meaning}'")
                except Exception:
                    try:
                        url = image_response.data[0].url
                        st.image(url, caption=f"Image of '{english_meaning}'")
                    except Exception as e:
                        st.warning(f"Image generation succeeded but display failed: {e}")
        else:
            candidates = vocab_df["Chinese_norm"].dropna().unique().tolist()
            sugg = get_close_matches(w, candidates, n=5, cutoff=0.6)
            if sugg:
                st.error("Word not found! Did you mean:")
                for s in sugg:
                    st.write(f"- {s}")
            else:
                st.error("Word not found!")
    else:
        st.warning("Please enter a Chinese word to translate!")
