import numpy as np
import pandas as pd
import scipy.stats as stats


def perform_mann_whitney_u_test(group_data1, group_data2):
    # Perform the Mann-Whitney U test
    statistic, p_value = stats.mannwhitneyu(
            group_data1, group_data2, alternative="two-sided"
            )

    # Calculate the effect size (r)
    n1, n2 = len(group1), len(group2)
    z = abs(statistic - (n1 * n2 / 2)) / ((n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5)
    print(z)
    effect_size = z / ((n1 + n2) ** 0.5)

    return statistic, p_value, effect_size


# Read data from CSV files
file1 = "rag.csv"
file2 = "searchengine.csv"
# Read the CSV files
df1 = pd.read_csv(file1, sep=",", header=None)
df2 = pd.read_csv(file2, sep=",", header=None)

# Extract the data for the two groups
group1 = df1.iloc[:, 1].values
group2 = df2.iloc[:, 1].values

# Perform comparisons
higher = np.sum(group1 > group2)
lower = np.sum(group1 < group2)
equal = np.sum(group1 == group2)

# Output results
print(f"Number of elements in {file1} that are higher than in {file2}: {higher}")
print(f"Number of elements in {file1} that are lower than in {file2}: {lower}")
print(f"Number of elements in {file1} that are equal to {file2}: {equal}")

statistic, p_value, effect_size = perform_mann_whitney_u_test(group1, group2)

print(f"Mann-Whitney U statistic: {statistic}")
print(f"p-value: {p_value}")
print(f"Effect size (r): {effect_size}")

median1 = np.median(group1)
median2 = np.median(group2)

mean1 = group1.mean()
mean2 = group2.mean()
print(f"Group 1: Chatbot \t Median: {median1} \t Mean: {mean1}")
print(f"Group 2: Search Engine \t Median: {median2} \t Mean: {mean2}")

# Interpret the results
alpha = 0.05  # Significance level
if p_value < alpha:
    print("There is a statistically significant difference between the two groups.")
else:
    print("There is no statistically significant difference between the two groups.")

print("\nEffect size interpretation: ")
if abs(effect_size) < 0.3:
    print("Small effect")
elif abs(effect_size) < 0.5:
    print("Medium effect")
else:
    print("Large effect")