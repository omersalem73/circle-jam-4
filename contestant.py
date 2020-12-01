from random import random, choice

from globals import get_game
from question import Question
from question_data import QuestionDifficulty


class Contestant:

    def __init__(self):
        self._answer_prob = {
            QuestionDifficulty.HARD: 0.3,
            QuestionDifficulty.AVERAGE: 0.7,
            QuestionDifficulty.EASY: 0.86
        }
        self._prize_to_quit_prob = {
            1000: 1,
            32000: 0.7
        }

    def answer(self, question: Question):
        correct_answer = question.get_correct_answer()
        wrong_answers = question.get_wrong_answers()

        if random() <= self._answer_prob[question.question_data.difficulty]:
            correct_answer.select()
        else:
            choice(wrong_answers).select()

    def consider_quitting(self):
        questions_stages = get_game().questions_stages
        # at present only consider quitting if just hit the exit point, not afterwards
        if questions_stages.is_currently_on_exit_point():
            if random() <= self._prize_to_quit_prob[questions_stages.current_exit_money()]:
                return True
        return False
