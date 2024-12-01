import requests
import html
import random

def get_question():
    """Get a single random trivia question."""
    url = "https://opentdb.com/api.php?amount=1"
    response = requests.get(url)
    data = response.json()['results'][0]
   
    # Clean up the data (remove HTML entities)
    question = html.unescape(data['question'])
    correct = html.unescape(data['correct_answer'])
    incorrect = [html.unescape(a) for a in data['incorrect_answers']]
   
    # Mix up the answers
    all_answers = [correct] + incorrect
    random.shuffle(all_answers)
   
    return question, all_answers, correct

def play_trivia():
    score = 0
    while True:
        # Get and show the question
        question, answers, correct = get_question()
        print(f"\nQuestion: {question}")
       
        # Show answers
        for i, answer in enumerate(answers, 1):
            print(f"{i}. {answer}")
           
        # Get player's answer
        try:
            choice = int(input("\nYour answer (or 0 to quit): "))
            if choice == 0:
                break
            if choice < 1 or choice > len(answers):
                print("Invalid choice!")
                continue
               
            # Check if correct
            if answers[choice-1] == correct:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The answer was: {correct}")
           
            print(f"Score: {score}")
           
        except ValueError:
            print("Please enter a number!")

if __name__ == "__main__":
    print("Welcome to Simple Trivia! (Enter 0 to quit)")
    play_trivia()
    print(f"\nThanks for playing!")