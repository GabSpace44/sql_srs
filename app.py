# pylint: disable=missing-module-docstring

# ------------------------------------------------------------
# IMPORT GLOBAL PACKAGE
# ------------------------------------------------------------
import streamlit as st
from pandas import DataFrame
from pathlib import Path

# ------------------------------------------------------------
# INIT DB
# ------------------------------------------------------------

if Path(f"{Path.cwd()}/data/").is_dir():
    pass
else:
    with open(f"{Path.cwd()}/init_db.py") as file:
        Path(f"{Path.cwd()}/data/").mkdir()
        exec(file.read())
        file.close()

# ------------------------------------------------------------
# IMPORT WORKFLOW PACKAGE
# ------------------------------------------------------------

from init_db import con, list_theme

# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")


with st.sidebar:
    option = st.selectbox(
        "What query do you like to review",
        list_theme,
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", option)

    exercise = con.execute(f"""SELECT *
                        FROM memory_state WHERE theme='{option}'
                        ORDER BY last_reviewed
                    """).df()
    st.write(exercise.loc[0:, ["theme", "exercise_name", "last_reviewed"]])
    if option:
        answer_sql = exercise.loc[0, "answer"]
        with open(f"{Path.cwd()}/answers/{answer_sql}") as file:
            answer_str: str = file.read()
            file.close()
        answer = con.execute(answer_str).df()
        EXERCISE_NAME = exercise["exercise_name"][0]

    if st.button("Reset"):
        con.execute(f"""
            UPDATE memory_state 
            set last_reviewed='1970-01-01'
            WHERE theme='{option}'
        """)
        st.session_state.user_input = ""
        st.rerun()


st.header("enter your code:")
SQL_QUERY: str = str(st.text_area(label="votre code SQL ici", key="user_input"))



def check_users_solution(user_query: str) -> None:
    """
    Check that the user SQL query is correct by
    :param user_query:
    :return:
    """
    global e
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
            st.write("Good job, this is correct !")
            st.balloons()
        else:
            st.write("Error, the datas are not the same")
            st.dataframe(result.compare(answer))
    except KeyError as e:
        st.write("Error, your query is not what we expected")

    st.dataframe(df_duckdb, width=400)


if SQL_QUERY:
    check_users_solution(SQL_QUERY)
else:
    st.write("Vous n'avez pas entrez de query sql.")

button_list :list[int|str]=[2,7,21]

cols: list[st.delta_generator.DeltaGenerator]= st.columns(len(button_list))
for col, n_day in zip(cols, button_list):
    with col:
        if  st.button(f"review in {n_day} days"):
            con.execute(
                f"""UPDATE memory_state
                SET last_reviewed=strftime(date_add(current_date,{n_day}),'%Y-%m-%d') 
                WHERE exercise_name='{EXERCISE_NAME}'
            """)
            st.rerun()




tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    if option:
        try:
            exercise_tables = exercise.loc[0, "tables"]
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


