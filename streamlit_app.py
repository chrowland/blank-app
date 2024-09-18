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
        "sentiment": 5,
    },
    {
        "tweet": "I don't like this feature. It's not useful. I prefer chart improvements.",
        "author": "Will Hangu",
        "sentiment": "",
    },
    {
        "tweet": "Wow, the Streamlit team can be proud! What an achievement!",
        "author": "Luca Masucco",
        "sentiment": "",
    },
    {
        "tweet": "The recent ChatGPT breakthrough is really exciting.",
        "author": "Adrien Tree",
        "sentiment": "",
    },
]

df = pd.DataFrame(data)


annotated = st.data_editor(df, hide_index=True, use_container_width=True)

st.download_button(
    "⬇️ Download annotations as .csv", annotated.to_csv(), "annotated.csv", use_container_width=True
)

data2=pd.DataFrame()
data2['sentiments']=sum(annotated.sentiment)
data2['sent_squared']=data2.sentiments**2
df2=pd.DataFrame(data2)

second_table=st.dataframe(df2,hide_index=True,use_container_width=True)
