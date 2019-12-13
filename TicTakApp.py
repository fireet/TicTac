from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

from itertools import product

from kivy.uix.modalview import ModalView


class GameButton(Button):
    coordinate = ListProperty([0, 0])


class GameGrid(GridLayout):
    result = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    player = NumericProperty(1)

    def __init__(self):
        super().__init__()

        for row, column in product(range(3), range(3)):
            game_button = GameButton(coordinate=(row, column))
            game_button.bind(on_release=self.press_button)
            self.add_widget(game_button)

    def press_button(self, button):
        players = {
            1: 'X',
            -1: '0'
        }
        color = {
            1: (1, 0, 0, 1),
            -1: (0, 1, 0, 1)
        }

        row, column = button.coordinate
        index = 3 * row + column

        self.play_now = self.result[index]

        if not self.play_now:
            self.result[index] = self.player
            button.text = players[self.player]
            button.background_color = color[self.player]
            self.player *= -1

        self.on_status()

    def on_status(self):

        status = self.result

        wins = [sum(status[0:3]),
                sum(status[3:6]),
                sum(status[6:9]),
                sum(status[0::3]),
                sum(status[1::3]),
                sum(status[2::3]),
                sum(status[::4]),
                sum(status[2:-2:2])
                ]

        winner = ''

        if 3 in wins:
            winner = 'X - wins'
        elif -3 in wins:
            winner = '0 - wins'
        elif 0 not in self.result:
            winner = 'Draw'

        if winner:
            popup = ModalView(size_hint=(0.75, 0.5))
            victory_label = Label(text=winner, font_size=30)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset_game)
            popup.open()

    def reset_game(self, *args):
        self.result = [0 for _ in range(9)]
        for child in self.children:
            child.text = ''
            child.background_color = (1, 1, 1, 1)

        self.player = 1


class BaseBox(BoxLayout):
    def __init__(self):
        super().__init__()

        self.add_widget(GameGrid())


class GameApp(App):
    def build(self):
        return BaseBox()


if __name__ == '__main__':
    GameApp().run()
