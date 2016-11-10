#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run from the root folder with either 'python setup.py test' or
'py.test test/test_sparkline.py'.
"""

from __future__ import unicode_literals, print_function

import pytest

from sparklines import sparklines, scale_values
from sparklines.__main__ import test_valid_number as is_valid_number


def test_parse_float():
    "Test parsing input numbers."

    t = is_valid_number

    assert t('4.5') == '4.5'
    assert t('-4.5') == '-4.5'
    assert t('4.') == '4.'
    assert t('.5') == '.5'
    assert t('4.5e0') == '4.5e0'
    assert t('-4.5e0') == '-4.5e0'
    assert t('-4.5e-2') == '-4.5e-2'
    assert t('-.5e-2') == '-.5e-2'

    assert t('4.5,') == '4.5'
    assert t('4.5;') == '4.5'
    assert t('"4.5"') == '4.5'
    assert t('(4.5)') == '4.5'

    assert t('null') == 'null'
    assert t('Null') == 'null'
    assert t('none') == 'none'
    assert t('None') == 'none'

    assert t('None,') == 'none'

    with pytest.raises(ValueError):
        t(',')
    with pytest.raises(ValueError):
        t('invalid')


def test_scale0():
    "Test scale..."

    res = scale_values([1, 2, 3])
    exp = [1., 4., 8.]
    assert res == exp


def test_scale1():
    "Test scale..."

    res = scale_values([1, 2, 3], num_lines=2)
    exp = [1., 9., 18.]
    assert res == exp


def test_scale_pi():
    "Test scale Pi."

    res = scale_values([3, 1, 4, 1, 5, 9, 2, 6])
    exp = [3, 1, 4, 1, 4, 8, 2, 5]
    assert res == exp


def test_pi():
    "Test first eight digits of Pi."

    res = sparklines([3, 1, 4, 1, 5, 9, 2, 6])
    exp = ['▃▁▄▁▄█▂▅']
    assert res == exp


def test_minmax():
    "Test two values, min and max."

    res = sparklines([1, 8])
    exp = ['▁█'] # 1, 8
    assert res == exp


def test_rounding0():
    "Test two values, min and max."

    res = sparklines([1, 5, 8])
    exp = ['▁▅█'] # 1, 5, 8
    assert res == exp

def test_maximum():
    res = sparklines([1, 2, 3, 10, 10], maximum=3)
    exp = ['▁▄███']
    assert res == exp

def test_maximum_internal_consistency():
    res = sparklines([1, 2, 3, 10, 10, 1], maximum=3)
    exp = sparklines([1, 2, 3, 3, 3, 1], maximum=3)
    assert res == exp


def test_minimum():
    res = sparklines([0, 0, 11, 12, 13], minimum=10)
    exp = ['▁▁▃▆█']
    assert res == exp

def test_minimum_internal_consistency():
    res = sparklines([0, 0, 11, 12, 13], minimum=10)
    exp = sparklines([10, 10, 11, 12, 13], minimum=10)
    assert res == exp

def test1():
    "Test single values all have the same four pixel high output character."

    for i in range(10):
        res = sparklines([i])
        exp = ['▄']
        assert res == exp


def test_empty():
    "Make sure degenerate cases don't fail"
    res = sparklines([])
    exp = ['']
    # Produces an empty line from the command line
    #   we might prefer empty output
    assert res == exp


def test_multiline():
    res = sparklines([1, 5, 8], num_lines=3)
    exp = [
        "  █",
        " ▆█",
        "▁██"]
    assert res == exp


def test_wrap():
    res = sparklines([1,2, 3, 1, 2, 3, 1, 2], wrap=3)
    exp = ["▁▄█", "", "▁▄█", "", "▁▄", ""]
    assert res == exp
