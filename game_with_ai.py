
# RGB
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BLACK = (0, 0, 0)

ROW_COUNT = 0
COLUMN_COUNT = 0

PLAYER = 0
SKY_NET = 1  # AI actually XD,just had fun

PLAYER_PIECE = 0
AI_PIECE = 0

WINDOW_LENGTH = 4
EMPTY = 0


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_valid_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))




SQUARE_SIZE = 0

width = 0
height = 0

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)


def wining_move(board, piece):
    # Check horizontal location to win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and \
                    board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical location to win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and \
                    board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Check for Positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and \
                    board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check for Negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and \
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def evaluate(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    # 4 in a row
    if window.count(piece) == 4:
        score += 100
    # 3 in a row
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0
    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            # 4 in a row
            score += evaluate(window, piece)
    # Score Vertical
    for c in range(COLUMN_COUNT):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = column_array[r:r + WINDOW_LENGTH]
            score += evaluate(window, piece)
    # Score positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate(window, piece)
    # Score negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate(window, piece)

    return score


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for column in valid_locations:
        row = get_valid_row(board, column)
        # we make copy to take new memory location, to any modifications do not change main board
        temp_board = board.copy()
        drop_piece(temp_board, row, column, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = column

    return best_col


def is_terminal_node(board):
    return wining_move(board, PLAYER_PIECE) or wining_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maximizing_player, alpha, beta):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if wining_move(board, AI_PIECE):
                return None, 9999999999999999
            elif wining_move(board, PLAYER_PIECE):
                return None, -9999999999999999
            else:  # no more valid moves
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_valid_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False, alpha, beta)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha > beta:
                break
        return column, value
    else:  # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_valid_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True, alpha, beta)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta,value)
            if beta <= alpha:
                break
        return column, value


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # rect(Surface, color, Rect,width = 0)
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # circle(Surface, color, pos, radius, width=0)
            pygame.draw.circle(screen,
                               BLACK,
                               (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)),
                               RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(
                    screen,
                    RED,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                     height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                     height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS)
    pygame.display.update()




my_font = pygame.font.SysFont("monospace", 75)

game_over = False
turn = random.randint(PLAYER, SKY_NET)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        # MouseButtonDown give us position
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Ask for PLayer 1 input
            if turn == PLAYER:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_valid_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if wining_move(board, PLAYER_PIECE):
                        label = my_font.render("Player 1 wins", 1, RED)
                        screen.blit(label, (40, 10))
                        print("Player 1 wins")
                        game_over = True

                    turn += 1
                    turn = turn % 2

    # Ask for PLayer 2 input
    if turn == SKY_NET and not game_over:

        #col = random.randint(0, COLUMN_COUNT - 1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 4, True, -math.inf, math.inf)
        if is_valid_location(board, col):
            # pygame.time.wait(500)
            row = get_valid_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if wining_move(board, AI_PIECE):
                label = my_font.render("Player 2 wins", 7, YELLOW)
                screen.blit(label, (40, 10))
                print("Player 2 wins")
                game_over = True

            turn += 1
            turn = turn % 2

            print_board(board)
            draw_board(board)

    if game_over:
        pygame.time.wait(3000)