import pytest
from Quiz import Quiz
from QuizItem import QuizItem

def test_quiz_creation():
    questions = [("A", 10.0), ("B", 20.0), ("C", 30.0)]
    quiz = Quiz(questions)
    assert len(quiz.questions) == 3
    assert quiz.current_index == 0
    assert not quiz.finished

def test_guessing():
    questions = [("A", 10.0), ("B", 20.0)]
    quiz = Quiz(questions)

    quiz.make_guess(11.0)
    assert quiz.current_index == 1
    assert not quiz.finished
    current = quiz.questions[0]
    assert current.guess == 11.0
    assert current.delta == 1.0
    assert current.rating == "excellent"

    quiz.make_guess(25.0)
    assert quiz.current_index == 2
    assert quiz.finished
    current = quiz.questions[1]
    assert current.guess == 25.0
    assert current.delta == 5.0
    assert current.rating == "good"
    #todo: test time elapsed stuff

def test_quiz_results():
    questions = [("A", 10.0), ("B", 20.0)]
    quiz = Quiz(questions)

    quiz.make_guess(10.0)
    quiz.make_guess(22.0)

    results = quiz.results()
    assert len(results) == 2
    assert results[0]["leave"] == "A"
    assert results[0]["value"] == 10.0
    assert results[0]["guess"] == 10.0
    assert results[0]["delta"] == 0.0
    assert results[0]["rating"] == "correct"

    assert results[1]["leave"] == "B"
    assert results[1]["value"] == 20.0
    assert results[1]["guess"] == 22.0
    assert results[1]["delta"] == 2.0
    assert results[1]["rating"] == "great"

def test_no_guess_after_finished():
    questions = [("A", 10.0)]
    quiz = Quiz(questions)

    quiz.make_guess(10.0)
    assert quiz.finished

    quiz.make_guess(15.0)
    assert quiz.current_index == 1
    current = quiz.questions[0]
    assert current.guess == 10.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])