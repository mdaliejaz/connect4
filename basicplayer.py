from util import memoize, run_search_function, setnodeminimax, NODES_EXPANDED_BY_MINIMAX


def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


def minimax_search(board, depth, eval_fn,
                                get_next_moves_fn=get_all_next_moves,
                                is_terminal_fn=is_terminal):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal_fn(depth, board):
        return [eval_fn(board), None]

    score = [None, None]
    global NODES_EXPANDED_BY_MINIMAX

    for move, new_board in get_next_moves_fn(board):
        NODES_EXPANDED_BY_MINIMAX += 1
        child_score = minimax_search(new_board, depth - 1, eval_fn,
                                                      get_next_moves_fn, is_terminal_fn)
        child_score[0] *= -1
        if score[0] is None or child_score[0] > score[0]:
            score[0] = child_score[0]
    return score


def minimax(board, depth, eval_fn=basic_evaluate,
            get_next_moves_fn=get_all_next_moves,
            is_terminal_fn=is_terminal,
            verbose=True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """

    game = [None, None]
    global NODES_EXPANDED_BY_MINIMAX

    for possible_move, new_board in get_next_moves_fn(board):
        NODES_EXPANDED_BY_MINIMAX += 1
        score = minimax_search(new_board, depth - 1, eval_fn,
                                                        get_next_moves_fn,
                                                        is_terminal_fn)
        score[0] *= -1
        if game[0] is None or score[0] > game[0]:
            game[0] = score[0]
            game[1] = possible_move

    setnodeminimax(NODES_EXPANDED_BY_MINIMAX)
    return game[1]


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


def get_chain_len(chain_type, board, row, col, player):
    token_count = 0
    if chain_type == 0:
        if col + 2 < 7 and board.get_cell(row, col + 2) == player and board.get_cell(row, col + 1) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif col + 1 < 7 and board.get_cell(row, col + 1) == player and board.get_cell(row, col) == player:
            token_count += 10
        elif board.get_cell(row, col) == player:
            token_count += 1
    elif chain_type == 1:
        if row + 2 < 6 and board.get_cell(row + 2, col) == player and board.get_cell(row + 1, col) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif row + 1 < 6 and board.get_cell(row + 1, col) == player and board.get_cell(row, col) == player:
            token_count += 10
        elif board.get_cell(row, col) == player:
            token_count += 1
    elif chain_type == 2:
        if row + 2 < 6 and col + 2 < 7 and board.get_cell(row + 2, col + 2) == player and \
                        board.get_cell(row + 1, col + 1) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif row + 1 < 6 and col + 1 < 7 and board.get_cell(row + 1, col + 1) == player and \
                        board.get_cell(row, col) == player:
            token_count += 10
        elif board.get_cell(row, col) == player:
            token_count += 1

        elif row + 2 < 6 and col - 2 < 7 and board.get_cell(row + 2, col - 2) == player and \
                        board.get_cell(row + 1, col - 1) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif row + 1 < 6 and col - 1 < 7 and board.get_cell(row + 1, col - 1) == player and \
                        board.get_cell(row, col) == player:
            token_count += 10

        elif row + 3 < 6 and col + 3 < 7 and board.get_cell(row + 3, col + 3) == player and \
                        board.get_cell(row + 1, col + 1) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif row + 3 < 6 and col + 3 < 7 and board.get_cell(row + 3, col + 3) == player and \
                        board.get_cell(row + 2, col + 2) == player \
                and board.get_cell(row, col) == player:
            token_count += 100

        elif row + 3 < 6 and col - 3 < 7 and board.get_cell(row + 3, col - 3) == player and \
                        board.get_cell(row + 1, col - 1) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
        elif row + 3 < 6 and col - 3 < 7 and board.get_cell(row + 3, col - 3) == player and \
                        board.get_cell(row + 2, col - 2) == player \
                and board.get_cell(row, col) == player:
            token_count += 100
    return token_count


def new_evaluate(board):
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score_row = 0
        score_col = 0
        score_diag = 0
        current_player = board.get_current_player_id()
        other_player = board.get_other_player_id()
        score = 0

        for row in xrange(6):
            for col in xrange(7):
                # Check for consecutive tokens in all three directions
                if board.get_cell(row, col) == board.get_current_player_id():
                    score_col -= get_chain_len(0, board, row, col, current_player)
                    score_row -= get_chain_len(1, board, row, col, current_player)
                    score_diag -= get_chain_len(2, board, row, col, current_player)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score_col += get_chain_len(0, board, row, col, other_player)
                    score_row += get_chain_len(1, board, row, col, other_player)
                    score_diag += get_chain_len(2, board, row, col, other_player)
            if board.get_cell(row, col) == board.get_current_player_id():
                score -= abs(3 - col) * 100
            elif board.get_cell(row, col) == board.get_other_player_id():
                score += abs(3 - col) * 100
        score += score_row + score_col + score_diag
    return score


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
