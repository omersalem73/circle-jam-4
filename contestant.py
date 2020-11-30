from random import random, choice

from question import Question
from question_data import QuestionDifficulty


class Contestant:

    def __init__(self):
        self._answer_prob = {
            QuestionDifficulty.HARD: 0.3,
            QuestionDifficulty.AVERAGE: 0.7,
            QuestionDifficulty.EASY: 0.86
        }

    def answer(self, question: Question):
        correct_answer = question.get_correct_answer()
        wrong_answers = question.get_wrong_answers()

        if random() <= self._answer_prob[question.question_data.difficulty]:
            correct_answer.select()
        else:
            choice(wrong_answers).select()

