# Grading Equity Analysis App

## Overview
This Streamlit app analyzes grading data to assess equity in educational outcomes. It focuses on minimizing grading inequities, especially among minoritized and first-generation students.

## How It Works
- The app loads a gradebook from a CSV file (`FAKE_EXAMPLE_DATA.csv`).
- It categorizes assignments into groups like attendance, study activities, quizzes, midterms, and final exams.
- Users can adjust weightings, drop scores, and set minimum scores for each group via sliders in the Streamlit sidebar.
- The app calculates final grades, median grades, grade distributions, and statistical measures like median absolute deviation and Glass's Delta.

## Setting Up Your Own Analysis
1. Fork the repository to create a private copy.
2. Replace `FAKE_EXAMPLE_DATA.csv` with your own CSV file. Ensure it follows a similar structure.
3. Modify the `assignment_groups` dictionary in `gradesimapp.py` to match your gradebook columns.
4. Deploy your app on Streamlit Cloud or another platform.

## Running the App Locally

1. Ensure Python is installed on your machine.
2. Clone your forked repository or download the source code.
3. Navigate to the app's directory in your terminal.
4. Install the required packages using `pip install -r requirements.txt`.
5. Run the app with `streamlit run b3simapp.py`.
6. The app should now be running locally and can be accessed via a web browser at the address provided by Streamlit (usually `localhost:8501`).

Remember to respect student privacy and confidentiality when handling real grade data.
