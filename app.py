import streamlit as st
import pandas as pd
from pandas import DataFrame
import duckdb
import io
from typing import cast


csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''
csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
beverages: DataFrame = cast(DataFrame,pd.read_csv(io.StringIO(csv)))
food_items: DataFrame = cast(DataFrame,pd.read_csv(io.StringIO(csv2)))

answer = '''
SELECT * FROM beverages
CROSS JOIN food_items
'''
solution = duckdb.sql(answer).df()

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

st.header("entrez your code:")
sql_query = st.text_area(label="votre code SQL ici", key="user_input")



with st.sidebar:
    option = st.selectbox(
        "What dog you like to review",
        ["Joins","GroupBy","Windows Functions"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write('You selected:', option)



if sql_query:
    st.write(f"Vous avez entrez : {sql_query}")
    df_duckdb: DataFrame = duckdb.query(sql_query ).df()
    st.dataframe(df_duckdb,width=400)
else:
    st.write(f"Vous n'avez pas entrez de query sql.")



tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution)
with tab3:
    st.write(answer)



