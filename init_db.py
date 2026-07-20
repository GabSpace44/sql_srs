# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
from pandas import DataFrame
from typing import cast
from pathlib import Path

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)


# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------


data: dict = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "size_and_trademark"],
    "tables": [["beverages", "food_items"], ["size", "trademark"]],
    "last_reviewed": ["2026-07-20", "2026-07-19"],
    "answer": ["beverages_and_food.sql", "size_and_trademark.sql"],
}
list_theme: list = list(set(data["theme"]))

memory_state_df = pd.DataFrame(data)
con.execute("""
            DROP TABLE IF EXISTS memory_state;
            CREATE TABLE memory_state AS
                SELECT * FROM memory_state_df;
            """)


# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------


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

beverages: DataFrame = cast(DataFrame, pd.read_csv(io.StringIO(CSV)))

food_items: DataFrame = cast(DataFrame, pd.read_csv(io.StringIO(CSV2)))

con.execute(f"""
            DROP TABLE IF EXISTS beverages;
            CREATE TABLE beverages AS 
            SELECT * FROM beverages;
            DROP TABLE IF EXISTS food_items;
            CREATE TABLE food_items AS 
            SELECT * FROM food_items;                
            """)


size = """
size
XS
M
L
XL
"""

trademark = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""

size: DataFrame = pd.read_csv(io.StringIO(size))
trademark: DataFrame = pd.read_csv(io.StringIO(trademark))


con.execute(f"""
            DROP TABLE IF EXISTS size;
            CREATE TABLE size AS 
            SELECT * FROM size;
            DROP TABLE IF EXISTS trademark;
            CREATE TABLE trademark AS 
            SELECT * FROM trademark;                
            """)
