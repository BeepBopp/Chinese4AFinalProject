import streamlit as st
import pandas as pd
from rapidfuzz import process
from pypinyin import pinyin, Style

@st.cache_data
def load_vocab(file_path):
    return pd.read_csv(file_path)

vocab_df = load_vocab("vocab.csv")

st.title("Translate to Chinese 🏮")

st.write("Enter an English word to get the Chinese translation with Pinyin!")

english_word = st.text_input("Enter a word:")

if st.button("Translate"):
    if english_word:
        english_vocab_list = vocab_df['English'].tolist()

        match, score, index = process.extractOne(english_word, english_vocab_list)

        if score >= 80:
            chinese_meaning = vocab_df.iloc[index]['Chinese']

            pinyin_list = pinyin(chinese_meaning, style=Style.TONE3)
            pinyin_text = " ".join([item[0] for item in pinyin_list])

            if match == english_word:
                st.success(f"**Chinese:** {chinese_meaning}\n**Pinyin:** {pinyin_text}")
            else:
                st.success(f"Did you mean: **{match}**?\n\n**Chinese:** {chinese_meaning}\n**Pinyin:** {pinyin_text}")
        else:
            st.error("Word not found!")
    else:
        st.warning("Please enter an English word to translate.")
