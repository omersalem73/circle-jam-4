from enum import Enum
import typing


class QuestionDifficulty(Enum):
    EASY = 'Easy'
    AVERAGE = 'Average'
    HARD = 'Hard'


class QuestionData:

    def __init__(self, text: str, correct_answer: str, three_wrong_answers: typing.List[str],
                 difficulty: QuestionDifficulty):
        self._text = f'{text} ({difficulty.value})'
        self._correct_answer = correct_answer
        self._three_wrong_answers = three_wrong_answers
        self._difficulty = difficulty

    @property
    def difficulty(self) -> QuestionDifficulty:
        return self._difficulty

    @property
    def text(self):
        return self._text

    @property
    def correct_answer(self):
        return self._correct_answer

    @property
    def three_wrong_answers(self):
        return self._three_wrong_answers
