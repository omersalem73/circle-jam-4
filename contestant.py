from random import random, choice

from globals import get_game
from question import Question


class Contestant:

    def __init__(self, name, answer_prob, prize_to_quit_prob):
        self._name = name
        self._answer_prob = answer_prob
        self._prize_to_quit_prob = prize_to_quit_prob

    @property
    def name(self):
        return self._name

    @property
    def answer_prob(self):
        return self._answer_prob

    @property
    def prize_to_quit_prob(self):
        return self._prize_to_quit_prob

    def answer(self, question: Question):
        correct_answer = question.get_correct_answer()
        wrong_answers = question.get_wrong_answers()

        if random() <= self._answer_prob[question.question_data.difficulty]:
            correct_answer.select()
        else:
            choice(wrong_answers).select()

    def should_withdraw(self):
        questions_stages = get_game().questions_stages
        # at present only consider quitting if just hit the exit point, not afterwards
        if questions_stages.is_currently_on_exit_point():
            if random() <= self._prize_to_quit_prob[questions_stages.get_current_exit_money()]:
                return True
        return False
