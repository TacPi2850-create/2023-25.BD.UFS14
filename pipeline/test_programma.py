import json
import requests
import jsonschema
import pytest
import html
import random

QUESTION_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "num_answers": {"type": "integer", "minimum": 2},
        "correct_answer": {"type": "string"},
        "all_answers": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 2
        }
    },
    "required": ["question", "num_answers", "correct_answer", "all_answers"]
}

def test_question_schema():
    """Test that the question meets the JSON schema."""
    question_data = get_question()
    jsonschema.validate(instance=question_data, schema=QUESTION_SCHEMA)

def test_question_format(snapshot):
    """Snapshot test for question format."""
    question_data = get_question()
    snapshot.assert_match({
        'question': question_data['question'],
        'num_answers': question_data['num_answers'],
        'correct_answer': question_data['correct_answer']
    })