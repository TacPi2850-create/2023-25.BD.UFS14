import azure.functions as func
import requests
import random
import logging

app = func.FunctionApp()

def get_question():
    """Get a single random trivia question."""
    url = "https://opentdb.com/api.php?amount=1"
    response = requests.get(url)
    data = response.json()['results'][0]
   
    question = data['question']
    correct = data['correct_answer']
    incorrect = data['incorrect_answers']
   
    # Mix up the answers
    all_answers = [correct] + incorrect
    random.shuffle(all_answers)
   
    return question, all_answers, correct

@app.route(route="TriviaHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def TriviaHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get a question
    question, answers, correct = get_question()
   
    # Format the response as a string
    response = f"Question: {question}\n\n"
    for i, answer in enumerate(answers, 1):
        response += f"{i}. {answer}\n"
   
    return func.HttpResponse(response)