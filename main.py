# '''class MenuAction:

#     def run(self):
#         pass


# class StartGame(MenuAction):

#     def run(self):
#         print('właśnie uruchamiam grę')


# # S(O)LID - otwarte na rozszerzenia, zamknięte na modyfikacje / rób program tak, aby dało się do niego włącząć nowe zmiany jako pluginy
# menu = Menu()
# menu.add_option('t', StartGame())
# # menu.add_option('d', download_file)
# menu.add_option('r', ReplayGame())
# menu.add_option('q', QuitGame())
# menu.add_option('d', DownloadAddon())
# menu.run()

'''
class Option:

    def run(self):
        raise NotImplementedError()


class StartSomething(Option):

    def run(self):
        # ...
        print('uruchamiam coś')


class ExportData(Option):

    def run(self):
        print('eksportuje dane')


class AboutPrinter(Option):

    def __init__(self, version):
        self._version = version

    def run(self):
        print(' Version:', self._version)


# Relacja JEST (dziedziczeniu)

# Relacja MA (kompozycja)


class Menu:

    def __init__(self):
        self.options = [
            StartSomething(),
            ExportData(),
            AboutPrinter(),
            ...
        ]


#     def add_option(self, option):
#         self.options.append(option)


class ConsoleMenu:

    def __init__(self, options=None, names=None):
        # self.options = options or []
        self._options = options
        if type(self._options) == type(None):  # NoneType
            self._options = []

        self._names = names
        if type(self._names) == type(None):  # NoneType
            self._names = []

        if len(self._names) != len(self._options):
            raise ValueError('Invalid count of names or options')

    def add_option(self, option, name):
        self._options.append(option)
        self._names.append(name)

    def run(self):
        if len(self._options) == 0:
            raise ValueError()
        self._print_options()
        index = self._get_option_index_from_user()
        option = self._options[index]
        option.run()

    def _print_options(self):
        n = 1
        for option_name in self._names:
            print(n, option_name)
            n += 1

    def _get_option_index_from_user(self):
        choice = int(input('> '))
        # !!! - uwaga na litery zamiast liczb
        # !!! - uwaga na wielkość liczby (powinna być zgodna z opcjami)
        # !!! - w sytuacji gdy user popełni błąd, powtórz (while?)
        return choice - 1


m1 = ConsoleMenu()
m1.add_option(ExportData(), 'Ekportuj dane')
m1.add_option(AboutPrinter(1), 'O programie')
m1.run()

en_menu = ConsoleMenu()
en_menu.add_option(ExportData(), 'Ekportuj dane')
en_menu.add_option(AboutPrinter(1), 'O programie')
en_menu.run()
'''

# 1. Zrób coś
# 2. Eksportuj
# 3. O programie
# > 2
#
# m2 = Menu([StartSomething()])
# m2.add_option(ExportData())
#
# # 1) Dziel kod na mniejsze częśći, które można uruchomić bezpośrednio.
#
# # 2) Interaktywne podejście  (dobrze zgrywa z oddolnym podejściem)
#
# # 3) Eliminacja Magic Values
#
# TicTacToe by Korwin Bieniek
import random


# custom exceptions


class AlreadyTakenSpotError(Exception):
    """Raised when one of the indexes is already taken"""
    pass


class NegativePlacementError(Exception):
    """Raised when one of the indexes is negative"""
    pass


CROSS_SYMBOL = 'X'
CIRCLE_SYMBOL = 'O'
EMPTY_SYMBOL = '-'


def input_board_size():
    while True:
        try:
            size_of_board = int(input('Input the size of the board: '))
        except ValueError:
            print('Please enter a value')
            continue

        if size_of_board <= 1 or size_of_board > 10:
            print('The value has to be bigger than 1 and less than 11')
            continue
        return size_of_board


# !!! - uwaga, wywołanie funkcji jest OK pod sprawdzenie, ale nie jest dobre pod zmienną, by na niej teraz bazować
# board_size = input_board_size()  # the default board size
# board_size = 10


def swap_player(player):
    return CIRCLE_SYMBOL if player == CROSS_SYMBOL else CROSS_SYMBOL


# !!!
def rand_player():
    return random.choice([CROSS_SYMBOL, CIRCLE_SYMBOL])


# dir, file, id

# HASŁO DNIA: parsowanie

# "(2+2)*3" ->
# tekst -----> wyodrębnienie wartości wygodnych w użycia z poziomu pythona

# load_file -> można podkręcić values[2:2+3]
# warto rozważyć podział na drobniejsze akcje (wczytanie, parsowanie
def _check_lines(lines, board_size):
    # if len(lines) % board_size != 0:
    # raise ValueError('Invalid content')
    # for line in lines:
    #     size = len(line)
    #     size2 = len(line[0])
    #     if len(line) != board_size:
    #         raise ValueError('Invalid content line')
    pass


def _split_lines(text):
    all_lines = text.split('\n')
    filled_lines = []
    filled_lines.extend(
        cleaned_line for line in all_lines if (cleaned_line := line.strip())
    )

    return filled_lines


def parse_history(text, size_of_board):
    lines = _split_lines(text)
    _check_lines(lines, size_of_board)
    return [
        '\n'.join(lines[i : i + size_of_board])
        for i in range(0, len(lines), size_of_board)
    ]


def load_history(filename, size_of_board):
    with open(filename) as doc:
        content = doc.read()
    return parse_history(content, size_of_board)


def print_board(board):
    for row in board:
        print(row)


def _create_board(size):
    row = ['-' for _ in range(size)]
    return [row for _ in range(size)]


# DODAJMY (TROCHĘ PÓŹNIEJ)
# save_file(board) # !!!

class Board:

    def __init__(self, size):
        # _board -> nie wolno odwoływać się wprost z poza tej klasy
        self._board = _create_board(size)  # niedostępne dla innych

    def fix_spot(self, row_index, col_index, player):
        if row_index < 0 or col_index < 0:
            raise IndexError()
        elif self._board[row_index][col_index] != EMPTY_SYMBOL:
            raise AlreadyTakenSpotError()
        else:
            self._board[row_index][col_index] = player

    def __str__(self):
        s = ''
        for row in self.board:
            for place in row:
                s += place
            s += "\n"
        return s

    def is_win(self, player):
        return bool(self._check_rows(player, len(self._board)) \
                or self._check_columns(player, len(self._board)) \
                or self._check_diagonals(player, len(self._board)))

    def is_draw(self):
        for row in self.board:
            for place in row:
                if place == '-':
                    return False
        return True

    def _check_rows(self, player, board_length):
        for i in range(board_length):
            if win := all(self.board[i][j] == player for j in range(board_length)):
                return win

    def _check_columns(self, player, board_length):
        for i in range(board_length):
            if win := all(self.board[j][i] == player for j in range(board_length)):
                return win

    def _check_diagonals(self, player, board_length):
        win = True
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


#     def verify_functionality(self, board):

#         self.board = board

#         if self.is_draw():
#             print("It's a draw!")
#         elif self.is_win(CROSS_SYMBOL):
#             print(f'Player {CROSS_SYMBOL} won the game!')
#         elif self.is_win(CIRCLE_SYMBOL):
#             print(f'Player {CIRCLE_SYMBOL} won the game!')
#         else:
#             print("Game is still running")


def show_board(board):
    print(board)  # python pod spodem wywoła też str(board)


def save_file(board):
    with open('replay.txt', 'a') as file_open:
        file_open.write(str(board))


def check_sign_placement(player, board):
    while True:
        try:
            row, col = list(
                map(int, input('Enter row and column numbers to fix spot: ').split()))
            print()
            board.fix_spot(row_index=row - 1, col_index=col - 1, player=player)
            break
        except AlreadyTakenSpotError:
            print('This place is already taken, try another one')
            continue
        except NegativePlacementError:
            print('Input a positive number')
            continue
        except IndexError:
            print(f'Input a number between 1 and {len(board)}')
            continue
        except ValueError:
            print('Input two numbers separated by space')
            continue


# TO ROBI WITH+PLIK POD SPODEM:
# def save_file(self):
#     file_open = open('replay.txt', 'a')
#     try:
#         for item in self.board:
#             file_open.write("%s\n" % item)
#     finally:
#         file_open.close()

def start(board):
    with open('replay.txt', 'w') as clear_file:
        size = len(board.board)
        board.board = _create_board(size)
        save_file(board)  # save empty board

        player = rand_player()

        while True:
            print(f'Player {player} turn:')

            show_board(board)

            check_sign_placement(player, board)

            if board.is_win(player):
                print(f'Player {player} won the game!')
                break

            if board.is_draw():
                print("It's a draw!")
                break

            player = swap_player(player)

        print()
        show_board(board)


'''
class MenuAction:

    def run(self):
        pass


class StartGame(MenuAction):

    def run(self):
        print('właśnie uruchamiam grę')


# S(O)LID - otwarte na rozszerzenia, zamknięte na modyfikacje / rób program tak, aby dało się do niego włącząć nowe zmiany jako pluginy
menu = Menu()
menu.add_option('t', StartGame())
menu.add_option('r', ReplayGame())
menu.add_option('q', QuitGame())
menu.add_option('d', DownloadAddon())
# menu.run()
'''


def menu(board):
    answer = 't'

    board_size = input_board_size()

    menu_message = 'Please enter \'t\' - to start again, \'r\' to see the replay of the last game or \'q\' - to ' \
                   'quit the game: '
    while answer == 't':
        board = Board(board_size)
        start(board)
        answer = input(menu_message)

        while answer not in ['q', 't', 'r']:
            answer = input(menu_message)
    if answer == 'r':
        turns_navigation(board_size)
    if answer == 'q':
        exit(0)


def turns_navigation(size):
    turns = load_history('replay.txt', size)
    index = 0
    print(turns[0])  # print empty board
    while True:
        turn_choice = input('To see the next turn enter \'d\''
                            ', to see the previous turn enter \'c\','
                            'to quit enter \'q\': ')
        if turn_choice == 'd':
            if index + 1 > len(turns) - 2:
                print("This was the last move")
            else:
                index += 1
                print(turns[index])
            # end_of_file = 0
            #
            # with open('replay.txt', 'r') as file_open:
            #     while True:
            #         file_eof = file_open.readline()
            #         end_of_file += 1
            #         if file_eof == '':
            #             break
            # if turn < end_of_file:

            # turn -= board_size

        elif turn_choice == 'c':
            if index < 1:
                print("This is the first turn, you can't go back anymore")
            else:
                index -= 1
                print(turns[index])

                # else:
                #     turn -= board_size
        elif turn_choice == 'q':
            exit()


if __name__ == '__main__':
    menu()
