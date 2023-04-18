import sqlite3
import streamlit as st
import re
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

st.set_page_config(page_title="Survey Results", layout="wide", initial_sidebar_state="auto", page_icon="📊")
st.title('Survey Results')

# Create a connection to the SQLite database
hr_db = sqlite3.connect('accounts.db')
hr_cursor = hr_db.cursor()
conn = sqlite3.connect('survey.db')
c = conn.cursor()

# Create hr_accounts table if not exists
hr_cursor.execute("CREATE TABLE IF NOT EXISTS hr_accounts(username TEXT, password TEXT, email TEXT)")

# HR account creation form
with st.form("create_hr_account_form"):
    st.subheader("Create HR Account")
    hr_username = st.text_input("Enter HR username")
    hr_password = st.text_input("Enter HR password", type="password")
    hr_email = st.text_input("Enter HR email")
    create_hr_account_submit = st.form_submit_button("Submit HR Account")

    if create_hr_account_submit:
        # Check if HR username, password, and email are not empty
        if hr_username and hr_password and hr_email:
            # Validate email format
            if not re.match(r".*@fourseasons\.com$", hr_email):
                st.warning("Please enter a valid email address.")
            else:
                try:
                    # Create HR account in the SQLite database
                    hr_cursor.execute("INSERT INTO hr_accounts (username, password, email) VALUES (?, ?, ?)",(hr_username, hr_password, hr_email))
                    hr_db.commit()
                    st.success("HR account created successfully!")
                except Exception as e:
                    st.error(f"Failed to create HR account: {e}")
        else:
            st.warning("Please enter HR username, password, and email.")

###################################################################################################
# HR login form
with st.form("login_hr_form"):
    st.subheader("HR Login")
    hr_login_username = st.text_input("Enter HR username")
    hr_login_password = st.text_input("Enter HR password", type="password")
    login_hr_submit = st.form_submit_button("Login")

    if login_hr_submit:
        # Check if the fields aren't empty
        if not hr_login_username or not hr_login_password:
            st.error("Please enter both HR username and password")
        # Check if both username and password are not empty
        if hr_login_username and hr_login_password:  
            hr_cursor.execute("SELECT * FROM hr_accounts WHERE username=?", (hr_login_username,))
            hr_account = hr_cursor.fetchone()
            # Check if HR account exists and password is correct
            if hr_account is not None and hr_account[1] == hr_login_password:
                st.success("Logged in successfully!")
                logged_in = True

                # Fetch all rows from the responses table
                c.execute("SELECT * FROM responses")
                rows = c.fetchall()

                # Create a pandas DataFrame from the fetched data
                df = pd.DataFrame(rows, columns=['ID', 'First Question',
                                                 'Second Question',
                                                 'Third Question',
                                                 'Fourth Question',
                                                 'Fifth Question',
                                                 'Sixth Question',
                                                 'Seventh Question',
                                                 'Eighth Question',
                                                 'Ninth Question',
                                                 'Tenth Question',
                                                 'Eleventh Question',
                                                 'Twelfth Question'])

                # Display the DataFrame
                st.write(df)

                # Fetch data from responses table
                c.execute("SELECT first_question, second_question, third_question, fourth_question, fifth_question, sixth_question, seventh_question, eighth_question, ninth_question FROM responses")
                rows = c.fetchall()

                # Convert data to a dataframe
                plot_df = pd.DataFrame(rows, columns=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9"])

                # Count "Yes" and "No" responses for each question
                yes_counts = plot_df.eq('Yes').sum()
                no_counts = plot_df.eq('No').sum()

                # Create a bar chart
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=yes_counts.index,
                    y=yes_counts.values,
                    name='Yes',
                    marker_color='green'
                ))
                fig.add_trace(go.Bar(
                    x=no_counts.index,
                    y=no_counts.values,
                    name='No',
                    marker_color='red'
                ))

                # Set chart title and axis labels
                fig.update_layout(
                    title="Responses for Questions 1 to 9 (Yes/No)",
                    xaxis_title="Question",
                    yaxis_title="Number of Responses"
                )

                # Display chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)
                #####################################################################
                st.subheader("Word Clouds")
               # Fetch data from responses table

                # Fetch data from responses table
                c.execute("SELECT tenth_question, eleventh_question, twelfth_question FROM responses")
                rows = c.fetchall()

                # Convert data to a dataframe
                plot_df = pd.DataFrame(rows, columns=["Tenth Question", "Eleventh Question", "Twelfth Question"])

                # Generate word clouds for each question response
                for column in plot_df.columns:
                    st.subheader(column)
                    response = ' '.join(plot_df[column].tolist())

                    # Tokenize the text data
                    tokens = word_tokenize(response)

                    # Pre-process text data by removing stop words and lemmatizing
                    stop_words = set(stopwords.words("english"))
                    lemmatizer = WordNetLemmatizer()
                    response = ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens if word.lower() not in stop_words])

                    if response:
                        wordcloud = WordCloud(width=1200,
                                              height=800,
                                              max_words=150, 
                                              background_color='white',
                                              collocations=False, 
                                              contour_color='steelblue', 
                                              contour_width=2,
                                              font_path=None, 
                                              random_state=42, max_font_size=200).generate(response)  # Removed font_path parameter
                        plt.figure(figsize=(10, 5))
                        plt.imshow(wordcloud, interpolation="bilinear")
                        plt.axis('off')
                        plt.title(column)
                        st.pyplot(plt)
                        plt.clf()
                    else:
                        st.warning("No responses found for {}".format(column))


# Close SQLite database connection
c.close()

conn.close()
##developed by Diego Torres, question @ diego.torres.developer@gmail.com - or https://www.linkedin.com/in/diego-torres--/