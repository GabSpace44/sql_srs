import streamlit as st
import pandas as pd
from pandas import DataFrame
import duckdb


st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

option = st.selectbox(
    "What dog you like to review",
    ["Joins","GroupBy","Windows Functions"],
    index=None,
    placeholder="Select a theme...",
)

st.write('You selected:', option)


st.write('Interpréteur de requête SQL')

data: dict= {"a": [1,2,3],"b":[4,5,6],"c":[7,8,9]}
df: DataFrame = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["SQL", "Dog", "Owl"])

with tab1:
    sql_query: str =str( st.text_area(label="entrez votre input"))
    if sql_query:
        st.write(f"Vous avez entrez : {sql_query}")
        df_duckdb: DataFrame = duckdb.query(sql_query ).df()
        st.dataframe(df_duckdb,width=400)
    else:
        st.write(f"Vous n'avez pas entrez de query sql.")
with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
