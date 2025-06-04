import pygame, sys
from pygame.locals import *
import random


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):  # draw button on screen
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))


def decrease_bg_volume():
    global current_volume

    if current_volume >= 0.1:
        current_volume -= 0.1
        pygame.mixer.music.set_volume(current_volume)
    if current_volume < 0.1:
        pygame.mixer.music.pause()


def increase_bg_volume():
    global current_volume

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    if current_volume < 1:
        current_volume += 0.1
        pygame.mixer.music.set_volume(current_volume)


def create_board():
    game_board = [[" ", " ", " "],
                  [" ", " ", " "],
                  [" ", " ", " "]]
    return game_board


def check_winner(board, player):
    for row in board:  # horizontal combinations
        if all(cell == player for cell in row):
            return True

    for col in range(len(board)):  # vertical combinations
        if all(board[row][col] == player for row in range(len(board))):
            return True

    # diagonal combinations
    if all(board[i][i] == player for i in range(len(board))):  # top left to bottom right
        return True
    if all(board[i][2 - i] == player for i in range(len(board))):  # top right to bottom left
        return True


def check_draw(board):
    if all(cell != " " for row in board for cell in row):
        # match is a draw
        return True


def display_game_over_screen(player):
    # music
    pygame.mixer.music.load('assets/music/Jorge Hernandez - Chopsticks.mp3')  # background music
    pygame.mixer.music.play(-1, 0.0)

    SCREEN.fill(LIGHT_BLUE)

    # text
    game_over_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 70)
    game_over_text = game_over_font.render(
        f"Game over!",
        False,
        BLACK,
        )
    SCREEN.blit(game_over_text, (SCREEN.get_width() // 2 - game_over_text.get_width() // 2,
                                 SCREEN.get_height() // 2 - game_over_text.get_height() * 1.5))

    player_wins_text = game_over_font.render(
        f"Player {player} wins!",
        False,
        BLACK,
    )
    SCREEN.blit(player_wins_text, (SCREEN.get_width() // 2 - player_wins_text.get_width() // 2,
                                 SCREEN.get_height() // 2 - player_wins_text.get_height() // 2))

    restart_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 48)
    restart_text = restart_font.render(
        f"Press 'Space' to restart",
        False,
        BLACK,
    )
    SCREEN.blit(restart_text, (SCREEN.get_width() // 2 - restart_text.get_width() // 2,
                                 SCREEN.get_height() // 2 + restart_text.get_height()))
    pygame.display.update()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    reset_game()
                    done = True


def display_game_draw_screen():
    # music
    pygame.mixer.music.load('assets/music/Jorge Hernandez - Chopsticks.mp3')  # background music
    pygame.mixer.music.play(-1, 0.0)

    SCREEN.fill(LIGHT_BLUE)

    # text
    game_over_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 70)
    game_over_text = game_over_font.render(
        f"Game ended in a draw",
        False,
        BLACK,
        )
    SCREEN.blit(game_over_text, (SCREEN.get_width() // 2 - game_over_text.get_width() // 2,
                                 SCREEN.get_height() // 2 - game_over_text.get_height()))

    restart_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 48)
    restart_text = restart_font.render(
        f"Press 'Space' to restart",
        False,
        BLACK,
    )
    SCREEN.blit(restart_text, (SCREEN.get_width() // 2 - restart_text.get_width() // 2,
                                 SCREEN.get_height() // 2 + restart_text.get_height() // 2))
    pygame.display.update()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    reset_game()
                    done = True


def reset_game():
    global SCREEN, board, current_player, current_volume

    # ---------- Music ----------
    playlist = ["assets/music/Density & Time - MAZE.mp3"]
    random_song = random.choice(playlist)
    pygame.mixer.music.load(random_song)  # background music
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(current_volume)

    # ---------- Screen ----------
    SCREEN.fill(LIGHT_BLUE)  # screen background color
    title_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 32)  # game title font
    title = title_font.render('TIC-TAC-TOE', False, BLACK)  # game title
    title_position = title.get_rect()  # make title movable
    title_position.center = (400, 50)  # position the game title: (x, y)

    # ---------- home button ----------
    home_button_image = pygame.image.load('assets/images/home_button.png').convert_alpha()
    home_button = Button(400, 500, home_button_image, 0.5)
    home_button.draw()

    # ---------- volume buttons ----------
    vol_up_img = pygame.image.load('assets/images/volume_up.png').convert_alpha()
    vol_up_button = Button(30, 30, vol_up_img, 0.1)
    vol_up_button.draw()

    vol_down_img = pygame.image.load('assets/images/volume_down.png').convert_alpha()
    vol_down_button = Button(100, 30, vol_down_img, 0.1)
    vol_down_button.draw()

    # ---------- tic-tac-toe board ----------
    # vertical lines
    pygame.draw.line(SCREEN, BLACK, (350, 100), (350, 400), 5)
    pygame.draw.line(SCREEN, BLACK, (450, 100), (450, 400), 5)
    # horizontal lines
    pygame.draw.line(SCREEN, BLACK, (250, 200), (550, 200), 5)
    pygame.draw.line(SCREEN, BLACK, (250, 300), (550, 300), 5)

    board = create_board()
    current_player = player_x

    game_is_running = True
    game_over = False
    game_draw = False

    pygame.display.update()
    main(title, title_position, home_button, game_is_running, game_over, game_draw, vol_up_button, vol_down_button)


def home_page():
    global current_volume
    # ---------- Music ----------
    pygame.mixer.music.load('assets/music/[FREE]  2016  Video Game Type Beat.mp3')  # background music (By B0ND! on YT)
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(current_volume)

    # ---------- Screen ----------
    SCREEN.fill(LIGHT_BLUE)  # screen background color
    title_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 70)  # game title font
    title = title_font.render('TIC-TAC-TOE', False, BLACK)  # game title
    title_position = title.get_rect()  # make title movable
    title_position.center = (400, 100)  # position the game title: (x, y)
    SCREEN.blit(title, title_position)

    credit_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 32)  # game title font
    credit = credit_font.render('By: Ghostypods on Github', False, BLACK)  # credit
    credit_pos = credit.get_rect()  # make title movable
    credit_pos.center = (400, 500)  # position the game title: (x, y)
    SCREEN.blit(credit, credit_pos)

    # ---------- start button ----------
    start_button_image = pygame.image.load('assets/images/start_button.png').convert_alpha()
    start_button = Button(400, 300, start_button_image, 0.3)
    start_button.draw()

    # ---------- volume buttons ----------
    vol_up_img = pygame.image.load('assets/images/volume_up.png').convert_alpha()
    vol_up_button = Button(30, 30, vol_up_img, 0.1)
    vol_up_button.draw()

    vol_down_img = pygame.image.load('assets/images/volume_down.png').convert_alpha()
    vol_down_button = Button(100, 30, vol_down_img, 0.1)
    vol_down_button.draw()

    pygame.display.update()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if start_button.rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    reset_game()
                    done = True

                if vol_up_button.rect.collidepoint(mouse_pos):
                    increase_bg_volume()

                if vol_down_button.rect.collidepoint(mouse_pos):
                    decrease_bg_volume()


def hitboxes():
    # ---------- cells/hitboxes ----------
    squares_hitbox = []  # stores every cell in the board

    # size and initial position of a cell's hitbox
    x = 250
    y = 100
    width = 100
    height = 100

    # create hitboxes
    for square in range(3):  # top row
        clickable_square = pygame.Rect(x, y, width, height)  # create hitbox for current cell
        x += 100  # move to next cell
        row_num = 0
        col_num = square
        squares_hitbox.append([clickable_square, row_num, col_num])  # store current cell

    x = 250
    y = 200
    for square in range(3):  # middle row
        clickable_square = pygame.Rect(x, y, width, height)  # pygame.draw.rect(SCREEN, RED, (x, y, width, height), 1)
        x += 100
        row_num = 1
        col_num = square
        squares_hitbox.append([clickable_square, row_num, col_num])

    x = 250
    y = 300
    for square in range(3):  # bottom row
        clickable_square = pygame.Rect(x, y, width, height)  # pygame.draw.rect(SCREEN, RED, (x, y, width, height), 1)
        x += 100
        row_num = 2
        col_num = square
        squares_hitbox.append([clickable_square, row_num, col_num])

    return squares_hitbox


def main(title, title_position, home_button, game_is_running, game_over, game_draw, vol_up_btn, vol_down_btn):
    global SCREEN, board, current_player, hitboxes_list
    # Runs the game
    while game_is_running:
        SCREEN.blit(title, title_position)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # draws the current players move
                mouse_pos = event.pos  # position of the click

                if home_button.rect.collidepoint(mouse_pos):
                    home_page()

                if vol_up_btn.rect.collidepoint(mouse_pos):
                    increase_bg_volume()

                if vol_down_btn.rect.collidepoint(mouse_pos):
                    decrease_bg_volume()

                # check if a cell was clicked
                for hitbox in hitboxes_list:  # checks each cell
                    if hitbox[0].collidepoint(mouse_pos):
                        # a cell was clicked
                        if current_player == player_x and board[hitbox[1]][hitbox[2]] == " ":
                            SCREEN.blit(current_player, (hitbox[0].x + 37, hitbox[0].y + 25))  # draw 'X'
                            board[hitbox[1]][hitbox[2]] = x_piece

                        elif current_player == player_o and board[hitbox[1]][hitbox[2]] == " ":
                            SCREEN.blit(current_player, (hitbox[0].x + 37, hitbox[0].y + 25))  # draw 'O'
                            board[hitbox[1]][hitbox[2]] = o_piece

                        else:
                            print("This spot is already taken bozo")
                            continue

                        if check_winner(board, 'X' if current_player == player_x else 'O'):
                            game_over = True

                        if check_draw(board):
                            game_draw = True

                        # switches to other player's turn
                        if not game_over and not game_draw:
                            current_player = player_x if current_player == player_o else player_o

            if event.type == QUIT:  # ends the game
                pygame.quit()
                sys.exit()

        pygame.display.update()  # update game

        if game_over:
            pygame.time.delay(1000)
            pygame.mixer.music.stop()
            winner = 'X' if current_player == player_x else 'O'
            display_game_over_screen(winner)

        if game_draw:
            pygame.time.delay(1000)
            pygame.mixer.music.stop()
            display_game_draw_screen()


# ---------- Initialization ----------
pygame.init()  # initialization
SCREEN = pygame.display.set_mode((800, 600), 0, 32)  # window size
pygame.display.set_caption('Tic-Tac-Toe')  # window title
current_volume = 0.5

# ---------- colors ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (150, 222, 255)

# ---------- Players ----------
player_font = pygame.font.Font('assets/fonts/ThaleahFat.ttf', 64)  # font of players' pieces

x_piece = "X"
o_piece = "O"
player_x = player_font.render(x_piece, False, BLACK)  # player x
player_o = player_font.render(o_piece, False, BLACK)  # player o

current_player = player_x  # set starting player

board = create_board()  # set up the game board

hitboxes_list = hitboxes()  # create hitboxes for each square on the board

home_page()  # start game from home page


