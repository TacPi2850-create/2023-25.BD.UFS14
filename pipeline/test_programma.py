import pytest
import json
from unittest.mock import patch, MagicMock
import jsonschema
from trivia_game import get_question, play_trivia

# JSON Schema for the trivia API response
TRIVIA_SCHEMA = {
    "type": "object",
    "properties": {
        "response_code": {"type": "integer"},
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "type": {"type": "string"},
                    "difficulty": {"type": "string"},
                    "question": {"type": "string"},
                    "correct_answer": {"type": "string"},
                    "incorrect_answers": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": [
                    "category",
                    "type",
                    "difficulty",
                    "question",
                    "correct_answer",
                    "incorrect_answers"
                ]
            }
        }
    },
    "required": ["response_code", "results"]
}

# Sample API response for testing
SAMPLE_RESPONSE = {
    "response_code": 0,
    "results": [{
        "category": "Science",
        "type": "multiple",
        "difficulty": "medium",
        "question": "What is the atomic number of Carbon?",
        "correct_answer": "6",
        "incorrect_answers": ["4", "8", "12"]
    }]
}

def test_schema_validation():
    """Test that the sample response matches our schema"""
    jsonschema.validate(instance=SAMPLE_RESPONSE, schema=TRIVIA_SCHEMA)

@pytest.fixture
def mock_api_response():
    """Fixture to provide a mock API response"""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_get.return_value = mock_response
        yield mock_get

def test_get_question(mock_api_response, snapshot):
    """Test the get_question function and compare with snapshot"""
    question, answers, correct = get_question()
   
    # Create a snapshot-friendly format
    result = {
        'question': question,
        'answers_length': len(answers),
        'correct_answer': correct
    }
   
    # Compare with snapshot
    assert result == snapshot

@pytest.mark.parametrize("input_sequence,expected_score", [
    (["1", "0"], 1),  # Correct answer then quit
    (["2", "0"], 0),  # Wrong answer then quit
    (["invalid", "1", "0"], 1),  # Invalid input, then correct, then quit
])
def test_play_trivia(mock_api_response, monkeypatch, input_sequence):
    """Test the play_trivia function with different input sequences"""
    # Mock the input function
    inputs = iter(input_sequence)
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
   
    # Mock print to capture output
    printed_messages = []
    monkeypatch.setattr('builtins.print', lambda *args: printed_messages.append(' '.join(map(str, args))))
   
    # Run the game
    play_trivia()
   
    # Check if score was printed correctly
    score_messages = [msg for msg in printed_messages if msg.startswith('Score:')]
    if score_messages:
        final_score = int(score_messages[-1].split(': ')[1])
        assert final_score == expected_score

def test_error_handling(mock_api_response):
    """Test error handling in get_question"""
    # Mock an API error
    mock_api_response.side_effect = Exception("API Error")
   
    with pytest.raises(Exception):
        get_question()

# Create snapshots/conftest.py
@pytest.fixture
def snapshot(snapshot_session):
    """Fixture for snapshot testing"""
    return snapshot_session

# Example snapshot (snapshots/snap_test_trivia.py)
snapshots = {
    'test_get_question': {
        'question': 'What is the atomic number of Carbon?',
        'answers_length': 4,
        'correct_answer': '6'
    }
}