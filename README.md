# Trivia.py

This Python script uses the Open Trivia Database API to fetch trivia questions and write them to CSV files. Each file corresponds to a different trivia category.

## How it works

1. The script first obtains an API token from the Open Trivia Database.
2. It then enters an infinite loop, where it fetches trivia questions for each category (from category 9 to 32).
3. For each category, it creates a CSV file named after the category.
4. It fetches the total number of questions available for the current category.
5. It then calculates the number of questions left to fetch for the current category.
6. If the desired number of questions to fetch is greater than the remaining number of questions, it adjusts the desired number.
7. It then sends a GET request to the API to fetch the desired number of questions.
8. If the API response contains a 'results' field, it writes each question and its correct answer to the CSV file.
9. It then increments the total number of questions written and checks if it has fetched all questions for the current category. If so, it moves on to the next category.
10. If the API response does not contain a 'results' field, it moves on to the next category.
11. The script pauses for a little over 5 seconds after each API request to avoid exceeding the API's request limit.
12. The script stops after fetching questions for all categories.

## Requirements

- Python 3
- `requests` module
- `time` module
- `csv` module
- `urllib.parse` module
- `pathlib` module

## Usage

Run the script in your terminal as follows:

```bash
python trivia.py
```

This will create CSV files in the same directory as the script. Each file will be named after a trivia category and will contain trivia questions and their correct answers.
