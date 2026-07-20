# pylint: disable=missing-module-docstring

import io
from typing import cast
import ast
import duckdb
import pandas as pd
import streamlit as st
from pandas import DataFrame
from init_db import  con
from pathlib import Path

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")


with st.sidebar:
    option = st.selectbox(
        "What query do you like to review",
        ["Joins", "GroupBy", "window_functions","cross_joins"],
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme='{option}'").df()
    st.write(exercise)
    if option:
        answer_sql = exercise.loc[0, "answer"]
        with open(f"{Path.cwd()}/answers/{answer_sql}") as file:
            answer_str: str = file.read()
            file.close()
        answer = con.execute(answer_str).df()


st.header("entrez your code:")
SQL_QUERY: str = str(st.text_area(label="votre code SQL ici", key="user_input"))

if SQL_QUERY:

    df_duckdb: DataFrame = con.execute(SQL_QUERY).df()
    if len(answer.columns) != len(df_duckdb.columns):
        st.write("Error, some columns are missing")
    n_lines_difference = df_duckdb.shape[0] - answer.shape[0]
    if n_lines_difference != 0:
        st.write(f"""result has a {n_lines_difference} lines difference between
            your answer and your query""")

    try:
        result = df_duckdb[answer.columns]
        if result.compare(answer).empty:
            pass
        else:
            st.write("Error, the datas are not the same")
            st.dataframe(result.compare(answer))
    except KeyError as e:
        st.write("Error, your query is not what we expected")

    st.dataframe(df_duckdb, width=400)
else:
    st.write("Vous n'avez pas entrez de query sql.")


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    if option:
        try:
            exercise_tables = ast.literal_eval(exercise.loc[0,"tables"])
            for table in exercise_tables:
                st.write(f"Table : {table}")
                st.write(con.execute(f"SELECT * FROM {table}"))
        except ValueError as e:
            st.write(f"""La table {exercise.loc[0,"tables"]} correspondant
                     au theme {exercise.loc[0,"theme"]} est inexistante""")
            print(e)
with tab3:
    if option:
        st.write(answer_str)
        st.write(answer)
