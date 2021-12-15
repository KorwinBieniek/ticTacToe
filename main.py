# 1) Dziel kod na mniejsze częśći, które można uruchomić bezpośrednio.

# 2) Interaktywne podejście  (dobrze zgrywa z oddolnym podejściem)

# 3) Eliminacja Magic Values

# todo rozbić funkcje na mniejsze
# todo zweryfikować funkcję select_player
# todo zweryfikować funkcję open file
# todo stworzyć funkcję pozwalającą testować planszę na konkretnych etapach gier -> testy jednostkowe
# todo usunąć magic numbers
# todo rozbić funkcje menu(), start() turns_navigation()
# todo zakaz wpisywania ujemnych wartości aby postawić znak na planszy
# todo podzielić funkcję check_sign_placement
# todo dodać elastyczność, aby plansza mogła przyjąć dowolne wymiary


# TicTacToe by Korwin Bieniek
import random

# magic values

CROSS_SYMBOL = 'X'
CIRCLE_SYMBOL = 'O'


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
    a_file = open("replay.txt")  # doc
    # with open('replay.txt', 'a') as file_open:
    lines_to_read = [turn_num - 3, turn_num - 2, turn_num - 1]  # indeksy
    for position, line in enumerate(a_file):
        if position in lines_to_read:
            print(line)


def print_board(board):
    for row in board:
        print(row)


print_board([
    ['X', 'O', '_'],
    ['X', 'O', '_'],
    ['X', 'O', '_']
])

print_board([
    ['X', 'O', '_'],
    ['_', 'O', 'X'],
    ['X', 'O', '_']
])


class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def check_rows(self, win, player, board_length):
        for i in range(board_length):
            for j in range(board_length):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

    def check_columns(self, win, player, board_length):
        for i in range(board_length):
            for j in range(board_length):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

    def check_diagonals(self, win, player, board_length):
        for i in range(board_length):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        for i in range(board_length):
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
        row, col = list(
            map(int, input('Enter row and column numbers to fix spot: ').split()))
        print()
        if self.board[row - 1][col - 1] != '-':
            print("This place is already taken, try another one")
            return False
        else:
            self.fix_spot(row - 1, col - 1, player)
            self.save_file()
            return True

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

    def start(self):
        with open('replay.txt', 'w'):
            self.board = []
            self.create_board()
            self.save_file()  # save empty board

            if select_player() == 1:
                player = 'X'
            else:
                player = 'O'

            while True:
                print(f'Player {player} turn:')

                self.show_board()

                good_placement = False
                while not good_placement:
                    try:
                        good_placement = self.check_sign_placement(player)
                    except IndexError:
                        print("Input a number between 1 and 3")
                        good_placement = False
                        player = player
                    except ValueError:
                        print("Input two numbers separated by space")
                        good_placement = False

                if self.is_win(player):
                    print(f'Player {player} won the game!')
                    break

                if self.is_draw():
                    print("It's a draw!")
                    break

                player = swap_player(player)

            print()
            self.show_board()


def menu():
    answer = 't'
    while answer == 't':
        tic_tac_toe.start()
        menu_message = 'Please enter \'t\' - to start again, \'q\' - to quit the game or \'r\' to see the replay of the last game: '
        answer = input(menu_message)

        while answer != 'q' and answer != 't' and answer != 'r':
            answer = input(menu_message)
    if answer == 'r':
        turns_navigation()
    if answer == 'q':
        exit(0)


def turns_navigation():
    turn = 3
    load_file(turn)
    while True:
        turn_choice = input('To see the next turn enter \'d\''
                            ', to see the previous turn enter \'c\','
                            'to quit enter \'q\': ')
        if turn_choice == 'd':
            turn += 3
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
                turn -= 3

        elif turn_choice == 'c':
            if turn == 3:
                print("This is the first turn, you can't go back anymore")
            else:
                turn -= 3
                load_file(turn)
        elif turn_choice == 'q':
            exit()


if __name__ == '__main__':
    tic_tac_toe = TicTacToe()
    menu()
