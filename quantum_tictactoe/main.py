from quantum_tictactoe.form import Ui_main
from quantum_tictactoe.game import InvalidMoveError, InvalidCollapseError, BotTypeError
from quantum_tictactoe.game import Tile, Bot, Board, Game
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import sys


class Ui_main_my(Ui_main):
    def __init__(self, main):
        super().__init__()
        super().setupUi(main)
        tiles = []
        for _ in range(9):
            tiles.append(Tile())
        self.myboard = Board(tiles)
        self.game = Game(self.myboard)
        self.bot_mode = ''
        self.last_clicked = None
        self.info.setText('Choose mode on top bar. If you are in game, choosing mode will clear board and start new game')
        self.buttons = [self.Button1_1, self.Button1_2, self.Button1_3,
                        self.Button2_1, self.Button2_2, self.Button2_3,
                        self.Button3_1, self.Button3_2, self.Button3_3]
        self.coll_buttons = [self.collButton1, self.collButton2, self.collButton3,
                             self.collButton4, self.collButton5, self.collButton6,
                             self.collButton7, self.collButton8, self.collButton9,
                             self.collButton10]
        self.action_buttons = [self.actionNone, self.actionEasy, self.actionHard]
        for button in self.buttons:
            button.clicked.connect(partial(self.button_click, button))
        for button in self.coll_buttons:
            button.clicked.connect(partial(self.coll_button_click, button))
        for action in self.action_buttons:
            action.triggered.connect(partial(self.mode_click, action))

    def button_click(self, button):
        """
        Makes move on clicked button
        or when game is in entanglement
        shows possible moves to collapse
        """
        if self.could_move():
            try:
                self.place_move(button)
            except InvalidMoveError as err:
                self.info.setText(str(err))
        if self.bot_mode != 'none' and 'x' in self.game.last_move():
            self.bot_move()
        if self.game.entanglement:
            self.clear_coll_buttons()
            player = 'X' if 'y' in self.game.last_move() else 'Y'
            mess = f'Game is in entanglement. Player {player} must choose which move will collapse.'
            self.info.setText(mess)
            self.makes_buttons_entangl()
            self.show_collapsion(button)
        self.last_clicked = button

    def makes_buttons_entangl(self):
        """
        Add * to buttons in entanglement
        """
        for num in self.game.board.entangl_tiles():
            text = self.buttons[num].text()
            if '*' not in text:
                text += '*'
                self.buttons[num].setText(text)

    def show_collapsion(self, button):
        """
        Show moves which are in button on coll_buttons
        """
        button_text = button.text()
        button_text = button_text.replace('\n', ', ')
        moves = button_text.split(', ')
        for index, move in enumerate(moves):
            if '*' in move:
                move = move[:-1]
            if 'x' in move or 'y' in move:
                self.coll_buttons[index].setVisible(True)
                self.coll_buttons[index].setEnabled(True)
                self.coll_buttons[index].setText(str(move))

    def bot_move(self):
        """
        Checks game state and run right bot script
        """
        if self.game.entanglement:
            self.game.game_collapse(self.bot, self.bot_mode)
            self.refresh_buttons_text()
            self.game.board.reset_entangl_tiles()
        if self.game.is_game_end():
            self.info.setText(str(self.game.game_result()))
            self.refresh_buttons_text()
        elif self.game.basic:
            moves = self.bot.move()
            move = self.game.whos_move()
            for tile in moves:
                text = self.buttons[tile].text()
                text = self.add_move_to_text(text, move)
                self.buttons[tile].setText(text)
            self.game.set_last_tile(moves[1])
            self.game.set_last_move(move)
            self.game.increase_counter()
            self.game.game_entanglement()
            self.info.setText('Your turn X')

    def place_move(self, button):
        """
        Appends move to tile/button
        Change game state
        """
        text = button.text()
        move = self.game.whos_move()
        text = self.add_move_to_text(text, move)
        for index, butt in enumerate(self.buttons):
            if butt == button:
                if self.game.is_first_move():
                    self.game.move(index)
                    self.game.set_first_move(False)
                else:
                    self.game.move(index)
                    self.game.set_last_move(move)
                    self.game.increase_counter()
                    self.game.set_first_move(True)
                    self.whos_turn()
                    self.game.game_entanglement()
        button.setText(text)

    def add_move_to_text(self, text, move):
        """
        Appends move to text and returns text
        """
        if text == '':
            text += move
        elif len(text) == 14:
            text += '\n' + move
        else:
            text += ', ' + move
        return text

    def could_move(self):
        """
        Checks if players could set moves.
        Returns true or false
        """
        if self.game.basic and self.bot_mode != '' and not self.game.is_finished():
            return True
        else:
            return False

    def coll_button_click(self, button):
        """
        Collapses move which is on clicked button
        """
        try:
            collapse = self.to_collapse(button)
            if 'x' not in self.game.last_move() or self.bot_mode == 'none':
                self.game.game_collapse(self.bot, self.bot_mode, collapse)
            self.refresh_buttons_text()
            self.game.board.reset_entangl_tiles()
            self.clear_coll_buttons()
            if self.game.is_game_end():
                self.game.set_finished()
                self.info.setText(str(self.game.game_result()))
                self.refresh_buttons_text()
            else:
                self.whos_turn()
        except InvalidCollapseError as err:
            self.info.setText(str(err))

    def whos_turn(self):
        """
        Sets info about which player can move now on self.info
        """
        player = 'X' if 'y' in self.game.last_move() else 'Y'
        text = f'Your turn {player}'
        self.info.setText(text)

    def refresh_buttons_text(self):
        """
        Refresh text on tiles
        """
        for index, butt in enumerate(self.buttons):
            array = self.game.board.tiles()[index].array()
            text = ''
            for move in array:
                if move != array[0]:
                    text += ', ' + move
                else:
                    text += move
            butt.setText(str(text))
            self.change_color(index, butt)

    def change_color(self, index, button):
        """
        Changes styleSheet on button when button is collapsed
        """
        if self.game.is_finished() and index in self.game.board.is_winner()[1]:
            style = "background-color: rgb(220,20,60);\nfont: 10pt \"MS Shell Dlg 2\";"
            button.setStyleSheet(style)
        else:
            if self.game.board.tiles()[index].is_collapsed():
                style = "background-color: rgb(32,178,170);\nfont: 10pt \"MS Shell Dlg 2\";"
                button.setStyleSheet(style)
            else:
                style = "background-color: rgb(0, 85, 255);\ncolor: rgb(255, 255, 255);\nfont: 10pt \"MS Shell Dlg 2\";"
                button.setStyleSheet(style)

    def to_collapse(self, button):
        """
        Search for button which was last clicked.
        Returns index of this button and text on coll_button.
        """
        for index, butt in enumerate(self.buttons):
            if butt == self.last_clicked:
                collapse = str(index) + ',' + button.text()
        return collapse

    def mode_click(self, action):
        """
        Changes bot mode and create bot.
        """
        self.clear_game()
        if action == self.actionNone:
            self.bot_mode = 'none'
        elif action == self.actionEasy:
            self.bot_mode = 'easy'
        elif action == self.actionHard:
            self.bot_mode = 'hard'
        try:
            self.bot = Bot(self.bot_mode, self.myboard, self.game)
            self.info.setText('Your turn X')
        except BotTypeError as err:
            self.info.setText(str(err))

    def clear_game(self):
        """
        Clear board and window
        """
        self.game.clear_game()
        self.clear_coll_buttons()
        self.refresh_buttons_text()

    def clear_coll_buttons(self):
        """
        Returns coll_buttons to default state
        """
        for coll_butt in self.coll_buttons:
            coll_butt.setVisible(False)
            coll_butt.setEnabled(False)
            coll_butt.setText('')


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    ui = Ui_main_my(main)
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
