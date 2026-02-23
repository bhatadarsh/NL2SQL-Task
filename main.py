from app.execution.database import initialize_database, insert_dummy_data
from app.services.nl2sql import process_question


if __name__ == "__main__":

    initialize_database()
    insert_dummy_data()

    while True:
        question = input("\nEnter your question: ")
        response = process_question(question)

        if "error" in response:
            print("Error:", response["error"])
        else:
            print("\nGenerated SQL:\n", response["sql"])
            print("\nResults:\n", response["data"])