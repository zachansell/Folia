import pytest
from unittest.mock import Mock, patch
from LeaveSet import LeaveSet
from Quiz import Quiz

def test_trainer_app_initialization():
    """Test that the trainer initializes with LeaveSet and Quiz support"""
    with patch('tkinter.Tk'):
        mock_root = Mock()
        from scrabble_leave_trainer import SimpleLeaveTrainer
        with patch.object(SimpleLeaveTrainer, '_setup_ui'), \
             patch.object(SimpleLeaveTrainer, '_load_session'):
            trainer = SimpleLeaveTrainer(mock_root)
            assert trainer._leaves is not None
            assert trainer._quiz is None

def test_scrabble_trainer_initialization():
    with patch('tkinter.Tk') as mock_tk:
        mock_root = Mock()
        mock_root.title = Mock()
        mock_root.geometry = Mock()
        mock_root.configure = Mock()
        from scrabble_leave_trainer import SimpleLeaveTrainer
        with patch.object(SimpleLeaveTrainer, '_setup_ui'), \
             patch.object(SimpleLeaveTrainer, '_load_session'):
            trainer = SimpleLeaveTrainer(mock_root)
            assert trainer._leaves is not None

def test_quiz_generation_from_leaveset():
    ls = LeaveSet()
    settings = {'num_questions': 5, 'min_len': 2, 'max_len': 4}
    items = ls.genQuizItems(settings)
    assert len(items) <= 5
    for item in items:
        assert 2 <= len(item.leave.replace('?', '')) <= 4

def test_quiz_statistics():
    questions = [("A", 10.0), ("B", 20.0), ("C", 30.0)]
    quiz = Quiz(questions)
    quiz.make_guess(11.0)
    quiz.make_guess(22.0)
    quiz.make_guess(35.0)
    stats = quiz.statistics()
    assert 'avg_delta' in stats
    assert 'accuracy' in stats
    assert stats['correct_count'] == 0
    assert stats['excellent_count'] == 1

def test_leaveset_filters_vowels():
    ls = LeaveSet()
    settings = {'num_questions': 3, 'min_vowels': 2, 'max_vowels': 3}
    items = ls.genQuizItems(settings)
    for item in items:
        vowels = sum(1 for c in item.leave.replace('?', '') if c in 'AEIOUY')
        assert 2 <= vowels <= 3

def test_leaveset_filters_consonants():
    ls = LeaveSet()
    settings = {'num_questions': 3, 'min_consonants': 2}
    items = ls.genQuizItems(settings)
    for item in items:
        consonants = sum(1 for c in item.leave.replace('?', '') if c.isalpha() and c not in 'AEIOUY')
        assert consonants >= 2

def test_leaveset_must_contain():
    ls = LeaveSet()
    settings = {'num_questions': 3, 'must_contain': 'S'}
    items = ls.genQuizItems(settings)
    for item in items:
        assert 'S' in item.leave

def test_leaveset_must_not_contain():
    ls = LeaveSet()
    settings = {'num_questions': 3, 'must_not_contain': 'Q'}
    items = ls.genQuizItems(settings)
    for item in items:
        assert 'Q' not in item.leave

def test_leaveset_value_range():
    ls = LeaveSet()
    settings = {'num_questions': 5, 'min_value': 10, 'max_value': 20}
    items = ls.genQuizItems(settings)
    for item in items:
        assert 10 <= item.value <= 20

def test_csv_validation_rejects_malformed():
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("AB,10.0\n")
        f.write("CD,20.0\n")
        f.write("12,invalid\n")
        f.write("EF,30.0\n")
        fname = f.name
    try:
        ls = LeaveSet(fname)
        assert 'AB' in ls
        assert 'CD' in ls
        assert '12' not in ls
        assert 'EF' in ls
    finally:
        os.unlink(fname)

def test_session_persistence():
    import tempfile, json, os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump({'sessions': 5, 'quizzes': 10}, f)
        fname = f.name
    try:
        with open(fname, 'r') as f:
            data = json.load(f)
        assert data['sessions'] == 5
        assert data['quizzes'] == 10
    finally:
        os.unlink(fname)

def test_quiz_workflow_integration():
    ls = LeaveSet()
    settings = {'num_questions': 3}
    pairs = [(item.leave, item.value) for item in ls.genQuizItems(settings)]
    quiz = Quiz(pairs)
    for leave, val in pairs:
        quiz.make_guess(val + 1)
    assert quiz.finished
    assert len(quiz.results()) == 3

def test_quiz_time_accumulation():
    import time
    questions = [("A", 10.0), ("B", 20.0)]
    quiz = Quiz(questions)
    time.sleep(0.01)
    quiz.make_guess(10.0)
    time.sleep(0.01)
    quiz.make_guess(20.0)
    assert quiz.total_time >= 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

