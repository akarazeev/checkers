class Board(object):
    BLACK = 1
    WHITE = 0
    NOTDONE = -1

    def __init__(self, height=8, width=8, first_player=0):
        self.width = width
        self.height = height

        # Листы для хранения позиций шашек
        self.blacklist = list()
        self.whitelist = list()

        for i in range(width):
            self.blacklist.append((i, (i+1)%2))
            if i % 2 != 0:
                self.blacklist.append((i, 2 + ((i+1)%2)))

            self.whitelist.append((i, height - (i%2) - 1))
            if i % 2 == 0:
                self.whitelist.append((i, height - (i % 2) - 3))

        self.board_state = [[' '] * self.width for _ in range(self.height)]
        self.game_won = self.NOTDONE
        self.turn = first_player

    def _print_welcome_statement(self):
        possible_move = next(self.iter_white_moves())
        move_from = self.xy_to_pos(possible_move[0])
        move_to = self.xy_to_pos(possible_move[1])
        print(f'Выберите шашку и сделайти ход (например: "{move_from} {move_to}")')

    def pos_to_xy(self, position: str):
        x = ord(position[0]) - 97
        y = self.height - int(position[1])
        return (x, y)

    def xy_to_pos(self, xy: tuple):
        pos_x = chr(xy[0] + 97)
        pos_y = str(self.height - xy[1])
        return f'{pos_x}{pos_y}'

    def get_users_move(self):
        self._print_welcome_statement()
        moveFrom = None
        moveTo = None

        while True:
            move = input().lower().split()

            if not (len(move) == 2):
                print("ОШИБКА: Неправильный ввод")
                self._print_welcome_statement()
                continue

            moveFrom = self.pos_to_xy(move[0])
            moveTo = self.pos_to_xy(move[1])

            if not (moveFrom in self.whitelist):
                print(f"ОШИБКА: Поле {move[0]} либо пустое, либо шашка не принадлежит вам")
                self._print_welcome_statement()
                continue

            break

        move = (moveFrom, moveTo, self.NOTDONE)
        return move

    def bots_move(self):
        moveFrom, moveTo, notdone = next(self.iter_black_moves())
        return moveFrom, moveTo, notdone

    def iter_white_moves(self):
        """
        Метод для генерации шагов для белых шашек.
        """
        for piece in self.whitelist:
            for move in self.iter_white_piece(piece):
                yield move
                
    def iter_black_moves(self):
        """
        Метод для генерации шагов для чёрных шашек.
        """
        for piece in self.blacklist:
            for move in self.iter_black_piece(piece):
                yield move
                
    def iter_white_piece(self, piece):
        """
        Метод для генерации шагов для белой шашки `piece`.
        """            
        return self.iter_both(piece, ((-1,-1),(1,-1)))
    
    def iter_black_piece(self, piece):
        """
        Метод для генерации шагов для чёрной шашки `piece`.
        """
        return self.iter_both(piece, ((-1,1),(1,1)))

    def iter_both(self, piece, moves):
        """
        Метод для генерации шагов для шашки `piece` в направлениях `moves`.
        """
        for move in moves:
            # Смещение.
            targetx = piece[0] + move[0]
            targety = piece[1] + move[1]
            target = (targetx, targety)

            if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
                continue

            # Проверяем на наличие шашки поле, в которое собираемся походить.
            black = target in self.blacklist
            white = target in self.whitelist

            # Поле `target` пустое.
            if not black and not white:
                yield (piece, target, self.NOTDONE)
            else:
                # В поле `target` есть какая-то шашка.
                if self.turn == self.BLACK and black:
                    continue
                elif self.turn == self.WHITE and white:
                    continue

                # Ещё раз смещаем координаты в том же направлении.
                jumpx = target[0] + move[0]
                jumpy = target[1] + move[1]
                target = (jumpx, jumpy)

                if jumpx < 0 or jumpx >= self.width or jumpy < 0 or jumpy >= self.height:
                    continue

                # Проверяем на наличие шашки поле, в которое собираемся походить.
                black = target in self.blacklist
                white = target in self.whitelist

                # Поле `target` пустое.
                if not black and not white:
                    yield (piece, target, self.turn)
    
    def update_board(self):
        for i in range(self.width):
            for j in range(self.height):
                self.board_state[i][j] = " "
        for piece in self.blacklist:
            self.board_state[piece[1]][piece[0]] = u'◇'
        for piece in self.whitelist:
            self.board_state[piece[1]][piece[0]] = u'◆'

    def move_silent_black(self, move_from, move_to, win_loss):
        if move_to[0] < 0 or move_to[0] >= self.width or move_to[1] < 0 or move_to[1] >= self.height:
            raise Exception("Выходит за границы доски", move_from)
        black = move_to in self.blacklist
        white = move_to in self.whitelist
        if not (black or white):
            self.blacklist[self.blacklist.index(move_from)] = move_to
            self.update_board()
            self.turn = self.WHITE
            self.game_won = win_loss
        else:
            raise Exception
        
    def move_silent_white(self, move_from, move_to, win_loss):
        if move_to[0] < 0 or move_to[0] >= self.width or move_to[1] < 0 or move_to[1] >= self.height:
            raise Exception("Выходит за границы доски", move_from)

        black = move_to in self.blacklist
        white = move_to in self.whitelist
        possible_moves = [x[1] for x in self.iter_white_piece(move_from)]

        if move_to in possible_moves and not (black or white):
            self.whitelist[self.whitelist.index(move_from)] = move_to
            self.update_board()
            self.turn = self.BLACK
            self.game_won = win_loss

            dx = move_to[0] - move_from[0]
            dy = move_to[1] - move_from[1]
            if abs(dx) != 1:
                opponent_x = move_from[0] + dx // 2
                opponent_y = move_from[1] + dy // 2
                self.blacklist.remove((opponent_x, opponent_y))
        else:
            raise Exception("Так нельзя ходить, либо ещё не поддерживается(")
    
    def move_black(self, move_from, move_to, win_loss):
        """
        Метод перемещает чёрную шашку из поля `move_from` в поле `move_to`,
            аргумент `win_loss` говорит была ли съедена шашка при таком ходе.
        """
        self.move_silent_black(move_from, move_to, win_loss)
        self.print()
        
    def moveWhite(self, move_from, move_to, win_loss):
        """
        Метод перемещает белую шашку из поля `move_from` в поле `move_to`,
            аргумент `win_loss` говорит была ли съедена шашка при таком ходе.
        """
        self.move_silent_white(move_from, move_to, win_loss)
        self.print()

    def print(self):
        print(self.__unicode__())
        
    def __unicode__(self):
        self.update_board()
        lines = list()
        lines.append(u'  ╭' + (u'───┬' * (self.width-1)) + u'───╮')

        for num, row in enumerate(self.board_state[:-1]):
            lines.append(str(self.height - num) + u' │ ' + u' │ '.join(row) + u' │')
            lines.append(u'  ├' + (u'───┼' * (self.width-1)) + u'───┤')

        lines.append(str(1) + u' │ ' + u' │ '.join(self.board_state[-1]) + u' │')
        lines.append(u'  ╰' + (u'───┴' * (self.width-1)) + u'───╯')
        lines.append('    ' + '   '.join(map(lambda x: chr(x + 65), range(self.width))))

        return '\n'.join(lines)
