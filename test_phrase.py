import pytest

class TestPhrase:
    def test_phrase(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "Test phrase should be less than 15 symbols"
