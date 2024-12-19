import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, f_oneway, ttest_ind, logistic

# Load the dataset
df = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes_20241120.csv")

# Data Preprocessing
df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
df = df[(df['LATITUDE'] != 0) & (df['LONGITUDE'] != 0)]
df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH DATE'] + ' ' + df['CRASH TIME'], errors='coerce')
df['Hour'] = df['CRASH_DATETIME'].dt.hour
df['DayOfWeek'] = df['CRASH_DATETIME'].dt.day_name()
df['Severity'] = (df['NUMBER OF PERSONS INJURED'] + df['NUMBER OF PERSONS KILLED']).fillna(0)



# Hypothesis: ANOVA
anova_result_time = f_oneway(df[df['Hour'].isin([7, 8, 9, 16, 17, 18])]['Severity'], df[~df['Hour'].isin([7, 8, 9, 16, 17, 18])]['Severity'])
anova_result_day = f_oneway(df[df['DayOfWeek'] == 'Monday']['Severity'], 
                            df[df['DayOfWeek'] == 'Tuesday']['Severity'],
                            df[df['DayOfWeek'] == 'Wednesday']['Severity'],
                            df[df['DayOfWeek'] == 'Thursday']['Severity'],
                            df[df['DayOfWeek'] == 'Friday']['Severity'],
                            df[df['DayOfWeek'] == 'Saturday']['Severity'],
                            df[df['DayOfWeek'] == 'Sunday']['Severity'])

print(f"ANOVA for Hypothesis (Time): p-value = {anova_result_time.pvalue}")
print(f"ANOVA for Hypothesis (Day): p-value = {anova_result_day.pvalue}")

