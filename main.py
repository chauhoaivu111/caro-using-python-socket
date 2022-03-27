import socket
import threading

class Caro:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = 'X'
        self.you = 'X'
        self.opponent = 'O'
        self.winner = None
        self.game_over = False

        # self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()

        self.you = 'X'
        self.opponent = 'O'

        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponent = 'X'
        threading.Thread(target=self.handle_connection, args=(client,)).start()


    def handle_connection(self, client):
        while not self.game_over:
            self.print_board()
            if self.turn == self.you:
                move = input('Enter <row-column>: ')
                if self.check_valid_move(move.split('-')):
                    self.apply_move(move.split('-'), self.you)
                    self.turn = not self.opponent
                    client.send(move.encode('utf-8'))
                else:
                    print('Invalid move!')
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.apply_move(data.decode('utf-8').split('-'), self.opponent)
                    self.turn = self.you
        client.close()

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won(move):
            if player == 'X':
                print('X won')
            else:
                print('O won')
        if self.winner == self.you:
            print('You win')
            exit()
        elif self.winner == self.opponent:
            print('You lose')
            exit()

    def check_valid_move(self, move) -> bool:
        return self.board[int(move[0])][int(move[1])] == ' '

    def check_if_won(self, move):
        if int(move[1]) < 4:
            for i in range(0, int(move[1]) + 1):
                if ''.join(self.board[int(move[0])][i:i + 5]) in ['XXXXX', 'OOOOO']:
                    return True
        elif int(move[1]) > 15:
            for i in range(19, int(move[1]) - 1, -1):
                if ''.join(self.board[int(move[0])][i - 4:i + 1]) in ['XXXXX', 'OOOOO']:
                    return True

        if int(move[0]) < 4:
            for i in range(0, int(move[0]) + 1):
                vertical = ''
                for j in range(i, i + 5):
                    vertical += self.board[j][int(move[1])]
                if vertical in ['XXXXX', 'OOOOO']:
                    return True
        elif int(move[0]) > 15:
            for i in range(19, int(move[0]) - 1, -1):
                vertical = ''
                for j in range(i, i - 5, -1):
                    vertical += self.board[j][int(move[1])]
                if vertical in ['XXXXX', 'OOOOO']:
                    return True

        # vertical
        for i in range(int(move[0]) - 4, int(move[0]) + 1):
            vertical = ''
            for j in range(i, i + 5):
                vertical += self.board[j][int(move[1])]
            if vertical in ['XXXXX', 'OOOOO']:
                return True

        # horizontal
        for i in range(int(move[1]) - 4, int(move[1]) + 1):
            if ''.join(self.board[int(move[0])][i:i + 5]) in ['XXXXX', 'OOOOO']:
                return True

        return False


    def print_board(self):
        temp = ''
        for line in self.board:
            temp += '--'.join(line) + '\n'
        print(temp)


    def initialize_board(self):
        return [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 0
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 1
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 2
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 3
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 4
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 5
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 6
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 7
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 8
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 9
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 10
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 11
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 12
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 13
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 14
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 15
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 16
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 17
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 18
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # 19
            # 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19
        ]

game = Caro()
game.host_game('localhost', 9003)