import pandas as pd
import sqlite3
import openai

openai.api_key = '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'

conn = sqlite3.connect('acceptable_answers_db.sqlite')

candidate_df = pd.read_csv('candidate_answers.csv')

prompts = []

for idx, row in candidate_df.iterrows():
    # Retrieve the question and candidate answer
    question = row['question']
    answer = row['answer']

    # Get the acceptable answer from the SQLite database
    cur = conn.cursor()
    cur.execute("SELECT acceptable_answer, rating FROM AcceptableAnswers WHERE question = ?", (question,))
    row = cur.fetchone()

    if row is None:
        continue 

    acceptable_answer, rating = row

    prompts.append(
    f"Question: {question}\n"
    f"Candidate's Answer: {answer}\n"
    f"Acceptable Answer: {acceptable_answer}\n"
    f"Expected Rating: {rating}\n"
    f"Evaluate the candidate's answer in terms of its correctness, completeness, and depth, compared to the acceptable answer, "
    f"and consider the expected rating. Provide a detailed analysis.")

overall_prompt = "Candidate responses:\n" + "\n".join(prompts) + "\nPlease provide an overall analysis of the candidate's performance. Consider the ratings of each answer in comparison to the candidate's answer to give an accurate analysis of the candidate."

response = openai.Completion.create(engine="text-davinci-003", prompt=overall_prompt, max_tokens=200)

analysis = response.choices[0].text.strip()

print(f"Candidate Analysis:\n{analysis}\n")

conn.close()
