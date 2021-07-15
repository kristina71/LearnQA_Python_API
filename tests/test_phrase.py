import pytest

from lib.base_case import BaseCase


class TestPhrase(BaseCase):
    def test_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "Test phrase should be less than 15 symbols"
