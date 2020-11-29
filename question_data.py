class QuestionData:

    def __init__(self, text, correct_answer, three_wrong_answers):
        self._text = text
        self._correct_answer = correct_answer
        self._three_wrong_answers = three_wrong_answers

    @property
    def text(self):
        return self._text

    @property
    def correct_answer(self):
        return self._correct_answer

    @property
    def three_wrong_answers(self):
        return self._three_wrong_answers
