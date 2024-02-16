import os
import pandas
file_name = "poc/cefr_leveled_texts.csv"
print(os.getcwd())
# Read data from CSV file into a DataFrame
df = pandas.read_csv(f'{file_name}')

# Add a new column named "id" with values 1, 2, 3, ...
df['id'] = range(1, len(df) + 1)

# Save the DataFrame back to the same CSV file, replacing the existing file
df.to_csv(f'{file_name}', index=False)

print("File saved successfully.")
