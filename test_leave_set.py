#!/usr/bin/env python3

import pytest
from LeaveSet import LeaveSet
import json
import os

def test_leave_set_loads():
    ls = LeaveSet()
    assert len(ls.values) > 0
    assert '?' in ls
    assert 'S' in ls

def test_normalize_leave():
    ls = LeaveSet()
    assert ls.normalize_leave('xyz') == 'XYZ'
    assert ls.normalize_leave('zyx') == 'ZYX'
    assert ls.normalize_leave('x?y') == '?XY'

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

if __name__ == "__main__":
    pytest.main([__file__, "-v"])