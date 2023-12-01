import pandas as pd

# Usage example
input_file_1 = 'spain_tidy_renamed.xlsx'
input_file_2 = 'spain_population_tidy.csv'
output_file = 'data.csv'

df1 = pd.read_excel(input_file_1)
df2 = pd.read_csv(input_file_2)

# Join the two df for df2.year == df1.year and df2.place == df1.place
df = pd.merge(df1, df2,  how='left', left_on=['Year','Place'], right_on = ['Year','Place'])

# Save the result in a csv file
df.to_csv(output_file, index=False)