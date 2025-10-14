import streamlit as st
import pandas as pd
from rapidfuzz import process

@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

st.title("Translate to English 🦅")

st.write("Enter a Chinese word to get the English translation! This app only recognizes (most of) the vocab we learned so far.")

chinese_word = st.text_input("Enter a word:")

if st.button("Translate"):
    if chinese_word:
        chinese_vocab_list = vocab_df['Chinese'].tolist()

        match, score, index = process.extractOne(chinese_word, chinese_vocab_list)

        if score >= 80:  
            english_meaning = vocab_df.iloc[index]['English']
            if match == chinese_word:
                st.success(f"**English meaning:** {english_meaning}")
            else:
                st.success(f"Did you mean: **{match}**?\n\n**English meaning:** {english_meaning}")
        else:
            st.error("Word not found!")
    else:
        st.warning("Please enter a word if you like to translate!")

