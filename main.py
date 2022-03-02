

# RGB
PINK = (255, 192, 203)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

BLACK = (0, 0, 0)

ROW_COUNT = 0
COLUMN_COUNT = 0


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


pygame.init()

SQUARE_SIZE = 0

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(0)

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
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    PINK,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                     height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                     height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                    RADIUS)
    pygame.display.update()




font = pygame.font.SysFont("monospace", 36)



while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # showing the who's turn
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PINK, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        # MouseButtonDown give us position
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # Ask for PLayer 1 input
            if turn == 0:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE)) #5.5 ->5

                if is_valid_location(board, col):
                    row = get_valid_row(board, col)
                    drop_piece(board, row, col, 1)

                    if wining_move(board, 1):
                        label = font.render("error", 1, PINK)
                        screen.blit(label, (40, 10))
                        print("error")
                        game_over = True
            # Ask for PLayer 2 input
            else:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_valid_row(board, col)
                    drop_piece(board, row, col, 2)

                    if wining_move(board, 2):
                        label = font.render("error", 1, YELLOW)
                        screen.blit(label, (40,10))
                        print("error")
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)