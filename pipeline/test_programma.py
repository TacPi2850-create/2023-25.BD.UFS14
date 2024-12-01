import pytest
import jsonschema
import requests
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
def mock_requests(mocker):
    """Fixture to provide a mock API response"""
    mock = mocker.patch('requests.get')
    mock.return_value.json.return_value = SAMPLE_RESPONSE
    return mock

def test_get_question(mock_requests):
    """Test the get_question function returns expected format"""
    question, answers, correct = get_question()
   
    assert question == SAMPLE_RESPONSE['results'][0]['question']
    assert len(answers) == 4  # All answers (1 correct + 3 incorrect)
    assert correct == SAMPLE_RESPONSE['results'][0]['correct_answer']
    assert all(isinstance(answer, str) for answer in answers)

@pytest.mark.parametrize("user_inputs,expected_score", [
    (["1", "0"], 1),           # Correct answer then quit
    (["2", "0"], 0),           # Wrong answer then quit
    (["invalid", "1", "0"], 1) # Invalid input, correct answer, quit
])
def test_play_trivia(mock_requests, mocker, user_inputs, expected_score):
    """Test the play_trivia function with different input sequences"""
    # Mock input() to return our test inputs
    inputs = iter(user_inputs)
    mocker.patch('builtins.input', lambda _: next(inputs))
   
    # Mock print() to capture output
    printed = []
    mocker.patch('builtins.print', lambda *args: printed.append(' '.join(map(str, args))))
   
    # Run game
    play_trivia()
   
    # Check final score
    score_messages = [msg for msg in printed if msg.startswith('Score:')]
    assert score_messages, "No score was printed"
    final_score = int(score_messages[-1].split(': ')[1])
    assert final_score == expected_score

def test_api_error(mocker):
    """Test error handling when API request fails"""
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = requests.RequestException("API Error")
   
    with pytest.raises(requests.RequestException):
        get_question()