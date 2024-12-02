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
        "question": "Which retro video game was released first?",
        "correct_answer": "Space Invaders",
        "incorrect_answers": ["Pac-Man", "Donkey Kong", "Frogger"]
    }]
}

def test_schema_validation():
    """Validate that our sample response matches the schema"""
    jsonschema.validate(instance=SAMPLE_RESPONSE, schema=TRIVIA_SCHEMA)

def test_question_format(snapshot):
    snapshot.snapshot_dir='snapshots'
    schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "question": {
            "type": "string"
        },
        "num_answers": {
            "type": "integer"
        },
        "correct_answer": {
            "type": "string"
        }
    },
    "required": ["question", "num_answers", "correct_answer"]
    }
   
    snapshot.assert_match(schema, 'risposte.txt')