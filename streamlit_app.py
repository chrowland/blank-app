import pandas as pd
import streamlit as st

st.set_page_config(layout="centered", page_title="Data Editor", page_icon="🧮")

st.title("✍️ Annotations")
st.caption("This is a demo of the `st.data_editor`.")

st.write("")

"""The new data editor makes it so easy to annotate data! Can you help us annotate sentiments for tweets about our latest release?"""

data = [
    {
        "tweet": "What a great new feature! I love it!",
        "author": "John Rose",
        "sentiment": "🤩 Positive",
        "ranking":1,
    },
    {
        "tweet": "I don't like this feature. It's not useful. I prefer chart improvements.",
        "author": "Will Hangu",
        "sentiment": "",
         "ranking":2,
    },
    {
        "tweet": "Wow, the Streamlit team can be proud! What an achievement!",
        "author": "Luca Masucco",
        "sentiment": "",
         "ranking":3,
    },
    {
        "tweet": "The recent ChatGPT breakthrough is really exciting.",
        "author": "Adrien Tree",
        "sentiment": "",
         "ranking":4,
    },
]

df = pd.DataFrame(data)
df.sentiment = df.sentiment.astype("category")
df.sentiment = df.sentiment.cat.add_categories(("☯ Neutral", "😤 Negative"))


annotated = st.data_editor(df, hide_index=True, use_container_width=True, disabled=["tweet", "author"])

st.download_button(
    "⬇️ Download annotations as .csv", annotated.to_csv(), "annotated.csv", use_container_width=True
)

