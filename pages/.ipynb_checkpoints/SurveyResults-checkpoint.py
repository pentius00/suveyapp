import sqlite3
import streamlit as st
import re
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(page_title="Survey Results", layout="wide", initial_sidebar_state="auto", page_icon="📊")
st.title('Survey Results')

# Create a connection to the SQLite database
hr_db = sqlite3.connect('hr_accounts.db')
hr_cursor = hr_db.cursor()
conn = sqlite3.connect('survey.db')
c = conn.cursor()


# Create hr_accounts table if not exists
hr_cursor.execute("CREATE TABLE IF NOT EXISTS hr_accounts(sername TEXT, password TEXT, email TEXT)")


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
                    hr_cursor.execute("INSERT INTO hr_accounts (username, password, email) VALUES (?, ?, ?)",
                              (hr_username, hr_password, hr_email))
                    hr_db.commit()
                    st.success("HR account created successfully!")
                except Exception as e:
                    st.error(f"Failed to create HR account: {e}")
        else:
            st.warning("Please enter HR username, password, and email.")
###################################################################################################
# HR login form
with st.form("login_hr_form"):
    st.subheader("Login as HR")
    hr_username_input = st.text_input("Enter HR username")
    hr_password_input = st.text_input("Enter HR password", type="password")
    login_hr_submit = st.form_submit_button("Login")

    if login_hr_submit:
        if not hr_username_input or not hr_password_input:
            st.error("Please enter both HR username and password")
        elif hr_username_input and hr_password_input:  # Check if both username and password are not empty
            hr_cursor.execute("SELECT * FROM hr_accounts WHERE username = ? AND password = ?",
                              (hr_username_input, hr_password_input))
            hr_account = hr_cursor.fetchone()
        

            if hr_account:
                st.success("Logged in as HR")
                st.title('Survey Results')
                # Fetch all survey responses from the responses table
                c.execute("SELECT * FROM responses")
                survey_responses = c.fetchall()

                # Display survey responses in a table
                # Display the responses in a tabular format
                if responses:
                    st.write('ID | First Question | Second Question | Third Question | Fourth Question | Fifth Question | Sixth Question | Seventh Question | Eighth Question | Ninth Question | Tenth Question | Eleventh Question | Twelfth Question')
                    st.write(':--|:--------------:|:---------------:|:--------------:|:---------------:|:-------------:|:--------------:|:---------------:|:---------------:|:--------------:|:-------------:|:------------------:|:----------------:|')
                    for response in responses:
                        st.write(f"{response[0]} | {response[1]} | {response[2]} | {response[3]} | {response[4]} | {response[5]} | {response[6]} | {response[7]} | {response[8]} | {response[9]} | {response[10]} | {response[11]} | {response[12]}")
                    else:
                        st.write('No responses found.')
                else:
                    st.error("Invalid HR username or password")

            else:
                st.warning("Please enter HR username and password")

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



# Store responses in the database upon form submission

            # Fetch data from responses table
            c.execute("SELECT first_question, second_question, third_question, fourth_question, fifth_question, sixth_question, seventh_question, eighth_question, ninth_question FROM responses")
            rows = c.fetchall()

            # Convert data to a dataframe
            plot_df = pd.DataFrame(rows, columns=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9"])

            # Create a bar chart
            fig = px.bar(plot_df.melt(var_name="Question", value_name="Response"), x="Question", y="Response", color="Response", barmode="group")

            # Set chart title and axis labels
            fig.update_layout(
                title="Responses for Questions 1 to 9",
                xaxis_title="Question",
                yaxis_title="Number of Responses"
            )

            # Display chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            #############################################################################################
            st.subheader("Word Clouds")
            c.execute("SELECT tenth_question, eleventh_question, twelfth_question FROM responses")
            rows = c.fetchall()

            # Convert data to a dataframe
            plot_df = pd.DataFrame(rows, columns=["Tenth Question", "Eleventh Question", "Twelfth Question"])

            # Generate word clouds for each question response
            for column in plot_df.columns:
                st.subheader(column)
                response = ' '.join(plot_df[column].tolist())
                if response:
                    wordcloud = WordCloud(width=200, height=100,
            max_words=150, background_color='white').generate(response)
                    plt.figure(figsize=(5, 3))
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis('off')
                    plt.title(column)
                    plt.show()
                    st.pyplot(plt)
                    plt.clf()
                else:
                    st.warning("No responses found for {}".format(column))

            # Close SQLite database connection
            conn.close()
          
# Close SQLite database connection
hr_db.close()

conn.close()
        