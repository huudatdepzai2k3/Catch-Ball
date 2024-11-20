import pygame, sys, cv2, random
from cvzone.HandTrackingModule import HandDetector
from pygame import mixer

# Initialize the game size
width = 1366
height = 768

# OpenCV code
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Initialize Pygame
pygame.init()

# Background sounds
mixer.music.load('music/sound_track.mp3')
mixer.music.play(loops=-1)

closedHand_sound = mixer.Sound('music/slap.mp3')
catching_sound = mixer.Sound('music/catching_sound.wav')
TimePassing_sound = mixer.Sound('music/time_passing.mp3')
gameOver_sound = mixer.Sound('music/game_over.mp3')
bomb_sound = mixer.Sound('music/bom_sound.mp3')
heart_sound = mixer.Sound('music/heart_collect.mp3')

# Define the screen
screen = pygame.display.set_mode((width, height))

# Timer
clock = pygame.time.Clock()
currentTime = 1

# Title and Icon
pygame.display.set_caption("Catch Ball")
icon = pygame.image.load('images/ball_32.png').convert_alpha()
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load('images/Catch_Ball.png').convert()

# Balls
BallsImg = []
BallsX = []
BallsY = []
Balls_rect = []
BallsMoveX = []
BallsMoveY = []
numberOfBallss = 8

# Bombs
BombImg = pygame.image.load('images/bomb.webp').convert_alpha()
bombs = []
bomb_rects = []
bombMoveX = []
bombMoveY = []
numberOfBombs = 4

# Hearts
HeartImg = pygame.image.load('images/heart.png').convert_alpha()
heart_rects = []
heartMoveX = []
heartMoveY = []
max_hearts = 2
heart_spawned = False  # Check if a heart is currently on screen

for i in range(numberOfBallss):
    BallsX.append(random.randint(0, width))
    BallsY.append(random.randint(0, height))
    BallsImg.append(pygame.image.load('images/ball_32.png').convert_alpha())
    Balls_rect.append(BallsImg[i].get_rect(topleft=(BallsX[i], BallsY[i])))
    BallsMoveX.append(10)
    BallsMoveY.append(8)

for _ in range(numberOfBombs):
    bombX = random.randint(0, width)
    bombY = random.randint(0, height)
    bombs.append(BombImg)
    bomb_rects.append(BombImg.get_rect(topleft=(bombX, bombY)))
    bombMoveX.append(random.choice([-5, 5]))  # Random horizontal movement
    bombMoveY.append(random.choice([-3, 3]))  # Random vertical movement

# Game Texts
score_value = 0
life = 3  # Player life
font = pygame.font.Font('freesansbold.ttf', 32)
gameOver_font = pygame.font.Font('freesansbold.ttf', 100)
textX = 10
textY = 10

# Game State
game_over = False
game_over_start_time = 0

# Sound state
time_sound_played = False
gameOver_sound_played = False

# Reset game function
def reset_game():
    global score_value, life, currentTime, game_over, heart_spawned, heart_rects, heartMoveX, heartMoveY, Balls_rect, BallsMoveX, BallsMoveY, bomb_rects, bombMoveX, bombMoveY, time_sound_played, gameOver_sound_played

    score_value = 0
    life = 3
    currentTime = pygame.time.get_ticks()  # Reset to current time for a new 60-second countdown
    game_over = False
    heart_spawned = False
    heart_rects = []  # Clear hearts
    heartMoveX = []  # Clear heart movements
    heartMoveY = []  # Clear heart movements

    Balls_rect = []  # Clear Ballss
    BallsMoveX = []  # Clear Balls movements
    BallsMoveY = []  # Clear Balls movements

    bomb_rects = []  # Clear bombs
    bombMoveX = []  # Clear bomb movements
    bombMoveY = []  # Clear bomb movements

    # Reset Ballss and bombs
    for i in range(numberOfBallss):
        Balls_rect.append(BallsImg[i].get_rect(topleft=(random.randint(0, width), random.randint(0, height))))
        BallsMoveX.append(10)
        BallsMoveY.append(8)

    for _ in range(numberOfBombs):
        bombX = random.randint(0, width)
        bombY = random.randint(0, height)
        bomb_rects.append(BombImg.get_rect(topleft=(bombX, bombY)))
        bombMoveX.append(random.choice([-5, 5]))  # Random horizontal movement
        bombMoveY.append(random.choice([-3, 3]))  # Random vertical movement

    # Reset timer
    currentTime = pygame.time.get_ticks()  # Reset to current time for a new 60-second countdown

    # Reset timer and sounds
    time_sound_played = False
    mixer.music.load('music/sound_track.mp3')
    mixer.music.play(loops=-1)

    # Reset "game over" flag so it can trigger again in the future
    gameOver_sound_played = False

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_life(x, y):
    if life == 1:
        life_text = font.render("Life : " + str(life), True, (240, 104, 19))
    else:
        life_text = font.render("Life : " + str(life), True, (150, 212, 58))
    screen.blit(life_text, (x, y))

def show_timer():
    global game_over_start_time, time_sound_played, game_over
    time_set = 60
    if not game_over:
        remaining_time = time_set - (pygame.time.get_ticks() - currentTime) // 1000  # Calculate remaining time in seconds
    else:
        remaining_time = 0

    if remaining_time <= 10:
        if remaining_time % 2 == 0:
            timer = font.render("Time: " + str(remaining_time), True, (255, 0, 0))
        else:
            timer = font.render("Time: " + str(remaining_time), True, (255, 255, 255))

        # Play sound when there are 10 seconds left
        if remaining_time <= 10 and not time_sound_played:
            TimePassing_sound.play(-1)  # Play sound continuously
            time_sound_played = True  # Mark sound as played
    else:
        timer = font.render("Time: " + str(remaining_time), True, (255, 255, 255))

    if remaining_time <= 0 :
        game_over = True
        
    screen.blit(timer, (1210, 10))

def game_over_screen():
    global gameOver_sound_played
    if not gameOver_sound_played:  # Only play sound once
        gameOver_sound.play()
        gameOver_sound_played = True  # Mark sound as played
    
    game_over_text = gameOver_font.render("Game Over!", True, (16, 122, 185))
    screen.blit(game_over_text, (width / 2 - 300, height / 2 - 100))

    # Instructions to play again or quit
    play_again_text = font.render("Press R to Play Again", True, (255, 255, 255))
    quit_text = font.render("Press Q to Quit", True, (255, 255, 255))
    
    screen.blit(play_again_text, (width / 2 - 150, height / 2 + 30))
    screen.blit(quit_text, (width / 2 - 100, height / 2 + 70))

    pygame.display.update()

    # Handle key events when game over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Quit game
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:  # Restart game
                reset_game()
                return

indexes_for_closed_fingers = [8, 12, 16, 20]

# Game Loop
catch_Balls_with_openHand = False
fingers = [0, 0, 0, 0]

# Heart Spawn Timer
heart_spawn_timer = 0
heart_spawn_duration = random.randint(15000, 25000)  # 15 to 25 seconds

while True:
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

        # Check for key press events for game reset or exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Exit game
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:  # Reset game
                reset_game()

    success, frame = cap.read()
    hands, frame = detector.findHands(frame)

    # Initialize hand type
    hand_type = "unknown"

    if hands:
        lmList = hands[0]
        wrist_x = lmList['lmList'][0][0]  # x-coordinate of the wrist
        if wrist_x < width / 2:
            hand_type = "left"  # Left hand detected
        else:
            hand_type = "right"  # Right hand detected

        # Player setup based on hand type
        if hand_type == "left":
            openHandImg = pygame.image.load('images/openHand_left.png').convert_alpha()
            openHandImg = pygame.transform.scale(openHandImg, (128, 128))
            closedHandImg = pygame.image.load('images/closedHand_left.png').convert_alpha()
            closedHandImg = pygame.transform.scale(closedHandImg, (128, 128))
        else:
            openHandImg = pygame.image.load('images/openHand_right.png').convert_alpha()
            openHandImg = pygame.transform.scale(openHandImg, (128, 128))
            closedHandImg = pygame.image.load('images/closedHand_right.png').convert_alpha()
            closedHandImg = pygame.transform.scale(closedHandImg, (128, 128))

        openHand_rect = openHandImg.get_rect(topleft=(width / 2, height / 2))
        closedHand_rect = closedHandImg.get_rect(topleft=(width / 2, height / 2))

        positionOfTheHand = lmList['lmList']
        openHand_rect.left = width - positionOfTheHand[9][0] * 1.5
        openHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5
        closedHand_rect.left = width - positionOfTheHand[9][0] * 1.5
        closedHand_rect.top = (positionOfTheHand[9][1] - 200) * 1.5

        hand_is_closed = 0
        for index in range(0, 4):
            if positionOfTheHand[indexes_for_closed_fingers[index]][1] > positionOfTheHand[indexes_for_closed_fingers[index] - 2][1]:
                fingers[index] = 1
            else:
                fingers[index] = 0

            if fingers[0] * fingers[1] * fingers[2] * fingers[3]:
                if hand_is_closed and not catch_Balls_with_openHand:
                    closedHand_sound.play()
                hand_is_closed = 0
                screen.blit(closedHandImg, closedHand_rect)
                if not game_over:
                     # Handle heart collection
                    for heart_index in range(len(heart_rects)):
                        if heart_rects[heart_index].colliderect(openHand_rect) and heart_spawned and catch_Balls_with_openHand:
                            heart_sound.play()
                            life += 1  # Increment life
                            heart_spawned = False
                            heart_rects.pop(heart_index)
                            heartMoveX.pop(heart_index)
                            heartMoveY.pop(heart_index)
                    
                    for iteration in range(numberOfBallss):
                        if openHand_rect.colliderect(Balls_rect[iteration]) and catch_Balls_with_openHand:
                            score_value += 1
                            catching_sound.play()
                            Balls_rect[iteration] = BallsImg[iteration].get_rect(topleft=(random.randint(0, 1366), random.randint(0, 768)))

                catch_Balls_with_openHand = False
            else:
                screen.blit(openHandImg, openHand_rect)
                hand_is_closed = 1
                for iterate in range(numberOfBallss):
                    if openHand_rect.colliderect(Balls_rect[iterate]):
                        catch_Balls_with_openHand = True

            if not game_over:
                for bomb_index in range(numberOfBombs):                            
                    if openHand_rect.colliderect(bomb_rects[bomb_index]):
                        life -= 1
                        bomb_sound.play()
                        bomb_rects[bomb_index] = BombImg.get_rect(topleft=(random.randint(0, 1366), random.randint(0, 768)))
                        if life <= 0:
                            game_over = True

    # Update Ballss
    for i in range(numberOfBallss):
        Balls_rect[i].right += BallsMoveX[i]
        if Balls_rect[i].right <= 16:
            BallsMoveX[i] += 10
        elif Balls_rect[i].right >= width:
            BallsMoveX[i] -= 10

        Balls_rect[i].top += BallsMoveY[i]
        if Balls_rect[i].top <= 0:
            BallsMoveY[i] += 8
        elif Balls_rect[i].top >= height - 32:
            BallsMoveY[i] -= 8
        screen.blit(BallsImg[i], Balls_rect[i])

    # Move bombs
    for bomb_index in range(numberOfBombs):
        bomb_rects[bomb_index].left += bombMoveX[bomb_index]
        bomb_rects[bomb_index].top += bombMoveY[bomb_index]

        # Bounce bombs off the edges
        if bomb_rects[bomb_index].right >= width or bomb_rects[bomb_index].left <= 0:
            bombMoveX[bomb_index] *= -1  # Reverse horizontal direction
        if bomb_rects[bomb_index].bottom >= height or bomb_rects[bomb_index].top <= 0:
            bombMoveY[bomb_index] *= -1  # Reverse vertical direction

        screen.blit(bombs[bomb_index], bomb_rects[bomb_index])

    # Heart spawning logic
    if heart_spawned:
        for index in range(len(heart_rects)):
            heart_rects[index].left += heartMoveX[index]
            heart_rects[index].top += heartMoveY[index]

            # Bounce hearts off the edges
            if heart_rects[index].right >= width or heart_rects[index].left <= 0:
                heartMoveX[index] *= -1  # Reverse horizontal direction
            if heart_rects[index].bottom >= height or heart_rects[index].top <= 0:
                heartMoveY[index] *= -1  # Reverse vertical direction

            screen.blit(HeartImg, heart_rects[index])

    if not heart_spawned and len(heart_rects) < max_hearts:
        # Check if it's time to spawn a new heart
        if pygame.time.get_ticks() - heart_spawn_timer >= heart_spawn_duration:
            new_heart_rect = HeartImg.get_rect(topleft=(random.randint(0, width), random.randint(0, height)))
            heart_rects.append(new_heart_rect)
            heartMoveX.append(random.choice([-3, 3]))  # Random horizontal movement
            heartMoveY.append(random.choice([-2, 2]))  # Random vertical movement
            heart_spawned = True  # Mark heart as spawned
            heart_spawn_timer = pygame.time.get_ticks()  # Reset the heart spawn timer
            heart_spawn_duration = random.randint(15000, 25000)  # 15 to 25 seconds for next heart
 
    show_score(textX, textY)
    show_life(textX, textY + 40)
    show_timer()

    if game_over:
        mixer.music.stop()
        TimePassing_sound.stop()
        game_over_screen()
    
    cv2.imshow("Detech hand", frame)
    pygame.display.update()
    clock.tick(60)

# End game and cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()
