# TicTacToe by Korwin Bieniek
import random

'''Założenia: Kółko i krzyżyk te same zasady co zwykle z tym, że: - dbamy o to, aby program był przyjazny dla 
użytkownika (nie odpuści, gdy dane od użytkownika są złe, program będzie pytał użytkownika aż ten poda nam dobry 
wynik) - dbamy o to, aby w programie nie było błędów, dążyć do tego, by jak największa część kodu została sprawdzona 
- (opcjonalnie) jak wyjdzie Panu wersja podstawowa to proszę utworzyć nowy plik i w nim rozszerzyć grę o to, 
aby użytkownik mógł ponowić grę po ukończeniu rozgrywki (pytanie i odpowiedź t/n) - (opcjonalnie) jak wyjdzie Panu 
wersja poprzednia to proszę utworzyć nowy plik i dodać w nim możliwość zapamiętywania historii przebiegu gry. Tutaj 
jak użytkownik ukończy rozgrywkę to otrzymuje pytanie czy chce przejrzeć grę, jeśli wciśnie T (od tak) wówczas rysuje 
mu się na początku pusta plansza, a potem użytkownik ma dwie opcje D) od dalej, i C) od cofnij. Obie opcje mają wpływ 
na przeglądanie historii. Kliknięcie D powoduje pokazanie stanu gry o jeden ruch dalej, klikać w D można aż do 
momentu ukończenia gry. Natomiast C powoduje, że cofamy się o 1 ruch, klikać w C można do momentu gdy plansza pokaże 
się pusta. 
        
'''


def swap_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'


def select_player():
    return random.randint(0, 1)


def load_file(turn_num):
    a_file = open("replay.txt")
    lines_to_read = [turn_num - 3, turn_num - 2, turn_num - 1]
    for position, line in enumerate(a_file):
        if position in lines_to_read:
            print(line)


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

    def is_win(self, player):
        # checking rows
        n = len(self.board)
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
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

    def start(self):
        open('replay.txt', 'w')
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


if __name__ == '__main__':
    tic_tac_toe = TicTacToe()
    answer = 't'
    while answer == 't':
        tic_tac_toe.start()
        answer = input('Please enter \'t\' - to start again'
                       ', \'n\' - to quit the game'
                       ' or \'r\' to see the replay of the last game: ')

        while answer != 'n' and answer != 't' and answer != 'r':
            answer = input('Please enter \'t\' - to start again'
                           ', \'n\' - to quit the game'
                           ' or \'r\' to see the replay of the last game: ')
    if answer == 'r':
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
                exit(0)
