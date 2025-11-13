import json
import os
import tempfile
from unittest.mock import Mock, patch, ANY

import pytest

from Quiz import Quiz


def build_trainer_with_mocks():
    with patch('tkinter.Tk'):
        from scrabble_leave_trainer import SimpleLeaveTrainer
        with patch.object(SimpleLeaveTrainer, '_setup_ui'), \
             patch.object(SimpleLeaveTrainer, '_load_session'):
            root = Mock()
            trainer = SimpleLeaveTrainer(root)
            trainer.quiz_label = Mock()
            trainer.leave_label = Mock()
            trainer.guess_entry = Mock()
            trainer.score_label = Mock()
            trainer.rating_label = Mock()
            trainer.lookup_entry = Mock()
            trainer.result_label = Mock()
            trainer.stats_label = Mock()
            trainer._stats = {
                'sessions': 0, 'quizzes': 0,
                'lifetime_score': 0, 'lifetime_total': 0,
                'total_delta': 0, 'perfect_count': 0
            }
            return trainer


def test_start_quiz_updates_state_and_labels():
    trainer = build_trainer_with_mocks()
    trainer.guess_entry.delete = Mock()
    trainer.guess_entry.focus_set = Mock()
    with patch.object(trainer, '_generate_questions', return_value=[('AB', 10.0), ('CD', 20.0)]), \
         patch.object(trainer, '_save_session') as save_mock:
        trainer.start_quiz(num_questions=2)
        assert trainer._quiz is not None
        assert trainer._stats['quizzes'] == 1
        save_mock.assert_called()
        trainer.leave_label.config.assert_any_call(text='AB')
        trainer.quiz_label.config.assert_any_call(text="What's the value of this leave?")
        trainer.guess_entry.delete.assert_called()
        trainer.guess_entry.focus_set.assert_called()


def test_check_guess_when_not_started_shows_info():
    trainer = build_trainer_with_mocks()
    with patch('tkinter.messagebox.showinfo') as showinfo:
        trainer.check_guess()
        showinfo.assert_called_once()


def test_check_guess_invalid_input_shows_error():
    trainer = build_trainer_with_mocks()
    trainer._quiz = Quiz([('AB', 10.0)])
    trainer.guess_entry.get = Mock(return_value='not-a-number')
    with patch('tkinter.messagebox.showerror') as showerror:
        trainer.check_guess()
        showerror.assert_called_once()

        assert trainer._quiz.current_index == 0


def test_check_guess_progresses_and_shows_results():
    trainer = build_trainer_with_mocks()
    trainer._quiz = Quiz([('AB', 10.0)])
    trainer.guess_entry.get = Mock(return_value='10.0')
    trainer.root.after = lambda ms, fn: fn()
    with patch('tkinter.messagebox.askyesno', return_value=False):
        trainer.check_guess()
        assert trainer._quiz.finished
        trainer.rating_label.config.assert_any_call(text='CORRECT', fg=ANY)


def test_lookup_leave_found_and_not_found():
    trainer = build_trainer_with_mocks()
    trainer._leaves.values = {'ABC': 12.34}
    trainer.lookup_entry.get = Mock(return_value='abc')
    trainer.lookup_leave()
    trainer.result_label.config.assert_any_call(text='ABC\n= 12.3', fg='#16a085')
    trainer.lookup_entry.get = Mock(return_value='zzz')
    trainer.lookup_leave()
    trainer.result_label.config.assert_any_call(text='ZZZ\nNot found', fg='#e74c3c')


def test_update_stats_display_text_contains_expected_fields():
    trainer = build_trainer_with_mocks()
    trainer._stats = {
        'sessions': 2,
        'quizzes': 3,
        'lifetime_score': 15,
        'lifetime_total': 30,
        'total_delta': 0,
        'perfect_count': 0
    }
    trainer._update_stats_display()
    calls = [kwargs for args, kwargs in trainer.stats_label.config.call_args_list]
    assert calls, "stats_label.config should be called at least once"
    text_val = calls[-1]['text']
    assert 'Sessions: 2' in text_val
    assert 'Quizzes: 3' in text_val
    assert '(50.0%)' in text_val


def test_load_and_save_session_round_trip(tmp_path):
    trainer = build_trainer_with_mocks()
    sess_path = tmp_path / 'session.json'
    with open(sess_path, 'w') as f:
        json.dump({'sessions': 5, 'quizzes': 10, 'lifetime_score': 1, 'lifetime_total': 2}, f)
    trainer._session_file = str(sess_path)
    trainer._load_session()
    assert trainer._stats['sessions'] == 6
    trainer._save_session()
    with open(sess_path, 'r') as f:
        data = json.load(f)
    assert data['sessions'] == 6
    assert data['quizzes'] == trainer._stats['quizzes']

