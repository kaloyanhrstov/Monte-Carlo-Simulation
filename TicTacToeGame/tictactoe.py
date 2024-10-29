import sys
from copy import deepcopy
from mcts import *
import pygame

pygame.init()

WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (63, 66, 74)

font = pygame.font.SysFont('freesansbold.ttf', 40)

# Initialize Pygame
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")


# Tic Tac Toe board class
class Board:
    # create constructor (init board class instance)
    def __init__(self, board=None):
        # define players
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        self.game_over = False

        # define board position
        self.position = {}

        # init (reset) board
        self.init_board()

        # create a copy of a previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    # init (reset) board
    def init_board(self):
        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                # set every board square to empty square
                self.position[row, col] = self.empty_square

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                # pygame.draw.rect(WINDOW, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.position[row, col] == 'o':
                    pygame.draw.circle(WINDOW, GREY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)
                elif self.position[row, col] == 'x':
                    pygame.draw.line(WINDOW, GREY, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE - SQUARE_SIZE // 4), 3)
                    pygame.draw.line(WINDOW, GREY, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE - SQUARE_SIZE // 4),
                                     (col * SQUARE_SIZE + SQUARE_SIZE - SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), 3)

    @staticmethod
    def draw_board_grid(screen, screen_width, screen_height, line_width):
        grid = (50, 50, 50)
        for x in range(1, 3):
            pygame.draw.line(screen, grid, (0, 100 * x), (screen_width, 100 * x), line_width)
            pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

    # make move
    def make_move(self, row, col):
        # create new board instance that inherits from the current state
        board = Board(self)

        # make move
        board.position[row, col] = self.player_1

        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        # return new board state
        return board

    # get whether the game is drawn
    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            # empty square is available
            if self.position[row, col] == self.empty_square:
                # this is not a draw
                return False

        # by default we return a draw
        self.game_over = True
        return True

    # get whether the game is won
    def is_win(self):
        # vertical sequence detection
        # loop over board columns
        for col in range(3):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for row in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    self.game_over = True
                    return True

        # horizontal sequence detection
        # loop over board columns
        for row in range(3):
            # define winning sequence list
            winning_sequence = []

            # loop over board rows
            for col in range(3):
                # if found same next element in the row
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in the row
                if len(winning_sequence) == 3:
                    # return the game is won state
                    return True

        # 1st diagonal sequence detection
        # define winning sequence list
        winning_sequence = []

        # loop over board rows
        for row in range(3):
            # init column
            col = row

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True

        # 2nd diagonal sequence detection
        # define winning sequence list
        winning_sequence = []

        # loop over board rows
        for row in range(3):
            # init column
            col = 3 - row - 1

            # if found same next element in the row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

            # if we have 3 elements in the row
            if len(winning_sequence) == 3:
                # return the game is won state
                return True

        # by default return non winning state
        return False

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.position[row, col] == ".":
                    empty_squares.append((row, col))
        return empty_squares

    def is_board_full(self):
        return len(self.get_empty_squares()) == 0

    # generate legal moves to play in the current position
    def generate_states(self):
        # define states list (move list - list of available actions to consider)
        actions = []

        # loop over board rows
        for row in range(3):
            # loop over board columns
            for col in range(3):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/board state to action list
                    actions.append(self.make_move(row, col))

        # return the list of available actions (board class instances)
        return actions

    # main game loop
    def game_loop(self):
        clock = pygame.time.Clock()
        mcts = MCTS()

        while True:
            self.draw_board_grid(WINDOW, WIDTH, HEIGHT, 6)
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # if game.player == 1:  # Only player 1 (X) can make moves
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // SQUARE_SIZE
                    row = mouse_pos[1] // SQUARE_SIZE

                    # if self.position[row, col] != self.empty_square:
                    #     print(' Illegal move!')
                    #     continue
                    if not self.game_over and not self.is_board_full():
                        self = self.make_move(row, col)

                    # print(self)

                    # AI's turn
                    if not self.game_over and not self.is_board_full():
                        best_move = mcts.search(self)

                        # make AI move here
                        self = best_move.board

                    # print(self)

            # check if the game is won
            if self.is_win():
                end_text = 'player "%s" has won the game!' % self.player_2

                end_img = font.render(end_text, True, RED)
                pygame.draw.rect(WINDOW, BLACK, (WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50))
                WINDOW.blit(end_img, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

            # check if the game is drawn
            elif self.is_draw():
                end_text = 'Game is drawn!'

                end_img = font.render(end_text, True, RED)
                pygame.draw.rect(WINDOW, BLACK, (WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50))
                WINDOW.blit(end_img, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

            pygame.display.update()
            clock.tick(60)

    # print board state
    # def __str__(self):
    #     # define board string representation
    #     board_string = ''
    #
    #     # loop over board rows
    #     for row in range(3):
    #         # loop over board columns
    #         for col in range(3):
    #             board_string += ' %s' % self.position[row, col]
    #
    #         # print new line every row
    #         board_string += '\n'
    #
    #     # prepend side to move
    #     if self.player_1 == 'x':
    #         board_string = '\n--------------\n "x" to move:\n--------------\n\n' + board_string
    #
    #     elif self.player_1 == 'o':
    #         board_string = '\n--------------\n "o" to move:\n--------------\n\n' + board_string
    #
    #     # return board string
    #     return board_string


# main driver
if __name__ == '__main__':
    # create board instance
    board = Board()

    # start game loop
    board.game_loop()
