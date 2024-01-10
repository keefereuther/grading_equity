# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import ttest_ind
from scipy.stats import median_abs_deviation

# Load the gradebook data
gradebook = pd.read_csv('FAKE_EXAMPLE_DATA.csv')

# Define the assignment groups
assignment_groups = {
    "attendance": [column for column in gradebook.columns if 'Attendance' in column],  
    "study_activities": [column for column in gradebook.columns if 'Study' in column],  
    "quizzes": [column for column in gradebook.columns if 'Quiz' in column],  
    "midterms": [column for column in gradebook.columns if 'Midterm' in column],  
    "final_exam": [column for column in gradebook.columns if 'Final_Exam' in column]
}

# Add a title to the app
st.title("Minimizing Inequity in Grading")

# Create sidebar for weightings
weightings = {group: st.sidebar.slider(f'{group} weighting', min_value=0.000, max_value=1.000, value=0.2, step=0.01) for group in assignment_groups.keys()}

# Create sidebar for dropped scores
dropped_scores = {group: st.sidebar.slider(f'{group} dropped scores', min_value=0, max_value=6, value=0) for group in assignment_groups.keys()}

# Create sidebar for minimum scores
minimum_scores = {group: st.sidebar.slider(f'{group} minimum score', min_value=0.0, max_value=1.0, value=0.0, step=0.01) for group in assignment_groups.keys()}

# Define the function for calculating final grades
def calculate_final_grade(gradebook, assignment_groups, weightings, dropped_scores, minimum_scores):
    
    # Initialize a DataFrame to store the final grades
    final_grades = pd.DataFrame()
    final_grades["ID"] = gradebook["ID"]
    final_grades["minoritized"] = gradebook["Minoritized"]

    # Initialize a Series to store the total weights (for normalization)
    total_weights = pd.Series(0, index=gradebook.index)

    # Loop over each assignment group
    for group, columns in assignment_groups.items():
        # Calculate the total score for the group, replacing missing or below-minimum scores with the minimum
        group_scores = gradebook[columns].apply(pd.to_numeric, errors='coerce')
        group_scores = group_scores.fillna(minimum_scores[group]).clip(lower=minimum_scores[group])

        # Drop the lowest scores
        if dropped_scores[group] > 0:
            group_scores = group_scores.apply(lambda row: row.nlargest(len(row) - dropped_scores[group]), axis=1)

        # Calculate the average score for the group
        group_averages = group_scores.mean(axis=1)

        # Multiply by the weight and add to the final grades
        final_grades[group] = group_averages * weightings[group]
        total_weights += weightings[group]

    # Normalize the final grades by the total weights
    final_grades["Final_Grade"] = final_grades.drop(columns=["ID", "minoritized"]).sum(axis=1) / total_weights

    return final_grades

# Calculate final grades
final_grades = calculate_final_grade(gradebook, assignment_groups, weightings, dropped_scores, minimum_scores)

# Display the final grades
# st.write(final_grades.head())

# Calculate summary statistics for each group
summary_statistics = final_grades.groupby("minoritized")["Final_Grade"].describe()

# Calculate the median for each group
minority_median = final_grades[final_grades["minoritized"] == True]["Final_Grade"].median()
non_minority_median = final_grades[final_grades["minoritized"] == False]["Final_Grade"].median()

# Calculate the difference between the medians
median_difference = minority_median - non_minority_median

# Convert to percentage and round to 2 decimal places
minority_median = round(minority_median * 100, 2)
non_minority_median = round(non_minority_median * 100, 2)
median_difference = round(median_difference * 100, 2)

# Display the medians
st.markdown(f"<p style='font-size:28px;'>This data is FAKE and only for the purpose of demonstrating the app.</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px;'>Racially Minoritized and/or First-Gen Students' Median: {minority_median}%</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px;'>Non-minoritized and not First-Gen Students' Median: {non_minority_median}%</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px;'>Median Difference: {median_difference}%</p>", unsafe_allow_html=True)

# Plot histograms of final grades for each group
plt.hist(final_grades.loc[final_grades["minoritized"] == False, "Final_Grade"], bins=50, histtype='step', label='Non-minoritized and not First-Gen Students', color='blue')
plt.hist(final_grades.loc[final_grades["minoritized"] == True, "Final_Grade"], bins=50, histtype='step', label='Racially Minoritized and/or First-Gen Students', color='orange')

# Add labels and legend
plt.xlabel('Final Grade')
plt.ylabel('Frequency')
plt.legend(loc='upper left')

# Display the plot
st.pyplot(plt)


# Calculate MAD for each group
minority_mad = median_abs_deviation(final_grades.loc[final_grades["minoritized"] == True, "Final_Grade"])
non_minority_mad = median_abs_deviation(final_grades.loc[final_grades["minoritized"] == False, "Final_Grade"])

st.write('Racially Minoritized MAD: ', minority_mad)
st.write('Racially Non-Minoritized MAD: ', non_minority_mad)

# Display the summary statistics
st.write(summary_statistics)

# Conduct t-test
t_stat, p_value = ttest_ind(final_grades[final_grades["minoritized"] == True]["Final_Grade"], 
                            final_grades[final_grades["minoritized"] == False]["Final_Grade"], 
                            equal_var=False, nan_policy='omit')
st.write(f"P-value (t-test): {p_value}")

# Calculate Glass's Delta
non_minority_std = final_grades.loc[final_grades["minoritized"] == False, "Final_Grade"].std()
glass_delta = (final_grades.loc[final_grades["minoritized"] == True, "Final_Grade"].mean() - final_grades.loc[final_grades["minoritized"] == False, "Final_Grade"].mean()) / non_minority_std
st.write('Glass Delta: ', glass_delta)
