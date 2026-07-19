# pylint: disable=missing-module-docstring

import io
from typing import cast

import duckdb
import pandas as pd
import streamlit as st
from pandas import DataFrame

CSV: str = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
CSV2: str = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
beverages: DataFrame = cast(DataFrame, pd.read_csv(io.StringIO(CSV))) # Test : CI ddnakjndkajzndjkazndjkqnksjdnqndjazndjz
food_items: DataFrame = cast(DataFrame, pd.read_csv(io.StringIO(CSV2)))

ANSWER_STR: str = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
solution_df = duckdb.sql(ANSWER_STR).df()

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

st.header("entrez your code:")
SQL_QUERY: str = str(st.text_area(label="votre code SQL ici", key="user_input"))


with st.sidebar:
    option = st.selectbox(
        "What dog you like to review",
        ["Joins", "GroupBy", "Windows Functions"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)


if SQL_QUERY:

    df_duckdb: DataFrame = duckdb.query(SQL_QUERY).df()
    if len(solution_df.columns) != len(df_duckdb.columns):
        st.write("Error, some columns are missing")
    n_lines_difference = df_duckdb.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"""result has a {n_lines_difference} lines difference between
            your solution_df and your query"""
        )

    try:
        result = df_duckdb[solution_df.columns]
        if str(result.compare(solution_df)) != "":
            st.write("Error, the datas are not the same")
            st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Error, your query is not what we expected")

    st.dataframe(df_duckdb, width=400)
else:
    st.write("Vous n'avez pas entrez de query sql.")


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)
with tab3:
    st.write(ANSWER_STR)
