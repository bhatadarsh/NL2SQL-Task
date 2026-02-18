from app.nl2sql import generate_sql_from_question
from app.database import initialize_database, insert_dummy_data

if __name__ == "__main__":

    # Setup DB
    initialize_database()
    insert_dummy_data()

    while True:
        question = input("\nEnter your question: ")

        result = generate_sql_from_question(question)

        print("\nResult:\n")
        print(result)
        print()
