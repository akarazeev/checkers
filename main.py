from board import Board

board = Board()
board.print()

while board.game_won == -1:
    print("== ВАШ ХОД ==")
    move_from, move_to, notdone = board.get_users_move()
    try:
        board.moveWhite(move_from, move_to, notdone)
    except Exception as e:
        print(f"ОШИБКА: {e}")
        continue

    move_from, move_to, notdone = board.bots_move()
    print(f"== ХОД БОТА ({board.xy_to_pos(move_from)} {board.xy_to_pos(move_to)}) ==")
    board.move_black(move_from, move_to, notdone)

    if board.game_won == board.WHITE:
        print("Белые побеждают!")
        break
    elif board.game_won == board.BLACK:
        print("Чёрные побеждают!")
        break
