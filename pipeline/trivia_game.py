import requests
import html
import random
import pytest
import jsonschema

def get_question():
    """Get a single random trivia question."""
    url = "https://opentdb.com/api.php?amount=1"
    response = requests.get(url)
    data = response.json()['results'][0]
    
    question = html.unescape(data['question'])
    correct = html.unescape(data['correct_answer'])
    incorrect = [html.unescape(a) for a in data['incorrect_answers']]
    
    all_answers = [correct] + incorrect
    random.shuffle(all_answers)
    
    return {
        'question': question,
        'num_answers': len(all_answers),
        'correct_answer': correct,
        'all_answers': all_answers
    }


def play_trivia():
    score = 0
    while True:
        question_data = get_question()
        print(f"\nQuestion: {question_data['question']}")
        
        for i, answer in enumerate(question_data['all_answers'], 1):
            print(f"{i}. {answer}")
        
        try:
            choice = int(input("\nYour answer (or 0 to quit): "))
            if choice == 0:
                break
            if choice < 1 or choice > question_data['num_answers']:
                print("Invalid choice!")
                continue
            
            if question_data['all_answers'][choice-1] == question_data['correct_answer']:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The answer was: {question_data['correct_answer']}")
            
            print(f"Score: {score}")
        
        except ValueError:
            print("Please enter a number!")

if __name__ == "__main__":
    print("Welcome to Simple Trivia! (Enter 0 to quit)")
    play_trivia()
    print(f"\nThanks for playing!")