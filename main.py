import arcade


class Budget:

    def __init__(self):
        self._val = 100000

    def on_draw(self):
        arcade.draw_text("Budget: ${}".format(self._val), 10, 710, arcade.color.WHITE, 26,
                         anchor_x='left', anchor_y='top')


class Rating:

    def __init__(self):
        self._val = 12.7

    def on_draw(self):
        arcade.draw_text('Rating: {}%'.format(self._val), 10, 680, arcade.color.WHITE, 26,
                         anchor_x='left', anchor_y='top')


def is_point_in_rect(x, y, rx, ry, rw, rh):
    return (x >= rx) and (x <= rx + rw) and (y >= ry) and (y <= ry + rh)


class PossibleAnswer:

    def __init__(self, tile_x, tile_y, text):
        self._tile_x = tile_x
        self._tile_y = tile_y
        self._text = text
        self._color = arcade.color.RED

    def select(self):
        self._color = arcade.color.YELLOW

    def unselect(self):
        self._color = arcade.color.RED

    def is_selected(self):
        return self._color == arcade.color.YELLOW

    def on_draw(self):
        arcade.draw_rectangle_filled(300 + 600 * self._tile_x, 40 + 80 * self._tile_y, 600, 80, self._color)
        arcade.draw_text(self._text, 300 + 600 * self._tile_x, 40 + 80 * self._tile_y, arcade.color.WHITE, 26,
                         anchor_x='center')

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if is_point_in_rect(x, y, 600 * self._tile_x, 80 * self._tile_y, 600, 80):
                self.select()


class Question:

    def __init__(self, question='', correct_answer='', three_wrong_answers=None):
        self._question = question
        if not three_wrong_answers:
            three_wrong_answers = ['', '', '']
        self._possible_answers = [
            PossibleAnswer(0, 0, correct_answer),
            PossibleAnswer(1, 0, three_wrong_answers[0]),
            PossibleAnswer(0, 1, three_wrong_answers[1]),
            PossibleAnswer(1, 1, three_wrong_answers[2])
        ]

    @property
    def text(self):
        return self._question

    def on_draw(self):
        arcade.draw_rectangle_filled(600, 40 + 80 * 2, 600, 80, arcade.color.BLUE)
        arcade.draw_text(self._question, 600, 40 + 80 * 2, arcade.color.WHITE, 26,
                         anchor_x='center')
        for answer in self._possible_answers:
            answer.on_draw()

    def _get_current_selected_answer(self):
        for answer in self._possible_answers:
            if answer.is_selected():
                return answer

    def on_mouse_press(self, x, y, button, modifiers):
        selected_answer = self._get_current_selected_answer()
        if selected_answer:
            selected_answer.unselect()
        for answer in self._possible_answers:
            answer.on_mouse_press(x, y, button, modifiers)
        new_selected_answer = self._get_current_selected_answer()

        if selected_answer and (not new_selected_answer):
            selected_answer.select()


class Levels:

    def __init__(self):
        self._selected_level = 2

    def next_level(self):
        self._selected_level += 1

    def on_draw(self):
        for i in range(5):
            if i == self._selected_level:
                arcade.draw_rectangle_filled(100, 415 + 50 * i, 200, 40, arcade.color.ORANGE)
            arcade.draw_text('${}'.format(10 ** (i + 3)), 20, 400 + 50 * i, arcade.color.WHITE, 26,
                             anchor_x='left')


class QuestionsPool:

    def __init__(self, questions):
        self._questions = questions
        self._show_highlight = False
        self._highlighted_index = 0
        self._selected_question = None

    def on_draw(self):
        if self._show_highlight:
            arcade.draw_rectangle_filled(600, 415 + 40 * self._highlighted_index, 300, 35, arcade.color.ORANGE)
        for i, question in enumerate(self._questions):
            arcade.draw_text(question.text, 600, 400 + 40 * i, arcade.color.WHITE, 26,
                             anchor_x='center')

    def on_mouse_motion(self, x, y, dx, dy):
        self._show_highlight = False
        for i, question in enumerate(self._questions):
            if is_point_in_rect(x, y, 450, 400 + 40 * i, 300, 40):
                self._show_highlight = True
                self._highlighted_index = i

    @property
    def selected_question(self):
        return self._selected_question

    def on_mouse_press(self, x, y, button, modifiers):
        if (button == arcade.MOUSE_BUTTON_LEFT) and self._show_highlight:
            self._selected_question = self._questions[self._highlighted_index]


class Game(arcade.Window):

    def __init__(self):
        super().__init__(1200, 720)
        self._budget = Budget()
        self._rating = Rating()
        self._on_scree_question = Question()
        self._questions_pool = QuestionsPool([
            Question('Who has the biggest?', 'Omer', ['Shoded', 'Omri', 'Gonen']),
            Question('Who has the longest?', 'Omer', ['Shoded', 'Omri', 'Gonen']),
            Question('Who has the hardest?', 'Omer', ['Shoded', 'Omri', 'Gonen'])
        ])
        self._levels = Levels()

    def on_draw(self):
        arcade.start_render()
        self._budget.on_draw()
        self._rating.on_draw()
        self._questions_pool.on_draw()
        self._on_scree_question.on_draw()
        self._levels.on_draw()

    def on_mouse_press(self, x, y, button, modifiers):
        selected_question = self._questions_pool.selected_question
        self._questions_pool.on_mouse_press(x, y, button, modifiers)
        new_selected_question = self._questions_pool.selected_question

        if new_selected_question != selected_question:
            self._on_scree_question = new_selected_question

        self._on_scree_question.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self._questions_pool.on_mouse_motion(x, y, dx, dy)


def main():
    Game()
    arcade.run()


if __name__ == '__main__':
    main()
