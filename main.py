from app.services.nl2sql import run_pipeline


while True:

    q = input("Enter your question: ")

    result = run_pipeline(q)

    print(result)
