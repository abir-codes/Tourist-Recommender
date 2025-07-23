from dotenv import load_dotenv
import os
import mysql.connector
import streamlit as st

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

connection = mysql.connector.connect(
 host = db_host,
 user = db_user,
 password =db_password,
 database = db_name
 )

mycursor = connection.cursor()


st.title("Tourist Recommender")

def select_column(column):
    column = f"SELECT DISTINCT {column} FROM spots"
    mycursor.execute(column)
    results = mycursor.fetchall()
    return [item[0] for item in results]
    

Categories = select_column("category")
Budget = select_column("budget")
Season = select_column("season")

Category = st.selectbox("Select Category",Categories)
Budget = st.selectbox("Select Category",Budget)
Season = st.selectbox("Select Category",Season)

if st.button("Search"):
    query = """
             SELECT * FROM spots WHERE category = %s AND budget = %s AND season = %s 

           """
    mycursor.execute(query,(Category,Budget,Season))
    results = mycursor.fetchall()

    if results :
      st.success(f"Found {len(results)} result(s) : ")
      for row in results:
        st.markdown(f" **{row[1]} : {row[2]}** ")
    else:
      st.warning("No results found ")


mycursor.close()
connection.close()

