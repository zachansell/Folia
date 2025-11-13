import pytest
from LeaveSet import LeaveSet
from Quiz import Quiz
from QuizItem import QuizItem

def test_full_quiz_cycle():
    ls = LeaveSet()
    settings = {'num_questions': 5, 'min_len': 2, 'max_len': 4}
    items = ls.genQuizItems(settings)
    assert len(items) == 5
    pairs = [(item.leave, item.value) for item in items]
    quiz = Quiz(pairs)
    assert not quiz.finished
    assert quiz.current_index == 0
    for i, (leave, val) in enumerate(pairs):
        quiz.make_guess(val)
        assert quiz.current_index == i + 1
    assert quiz.finished
    results = quiz.results()
    assert len(results) == 5
    stats = quiz.statistics()
    assert stats['correct_count'] == 5

def test_mixed_accuracy_quiz():
    ls = LeaveSet()
    pairs = list(ls.items())[:5]
    quiz = Quiz(pairs)
    for i, (leave, val) in enumerate(pairs):
        offsets = [0, 1, 2, 5, 10]
        quiz.make_guess(val + offsets[i])
    stats = quiz.statistics()
    assert stats['correct_count'] == 1
    assert stats['excellent_count'] == 2

def test_leaveset_normalize_and_lookup():
    ls = LeaveSet()
    normalized = ls.normalize_leave('abc')
    assert normalized == 'ABC'
    norm1 = ls.normalize_leave('abc')
    norm2 = ls.normalize_leave('ABC')
    norm3 = ls.normalize_leave('cba')
    assert norm1 == norm2 == norm3
    val = ls.get(norm1)
    if val is not None:
        assert ls.get(norm2) == val
        assert ls.get(norm3) == val

def test_quiz_with_blanks():
    ls = LeaveSet()
    settings = {'num_questions': 3, 'must_contain': '?'}
    items = ls.genQuizItems(settings)
    assert len(items) > 0
    for item in items:
        assert '?' in item.leave

def test_complex_filter_combination():
    ls = LeaveSet()
    settings = {
        'num_questions': 5,
        'min_len': 3,
        'max_len': 4,
        'min_vowels': 1,
        'max_consonants': 3,
        'min_value': 0,
        'max_value': 25
    }
    items = ls.genQuizItems(settings)
    for item in items:
        leave_chars = item.leave.replace('?', '')
        assert 3 <= len(leave_chars) <= 4
        vowels = sum(1 for c in leave_chars if c in 'AEIOUY')
        consonants = sum(1 for c in leave_chars if c.isalpha() and c not in 'AEIOUY')
        assert vowels >= 1
        assert consonants <= 3
        assert 0 <= item.value <= 25

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

