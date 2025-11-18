import streamlit as st
import pandas as pd
from rapidfuzz import process
from pypinyin import pinyin, Style
from openai import OpenAI

# Load vocab
@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Translate to Chinese 🏮")

st.write("Enter an English word to get the Chinese translation! This app only recognizes (most of) the vocab we learned so far.")

english_word = st.text_input("Enter a word:")

if st.button("Translate"):
    if english_word:
        english_vocab_list = vocab_df['English'].tolist()
        match, score, index = process.extractOne(english_word, english_vocab_list)

        if score >= 80:
            chinese_meaning = vocab_df.iloc[index]['Chinese']
            pinyin_list = pinyin(chinese_meaning, style=Style.TONE)
            pinyin_text = " ".join([item[0] for item in pinyin_list])

            st.success(f"**Chinese:** {chinese_meaning}\n**Pinyin:** {pinyin_text}")
            
            with st.spinner("Generating image..."):
                prompt = f"A realistic, high-quality image of {english_word} ({chinese_meaning})"
                image_response = client.images.generate(
                    model="gpt-image-1",
                    prompt=prompt,
                    size="512x512"
                )
                image_url = image_response.data[0].url
                st.image(image_url, caption=f"Image of {english_word}; generated with an OpenAI API key")

        else:
            st.error("Word not found!")
    else:
        st.warning("Please enter an English word to translate.")
