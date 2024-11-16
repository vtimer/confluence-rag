import numpy as np
import pandas as pd
from scipy import stats


def vargha_delaney_a12(group1, group2):
    m, n = len(group1), len(group2)
    r = stats.rankdata(np.concatenate([group1, group2]))
    r1 = sum(r[:m])
    a12 = (r1 / m - (m + 1.0) / 2.0) / n
    return a12


def interpret_a12(a12):
    if a12 <= 0.29 or a12 >= 0.71:
        return "Large"
    elif a12 <= 0.36 or a12 >= 0.64:
        return "Medium"
    elif a12 <= 0.44 or a12 >= 0.56:
        return "Small"
    else:
        return "Negligible"


# Read data from CSV files
file1 = "rag.csv"
file2 = "searchengine.csv"

df1 = pd.read_csv(file1, sep=",", header=None)
df2 = pd.read_csv(file2, sep=",", header=None)
# Assuming the data is in the second column of each CSV file
group1_data = df1.iloc[:, 1].values
group2_data = df2.iloc[:, 1].values

# Calculate A12
a12 = vargha_delaney_a12(group1_data, group2_data)

print(f"Vargha-Delaney A12: {a12:.3f}")
print(f"Effect size: {interpret_a12(a12)}")

if a12 < 0.5:
    print(f"In {((1 - a12) * 100):.1f}% of cases, Group 1: chatbot tends to have lower (better) values")
elif a12 > 0.5:
    print(f"In {(a12 * 100):.1f}% of cases, Group 2: search engine tends to have lower (better) values")
else:
    print("No difference between the groups")

# Initialize counters
lower_count = 0
equal_count = 0
higher_count = 0

# Ensure both arrays have the same length
min_length = min(len(group1_data), len(group1_data))

# Compare elements at the same position
for i in range(min_length):
    if group1_data[i] < group2_data[i]:
        lower_count += 1
    elif group1_data[i] == group2_data[i]:
        equal_count += 1
    else:
        higher_count += 1

# Print results
print(f"Comparing elements at the same position in both arrays:")
print(f"Items in first array were:")
print(f"Lower: {lower_count} times")
print(f"Equal: {equal_count} times")
print(f"Higher: {higher_count} times")