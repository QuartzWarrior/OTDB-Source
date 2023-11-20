from requests import get  # Importing the 'get' function from the 'requests' module
from time import sleep  # Importing the 'sleep' function from the 'time' module
from csv import (
    writer as csv_writer,
)  # Importing the 'writer' function from the 'csv' module and aliasing it as 'csv_writer'
from urllib.parse import (
    unquote,
)  # Importing the 'unquote' function from the 'urllib.parse' module
from pathlib import Path  # Importing the 'Path' class from the 'pathlib' module

token = get("https://opentdb.com/api_token.php?command=request").json()[
    "token"
]  # Sending a GET request to obtain an API token from a URL and extracting the token value from the JSON response
num = 9  # Assigning the value 9 to the variable 'num' (the first trivia category number)
count = 50  # Assigning the value 50 to the variable 'count'
questions_written = 0  # Assigning the value 0 to the variable 'questions_written'

while 1:  # Starting an infinite loop
    current = get(f"https://opentdb.com/api_category.php").json()["trivia_categories"][
        num - 9
    ][
        "name"
    ]  # Sending a GET request to obtain the current trivia category name from a URL and extracting it from the JSON response

    file_path = Path(
        f"{unquote(current)}.csv"
    ).touch()  # Creating a new file with the name of the current trivia category, URL decoding the category name and appending '.csv' extension

    full_count = get(f"https://opentdb.com/api_count.php?category={num}").json()[
        "category_question_count"
    ][
        "total_question_count"
    ]  # Sending a GET request to obtain the total question count for the current trivia category from a URL and extracting it from the JSON response

    current_count = (
        open(f"{unquote(current)}.csv", "r").read().count("\n")
    )  # Opening the file for the current trivia category in read mode, reading its contents, and counting the number of newline characters to determine the current question count

    left_count = (
        full_count - current_count
    )  # Calculating the number of questions remaining for the current trivia category

    print(
        f"{left_count} questions left in {unquote(current)}"
    )  # Printing the number of questions remaining for the current trivia category

    if (
        count > left_count
    ):  # If the desired question count is greater than the remaining question count
        count = (
            left_count  # Set the desired question count to the remaining question count
        )

    data = get(  # Send a GET request to the Open Trivia Database API
        "https://opentdb.com/api.php?amount={}&category={}&encode=url3986&token={}".format(
            count,
            num,
            token,  # Format the URL with the desired question count, category number, and API token
        )
    ).json()  # Convert the API response to JSON

    if "results" in data:  # If the API response contains a 'results' field
        with open(
            f"{unquote(current)}.csv", "a+", newline=""
        ) as file:  # Open the current category's CSV file in append mode
            writer = csv_writer(file)  # Create a CSV writer

            for result in data["results"]:  # For each result in the API response
                writer.writerow(
                    [result["question"], result["correct_answer"]]
                )  # Write the question and correct answer to the CSV file

            print(  # Print a success message
                f"Successfully wrote {len(data['results'])} questions to {unquote(current)}.csv. Total questions: {current_count + len(data['results'])}"
            )
        questions_written += (
            count  # Increment the total question count by the desired question count
        )
        if (
            questions_written >= full_count
        ):  # If the total question count is greater than or equal to the full question count
            num += 1  # Increment the category number

            count = 50  # Reset the desired question count to 50

            if num == 33:  # If the category number is 33
                print("Done!")  # Print a completion message

                break  # Break the loop
            questions_written = 0  # Reset the total question count
        sleep(
            5.01
        )  # Pause the execution of the program for a little over 5 seconds (to avoid exceeding the API request limit)
    else:  # If the API response does not contain a 'results' field
        num += 1  # Increment the category number

        count = 50  # Reset the desired question count to 50

        if num == 33:  # If the category number is 33
            print("Done!")  # Print a completion message

            break  # Break the loop
        questions_written = 0  # Reset the total question count

        sleep(
            5.01
        )  # Pause the execution of the program for a little over 5 seconds (to avoid exceeding the API request limit)
