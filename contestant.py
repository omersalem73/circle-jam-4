from globals import get_game
from random import random, choice


class Contestant:

    def __init__(self, chance_of_answer_correct=0.9):
        self._chance_of_answer_correct = chance_of_answer_correct

    def answer(self):
        correct_answer = get_game().on_screen_question.get_correct_answer()
        wrong_answers = get_game().on_screen_question.get_wrong_answers()

        if random() <= self._chance_of_answer_correct:
            correct_answer.select()
        else:
            choice(wrong_answers).select()

        get_game().on_screen_question.verify_answered_question()
