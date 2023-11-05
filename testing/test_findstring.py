
import findstring
import pytest

def test_ispresent():
    assert findstring.ispresent('al')

def test_nodigit():
    assert findstring.nodigit('')