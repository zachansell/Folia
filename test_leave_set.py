#!/usr/bin/env python3

import pytest
from LeaveSet import LeaveSet
import json
import os
import random
from QuizItem import QuizItem

def test_leave_set_loads():
    ls = LeaveSet()
    assert len(ls.values) > 0
    keys = list(ls.keys())
    assert len(keys) > 0
    
    item_keys = set(k for k, _ in ls.items())
    for k in keys:
        assert k in ls.values
        assert k in item_keys
    
    assert '?' in ls
    assert 'S' in ls

def test_normalize_leave():
    ls = LeaveSet()
    assert ls.normalize_leave('xyz') == 'XYZ'
    assert ls.normalize_leave('XYZ') == 'XYZ'
    assert ls.normalize_leave('zyx') == 'XYZ'
    assert ls.normalize_leave('x?y') == '?XY'
    assert ls.normalize_leave('a') == 'A'
    assert ls.normalize_leave('AiouoQ') == 'AIOOQU'
    assert ls.normalize_leave('P?Qriu') == '?IPQRU'

def test_get_value():
    ls = LeaveSet()
    value = ls.get('S')
    assert value is not None
    assert isinstance(value, (int, float))
    assert ls.get('ZZZZZ', -9999999999) == -9999999999

def test_blanks_are_valuable():
    ls = LeaveSet()
    assert ls.get('?') > 15
    assert ls.get('??') > ls.get('?')

def test_session_tracking():
    test_file = 'test_session.json'
    data = {'sessions': 5, 'quizzes': 10}
    
    with open(test_file, 'w') as f:
        json.dump(data, f)
    
    with open(test_file, 'r') as f:
        loaded = json.load(f)
    
    assert loaded['sessions'] == 5
    assert loaded['quizzes'] == 10
    
    os.unlink(test_file)

def test_value_ranges():
    ls = LeaveSet()
    values = [v for v in ls.values_list() if v is not None]
    assert min(values) > -50
    assert max(values) < 100

def test_unique_keys():
    ls = LeaveSet()
    keys = list(ls.keys())
    unique_keys = set(keys)
    assert len(keys) == len(unique_keys), "Initial keys in LeaveSet are not unique"
    
def test_value_type_consistency():
    ls = LeaveSet()
    for value in ls.values_list():
        assert isinstance(value, (int, float)), f"Value {value} is not of type int or float"


def test_genQuizItems_basic_returns_item():
    random.seed(0)
    ls = LeaveSet()
    items = ls.genQuizItems({'num_questions': 1})
    assert isinstance(items, list)
    assert len(items) == 1
    assert isinstance(items[0], QuizItem)


def test_genQuizItems_min_len_filters_to_none():
    ls = LeaveSet()
    max_len = 0
    for k in ls.keys():
        l = len(k)
        if l > max_len:
            max_len = l
    items = ls.genQuizItems({'num_questions': 1, 'min_len': max_len + 1})
    assert items == [] or len(items) == 0


def test_genQuizItems_must_contain_and_not_contain():
    ls = LeaveSet()
    letter = None
    for k in ls.keys():
        for ch in k:
            if ch.isalpha():
                letter = ch
                break
        if letter:
            break
    if not letter:
        pytest.skip("No alphabetic characters in LeaveSet keys to test must_contain")

    items = ls.genQuizItems({'num_questions': 10, 'must_contain': letter, 'must_not_contain': 'Z'})
    for it in items:
        assert letter in it.leave and 'Z' not in it.leave


def test_genQuizItems_value_range():
    ls = LeaveSet()
    vals = [v for v in ls.values_list() if v is not None]
    if not vals:
        pytest.skip("No values in LeaveSet")
    min_v = min(vals)
    max_v = max(vals)
    items = ls.genQuizItems({'num_questions': 10, 'min_value': min_v, 'max_value': max_v})
    for it in items:
        assert it.value >= min_v and it.value <= max_v


def test_genQuizItems_num_questions_limit():
    ls = LeaveSet()
    candidates_count = len([1 for k, v in ls.items() if v is not None])
    for num_q in (1, 5, 10, 50):
        items = ls.genQuizItems({'num_questions': num_q})
        expected = num_q if num_q > 0 and num_q <= candidates_count else candidates_count
        assert len(items) == expected


def test_genQuizItems_max_len_filters():
    ls = LeaveSet()
    max_len = 3
    items = ls.genQuizItems({'num_questions': 100, 'max_len': max_len})
    for it in items:
        assert len(it.leave) <= max_len, f"Leave '{it.leave}' length {len(it.leave)} exceeds max_len {max_len}"


def test_genQuizItems_min_len_filters():
    ls = LeaveSet()
    min_len = 5
    items = ls.genQuizItems({'num_questions': 100, 'min_len': min_len})
    for it in items:
        assert len(it.leave) >= min_len, f"Leave '{it.leave}' length {len(it.leave)} below min_len {min_len}"


def test_genQuizItems_vowel_and_consonant_filters():
    ls = LeaveSet()
    settings = {
        'num_questions': 100,
        'min_vowels': 1,
        'max_vowels': 3,
        'min_consonants': 1,
        'max_consonants': 4,
    }
    items = ls.genQuizItems(settings)
    vowels = set('AEIOUY')
    for it in items:
        letters_only = [c for c in it.leave if c != '?']
        vowel_count = sum(1 for c in letters_only if c in vowels)
        cons_count = sum(1 for c in letters_only if c.isalpha() and c not in vowels)
        assert 1 <= vowel_count <= 3
        assert 1 <= cons_count <= 4


def test_genQuizItems_zero_questions_returns_all():
    ls = LeaveSet()
    candidates = [c for c in ls.items() if c[1] is not None]
    items = ls.genQuizItems({'num_questions': 0})
    assert len(items) == len(candidates)


def test_genQuizItems_all_items_are_quizitem():
    ls = LeaveSet()
    items = ls.genQuizItems({'num_questions': 20})
    for it in items:
        assert isinstance(it, QuizItem)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])