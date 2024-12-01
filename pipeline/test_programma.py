import pytest
import jsonschema
from trivia_game import get_question

# JSON Schema for validating trivia API response
TRIVIA_SCHEMA = {
    "type": "object",
    "properties": {
        "response_code": {"type": "integer"},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "correct_answer": {"type": "string"},
                    "incorrect_answers": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["question", "correct_answer", "incorrect_answers"]
            }
        }
    },
    "required": ["response_code", "results"]
}

# Sample response for testing
SAMPLE_RESPONSE = {
    "response_code": 0,
    "results": [{
        "question": "What is the atomic number of Carbon?",
        "correct_answer": "6",
        "incorrect_answers": ["4", "8", "12"]
    }]
}

def test_schema_validation():
    """Validate that our sample response matches the schema"""
    jsonschema.validate(instance=SAMPLE_RESPONSE, schema=TRIVIA_SCHEMA)

def test_question_format(snapshot):
    """Test question format matches snapshot"""
    question, answers, correct = get_question()
   
    result = {
        'question': question,
        'num_answers': len(answers),
        'correct_answer': correct
    }
   
    assert result == snapshot