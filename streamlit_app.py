import streamlit as st

st.set_page_config(page_title="Translator", page_icon="📖")

english = st.Page("english.py", title="Translate to English", icon="🦅")
chinese = st.Page("chinese.py", title="Translate to Chinese", icon="🏮")
culture = st.Page("culture.py", title="Culture", icon="🌍")

# Create navigation
pg = st.navigation([english, chinese, culture])

pg.run()
