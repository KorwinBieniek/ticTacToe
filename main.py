# 1) Dziel kod na mniejsze częśći, które można uruchomić bezpośrednio.

# 2) Interaktywne podejście  (dobrze zgrywa z oddolnym podejściem)

# 3) Eliminacja Magic Values

# todo zweryfikować funkcję select_player


# TicTacToe by Korwin Bieniek
import random

# custom exceptions
from AlreadyTakenSpotError import AlreadyTakenSpotError
from NegativePlacementError import NegativePlacementError

CROSS_SYMBOL = 'X'
CIRCLE_SYMBOL = 'O'
board_size = int(input('Input the size of the board: '))


def swap_player(player):
    if player == CROSS_SYMBOL:
        return CIRCLE_SYMBOL
    return CROSS_SYMBOL


# !!!
def select_player():
    return random.randint(0, 1)


# dir, file, id

# HASŁO DNIA: parsowanie

# "(2+2)*3" ->
# tekst -----> wyodrębnienie wartości wygodnych w użycia z poziomu pythona

# load_file -> można podkręcić values[2:2+3]
# warto rozważyć podział na drobniejsze akcje (wczytanie, parsowanie
def load_file(turn_num):
    replay_file = open("replay.txt")  # doc

    amount_of_lines = 3  # amount of lines we want to print
    parse_file(turn_num, replay_file, amount_of_lines)

    replay_file.close()


def parse_file(turn_num, file, amount_of_lines):
    lines_to_read = [turn_num - amount_of_lines, turn_num - amount_of_lines + 1,
                     turn_num - amount_of_lines + 2]  # indeksy
    for position, line in enumerate(file):
        if position in lines_to_read:
            print(line)


def print_board(board):
    for row in board:
        print(row)


class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append('-')
            self.board.append(row)
        return board_size

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def check_rows(self, win, player, board_length):
        for i in range(board_length):
            win = True
            for j in range(board_length):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

    def check_columns(self, win, player, board_length):
        for i in range(board_length):
            win = True
            for j in range(board_length):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

    def check_diagonals(self, win, player, board_length):
        for i in range(board_length):
            win = True
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        for i in range(board_length):
            win = True
            if self.board[i][board_length - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

    def is_win(self, player):
        if self.check_rows(True, player, len(self.board)) \
                or self.check_columns(True, player, len(self.board)) \
                or self.check_diagonals(True, player, len(self.board)):
            return True
        else:
            return False

    def is_draw(self):
        for row in self.board:
            for place in row:
                if place == '-':
                    return False
        return True

    def show_board(self):
        for row in self.board:
            for place in row:
                print(place, end=" ")
            print()

    def check_sign_placement(self, player):
        good_placement = False
        while not good_placement:
            try:
                row, col = list(
                    map(int, input('Enter row and column numbers to fix spot: ').split()))
                print()
                if row < 0 or col < 0:
                    raise NegativePlacementError
                elif self.board[row - 1][col - 1] != '-':
                    raise AlreadyTakenSpotError
                else:
                    self.fix_spot(row - 1, col - 1, player)
                    self.save_file()
                    good_placement = True
            except AlreadyTakenSpotError:
                print('This place is already taken, try another one')
                good_placement = False
            except NegativePlacementError:
                print('Input a positive number')
                good_placement = False
            except IndexError:
                print('Input a number between 1 and 3')
                good_placement = False
            except ValueError:
                print('Input two numbers separated by space')
                good_placement = False

    def save_file(self):
        with open('replay.txt', 'a') as file_open:
            for item in self.board:
                file_open.write("%s\n" % item)

    # TO ROBI WITH+PLIK POD SPODEM:
    # def save_file(self):
    #     file_open = open('replay.txt', 'a')
    #     try:
    #         for item in self.board:
    #             file_open.write("%s\n" % item)
    #     finally:
    #         file_open.close()

    def randomize_player(self):
        if select_player() == 1:
            return CROSS_SYMBOL
        else:
            return CIRCLE_SYMBOL

    def start(self):
        clear_file = open('replay.txt', 'w')
        self.board = []
        self.create_board()
        self.save_file()  # save empty board

        player = self.randomize_player()

        while True:
            print(f'Player {player} turn:')

            self.show_board()

            self.check_sign_placement(player)

            if self.is_win(player):
                print(f'Player {player} won the game!')
                break

            if self.is_draw():
                print("It's a draw!")
                break

            player = swap_player(player)

        print()
        self.show_board()
        clear_file.close()

    def verify_functionality(self, board):

        self.board = board

        if self.is_draw():
            print("It's a draw!")
        elif self.is_win(CROSS_SYMBOL):
            print(f'Player {CROSS_SYMBOL} won the game!')
        elif self.is_win(CIRCLE_SYMBOL):
            print(f'Player {CIRCLE_SYMBOL} won the game!')
        else:
            print("Game is still running")


def menu():
    answer = 't'
    while answer == 't':
        tic_tac_toe.start()
        menu_message = 'Please enter \'t\' - to start again, \'r\' to see the replay of the last game or \'q\' - to quit the game: '
        answer = input(menu_message)

        while answer != 'q' and answer != 't' and answer != 'r':
            answer = input(menu_message)
    if answer == 'r':
        turns_navigation()
    if answer == 'q':
        exit(0)


def turns_navigation():
    turn = board_size
    load_file(turn)
    while True:
        turn_choice = input('To see the next turn enter \'d\''
                            ', to see the previous turn enter \'c\','
                            'to quit enter \'q\': ')
        if turn_choice == 'd':
            turn += board_size
            end_of_file = 0

            with open('replay.txt', 'r') as file_open:
                while True:
                    file_eof = file_open.readline()
                    end_of_file += 1
                    if file_eof == '':
                        break
            if turn < end_of_file:

                load_file(turn)
            else:
                print("This was the last move")
                turn -= board_size

        elif turn_choice == 'c':
            if turn == board_size:
                print("This is the first turn, you can't go back anymore")
            else:
                turn -= board_size
                load_file(turn)
        elif turn_choice == 'q':
            exit()


if __name__ == '__main__':
    tic_tac_toe = TicTacToe()
    menu()
    tic_tac_toe.verify_functionality([
        ['X', 'O', '-'],
        ['X', 'O', '-'],
        ['X', 'O', '-']
    ])

    tic_tac_toe.verify_functionality([
        ['X', 'O', '-'],
        ['-', 'O', 'X'],
        ['X', 'O', '-']
    ])

    tic_tac_toe.verify_functionality([
        ['X', '-', 'O'],
        ['-', '-', 'O'],
        ['X', '-', 'O']
    ])

    tic_tac_toe.verify_functionality([
        ['X', '-', '-'],
        ['O', 'O', 'O'],
        ['X', 'O', '-']
    ])

    tic_tac_toe.verify_functionality([
        ['X', 'O', '-'],
        ['-', 'O', 'O'],
        ['X', 'X', 'X']
    ])

    tic_tac_toe.verify_functionality([
        ['X', 'O', '-'],
        ['-', 'X', 'O'],
        ['O', 'O', 'X']
    ])

    tic_tac_toe.verify_functionality([
        ['X', 'X', 'X'],
        ['-', 'O', 'X'],
        ['O', 'O', '-']
    ])

    tic_tac_toe.verify_functionality([
        ['X', 'X', 'O'],
        ['-', 'O', 'X'],
        ['O', 'O', '-']
    ])
