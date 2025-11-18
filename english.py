import streamlit as st
import pandas as pd
from openai import OpenAI

# Load vocab
@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Translate to English 🦅")
st.write("Enter a Chinese word to get the English translation! This app only recognizes (most of) the vocab we learned so far.")

chinese_word = st.text_input("Enter a word:")

if st.button("Translate"):
    if chinese_word:
        # Exact match only
        if chinese_word in vocab_df['Chinese'].values:
            english_meaning = vocab_df.loc[vocab_df['Chinese'] == chinese_word, 'English'].values[0]
            st.success(f"**English meaning:** {english_meaning}")

            # Generate image using OpenAI
            with st.spinner("Generating image..."):
                prompt = f"A realistic, high-quality image representing '{english_meaning}'"
                image_response = client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt,
                    size="512x512"
                )
                image_url = image_response.data[0].url
                st.image(image_url, caption=f"Image of '{english_meaning}'")
        else:
            st.error("Word not found in vocab!")
    else:
        st.warning("Please enter a Chinese word to translate!")
