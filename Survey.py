import sqlite3
import streamlit as st
import re
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt   

# Set Streamlit page configuration
st.set_page_config(page_title="Survey Form", layout="wide", initial_sidebar_state="auto")
st.title('Happy Survey')
st.subheader('This is a survey from People and Culture')
st.image('https://searchengineland.com/wp-content/seloads/2018/09/happy-people-survey-ss-1920-compressor-800x450.png')
st.markdown('<style>body{background-color: #F8F9FA;}</style>', unsafe_allow_html=True)
# Connect to SQLite database
conn = sqlite3.connect('survey.db')
c = conn.cursor()
# Create an empty list for responses
responses = []
# Store responses in the SQLite database
c.execute("CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY AUTOINCREMENT,first_question TEXT, second_question TEXT, third_question TEXT, fourth_question TEXT, fifth_question TEXT, sixth_question TEXT, seventh_question TEXT, eighth_question TEXT, ninth_question TEXT, tenth_question TEXT, eleventh_question TEXT, twelfth_question TEXT)")
###########################################################################################################################################################
# Define a Streamlit survey form
st.write("Only select one option")
# Input fields for survey questions
st.write("1. Have you ever used our product? ")
first_question = st.multiselect("Select your response", ["Yes", "No"], key="q1")

st.write("2. Would you recommend our product to others? (Yes/No)")
second_question = st.multiselect("Select your response", ["Yes", "No"], key="q2")

st.write("3. Did you find our product easy to use? (Yes/No)")
third_question = st.multiselect("Select your response", ["Yes", "No"], key="q3")

st.write("4. Was our product helpful in solving your problem? (Yes/No)")
fourth_question = st.multiselect("Select your response", ["Yes", "No"], key="q4")

st.write("5. Did our product meet your expectations? (Yes/No)")
fifth_question = st.multiselect("Select your response", ["Yes", "No"], key="q5")

st.write("6. Are you satisfied with our product? (Yes/No)")
sixth_question = st.multiselect("Select your response", ["Yes", "No"], key="q6")

st.write("7. Do you plan to continue using our product? (Yes/No)")
seventh_question = st.multiselect("Select your response", ["Yes", "No"], key="q7")

st.write("8. Did you encounter any issues while using our product? (Yes/No)")
eighth_question = st.multiselect("Select your response", ["Yes", "No"], key="q8")

st.write("9. Did you encounter any issues while using our product? (Yes/No)")
ninth_question = st.multiselect("Select your response", ["Yes", "No"], key="q9")

st.write("10. Do you have any suggestions for improving our product? ")
tenth_question = st.text_input("Write your response", max_chars=500, key="q10")

st.write("11. Please provide any other comments or feedback:")
eleventh_question = st.text_input("Enter your comments", max_chars=500, key="q11")

st.write("12. Please privide a list of adjetives to describe this product:")
twelfth_question = st.text_input("Enter your adjetives", key="q12")

submit = st.button("Submit", key="submit_button_1")

# Store responses in the database upon form submission
if submit:
    # Convert lists to strings
    first_question = ', '.join(first_question)
    second_question = ', '.join(second_question)
    third_question = ', '.join(third_question)
    fourth_question = ', '.join(fourth_question)
    fifth_question = ', '.join(fifth_question)
    sixth_question = ', '.join(sixth_question)
    seventh_question = ', '.join(seventh_question)
    eighth_question = ', '.join(eighth_question)
    ninth_question = ', '.join(ninth_question)
    tenth_question =', '.join(tenth_question)
    eleventh_question =', '.join(eleventh_question)
    twelfth_question =', '.join(twelfth_question)
    
     #Insert responses into the database
    c.execute("INSERT INTO responses (first_question, second_question, third_question, fourth_question, fifth_question, sixth_question, seventh_question, eighth_question, ninth_question, tenth_question, eleventh_question, twelfth_question) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
          (first_question, second_question, third_question, fourth_question, fifth_question, sixth_question, seventh_question, eighth_question, ninth_question, tenth_question, eleventh_question, twelfth_question))
    conn.commit()
    st.success("Responses submitted successfully!")
    st.balloons()



####################################################

