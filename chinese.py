import streamlit as st
import pandas as pd
from rapidfuzz import process

@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

st.title("Translate to Chinese 🏮")

st.write("Enter a English word to get the Chinese translation! This app only recognizes (most of) the vocab we learned so far.")

english_word = st.text_input("Enter a word:")

if st.button("Translate"):
    if english_word:
        english_vocab_list = vocab_df['English'].tolist()

        match, score, index = process.extractOne(english_word, english_vocab_list)

        if score >= 80:  
            chinese_meaning = vocab_df.iloc[index]['Chinese']
            if match == english_word:
                pinyin = vocab_df.iloc[index]['Pinyin']
                st.success(f"**Chinese meaning:** {chinese_meaning}", \n, f"**Pinyin:** {pinyin})
                
            else:
                st.success(f"Did you mean: **{match}**?\n\n**Chinese meaning:** {chinese_meaning}")
        else:
            st.error("Word not found!")
    else:
        st.warning("Please enter an English word to translate.")

