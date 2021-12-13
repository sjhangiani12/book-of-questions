import pandas as pd


df = pd.read_csv("book_of_questions.csv")
df.columns = ['col', 'questions', 'fad', 'dfak', 'dlafk', 'sddf', 'fjke']
list_of_questions = df[['questions']].dropna()

print(list_of_questions.to_csv("cleaned_questions.csv"))