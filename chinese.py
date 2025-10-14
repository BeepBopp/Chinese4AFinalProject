import streamlit as st
import pandas as pd

@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

st.title("Translate to Chinese 🏮")

english_word = st.text_input("Enter an English word:")

if chinese_word:
    result = vocab_df[vocab_df['English'] == english_word]
    if not result.empty:
        english_meaning = result.iloc[0]['Chinese']
        st.success(f"Chinese meaning: **{english_meaning}**")
        # will include pinyin later 
        # maybe audio recordings of Chinese word but probably not
    else:
        st.error("Word not found!")
