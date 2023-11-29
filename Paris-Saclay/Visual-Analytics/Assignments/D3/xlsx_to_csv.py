import pandas as pd

def xlsx_to_csv(input_file, output_file):
    df = pd.read_excel(input_file)
    df.to_csv(output_file, index=False)
    # print distinct df['Crime Category'].unique()
    print(df['Crime Category'].unique())

# Usage example
input_file = 'spain_tidy_renamed.xlsx'
output_file = 'data.csv'
xlsx_to_csv(input_file, output_file)
