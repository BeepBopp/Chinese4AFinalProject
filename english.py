import streamlit as st
import pandas as pd

@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

st.title("Translate to English 🦅")

chinese_word = st.text_input("Enter a Chinese word:")

if chinese_word:
    result = vocab_df[vocab_df['Chinese'] == chinese_word]
    if not result.empty:
        english_meaning = result.iloc[0]['English']
        st.success(f"English meaning: **{english_meaning}**")
    else:
        st.error("Word not found!")
