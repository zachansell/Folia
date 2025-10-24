import pytest
from Quiz import Quiz
from QuizItem import QuizItem

def test_quiz_creation()
    questions = [("A", 10.0), ("B", 20.0), ("C", 30.0)]
    quiz = Quiz(questions)
    assert len(quiz.questions) == 3
    assert quiz.current_index == 0
    assert not quiz.finished

if __name__ == "__main__":
    pytest.main([__file__, "-v"])