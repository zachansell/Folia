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
        l = len([c for c in k if c != '?'])
        if l > max_len:
            max_len = l
    items = ls.genQuizItems({'num_questions': 1, 'min_len': max_len + 1})
    assert items == [] or len(items) == 0


def test_genQuizItems_must_contain_and_not_contain():
    ls = LeaveSet()
    keys = list(ls.keys())
    sample_key = next((k for k in keys if k != '?'), None)
    if sample_key is None:
        pytest.skip("No suitable keys to test")
    ch = sample_key.replace('?', '')[0]
    items = ls.genQuizItems({'num_questions': 0, 'must_contain': ch, 'must_not_contain': 'Z'})
    for it in items:
        assert ch in it.leave


def test_genQuizItems_value_range():
    ls = LeaveSet()
    vals = [v for v in ls.values_list() if v is not None]
    if not vals:
        pytest.skip("No values in LeaveSet")
    min_v = min(vals)
    items = ls.genQuizItems({'num_questions': 0, 'min_value': min_v, 'max_value': min_v})
    for it in items:
        assert it.value == min_v

if __name__ == "__main__":
    pytest.main([__file__, "-v"])