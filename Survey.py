# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Ballon d'Or Fan Survey 🏆")
st.write("Vote for your favorite Ballon d'Or contender!")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.radio(
    "Which player deserves the Ballon d'Or?",
    ["Kylian Mbappe", "Harry Kane", "Michael Olise",
     "Ousmane Dembele", "Erling Haaland", "Lamine Yamal"])
    value_input = st.text_input("Rate this player's performance from 1 to 10:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category_input = category_input.strip()
        value_input = value_input.strip()
        if category_input == "" or value_input == "":
            st.error("Please answer both questions before submitting.")

        elif not value_input.isdigit() or not 1 <= int(value_input) <= 10:
            st.error("Please enter a rating between 1 and 10.")
        else:
            infile = open("data.csv", "a")
            infile.write(category_input + "," + value_input + "\n")
            infile.close()
            st.write("Data saved to:", os.path.abspath("data.csv"))

            st.success("Your vote has been recorded!")
            st.write(f"You voted for **{category_input}** and rated them **{value_input}/10**.")



# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")