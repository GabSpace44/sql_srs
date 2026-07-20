# pylint: disable=missing-module-docstring

import io
from typing import cast

import duckdb
import pandas as pd
import streamlit as st
from pandas import DataFrame
from init_db import beverages, food_items, solution_df,ANSWER_STR,con


st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")


with st.sidebar:
    option = st.selectbox(
        "What dog you like to review",
        ["Joins", "GroupBy", "Windows Functions","cross_joins"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme='{option}'")
    st.write(exercise)

st.header("entrez your code:")
SQL_QUERY: str = str(st.text_area(label="votre code SQL ici", key="user_input"))

# if SQL_QUERY:
#
#     df_duckdb: DataFrame = duckdb.query(SQL_QUERY).df()
#     if len(solution_df.columns) != len(df_duckdb.columns):
#         st.write("Error, some columns are missing")
#     n_lines_difference = df_duckdb.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(f"""result has a {n_lines_difference} lines difference between
#             your solution_df and your query""")
#
#     try:
#         result = df_duckdb[solution_df.columns]
#         if str(result.compare(solution_df)) != "":
#             st.write("Error, the datas are not the same")
#             st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Error, your query is not what we expected")
#
#     st.dataframe(df_duckdb, width=400)
# else:
#     st.write("Vous n'avez pas entrez de query sql.")
#
#
# tab2, tab3 = st.tabs(["Tables", "Solution"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution_df)
# with tab3:
#     st.write(ANSWER_STR)
