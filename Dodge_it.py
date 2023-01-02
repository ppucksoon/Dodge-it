from functools import cache
import math
import pygame
import random
import time
import pickle

# ------------------------초기 설정------------------------
pygame.init()
pygame.key.set_repeat(800, 50)

FPS = 60
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
size = (1500, 800)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
pygame.display.set_caption('Dodge it')

@cache
def get_font(font, font_size):
    return pygame.font.Font(f'./font/{font}', font_size)

def write(txt, font, font_size, color, pos, criterion="center", alpha = 255):
    text = get_font(font, font_size).render(txt, True, color)
    text_pos = text.get_rect()
    if criterion == "center":
        text_pos.center = pos
    elif criterion == "top":
        text_pos.top = pos
    elif criterion == "topleft":
        text_pos.topleft = pos
    elif criterion == "topright":
        text_pos.topright = pos
    elif criterion == "bottom":
        text_pos.bottom = pos
    elif criterion == "bottomleft":
        text_pos.bottomleft = pos
    elif criterion == "bottomright":
        text_pos.bottomright = pos
    text.set_alpha(alpha)
    screen.blit(text, text_pos)

# 이미지 불러오기
player_ball = pygame.image.load('./image/Dodge_it_player_ball.png')
player_ball = pygame.transform.scale(player_ball, (30, 30))
score_ball = pygame.image.load('./image/Dodge_it_player_ball.png')
score_ball = pygame.transform.scale(score_ball, (14, 14))
enemy_ball = pygame.image.load('./image/Dodge_it_enemy_ball.png')
enemy_ball = pygame.transform.scale(enemy_ball, (14, 14))
slow_ball = pygame.image.load('./image/Dodge_it_slow_ball.png')
slow_ball = pygame.transform.scale(slow_ball, (14, 14))
shield_ball = pygame.image.load('./image/Dodge_it_shield_ball.png')
shield_ball = pygame.transform.scale(shield_ball, (14, 14))
double_ball = pygame.image.load('./image/Dodge_it_double_ball.png')
double_ball = pygame.transform.scale(double_ball, (14, 14))
slow_icon = pygame.image.load('./image/Dodge_it_slow_icon.png')
slow_icon = pygame.transform.scale(slow_icon, (30, 30))
shield_icon = pygame.image.load('./image/Dodge_it_shield_icon.png')
shield_icon = pygame.transform.scale(shield_icon, (30, 30))
double_icon = pygame.image.load('./image/Dodge_it_double_icon.png')
double_icon = pygame.transform.scale(double_icon, (30, 30))
score_reblit = pygame.image.load('./image/Dodge_it_reblit_icon.png')
score_reblit = pygame.transform.scale(score_reblit, (40, 40))
leaderboard = pygame.image.load('./image/Dodge_it_leaderboard.png')
leaderboard = pygame.transform.scale(leaderboard, (340, 510))
pre_score_board = pygame.image.load('./image/Dodge_it_previous_score.png')
pre_score_board = pygame.transform.scale(pre_score_board, (340, 510))
quit_button = pygame.image.load('./image/Dodge_it_quit_button.png')
quit_button = pygame.transform.scale(quit_button, (100, 100))
keyboard = pygame.image.load('./image/Dodge_it_keyboard.png')
keyboard = pygame.transform.scale(keyboard, (1500, 800))
pause_button = pygame.image.load('./image/Dodge_it_pause.png')
pause_button = pygame.transform.scale(pause_button, (40, 40))
continue_button = pygame.image.load('./image/Dodge_it_continue.png')
continue_button = pygame.transform.scale(continue_button, (40, 40))
intro_button = pygame.image.load('./image/Dodge_it_introduction.png')
intro_button = pygame.transform.scale(intro_button, (100, 100))
right_arrow = pygame.image.load('./image/Dodge_it_right_arrow.png')
right_arrow = pygame.transform.scale(right_arrow, (50, 100))
left_arrow = pygame.image.load('./image/Dodge_it_left_arrow.png')
left_arrow = pygame.transform.scale(left_arrow, (50, 100))


# 점수 데이터 클리어(초기화)
def clearScoreData():
    with open(".\score\previous_score.pickle", "wb") as fw:
        pickle.dump([["None", 0]], fw)


# 애니메이션 함수
def easeOutQuint(x):
    return 1 - math.pow(1 - x, 5)


# 두 점 사이의 거리 계산
def distance(point_1, point_2):
    vector_1 = pygame.Vector2(point_1[0], point_1[1])
    vector_2 = pygame.Vector2(point_2[0], point_2[1])
    return vector_1.distance_to(vector_2)


# 점수 공의 스폰 위치 변경
def changeScoreBall():
    score_ball_x = random.randint(0, 1500 - 21)
    score_ball_y = random.randint(0, 800 - 14)
    score_ball_center = [score_ball_x + 10.5, score_ball_y + 7]
    return score_ball_center


# 특수 공에 닿았는지 판별 후 닿은 특수 공 삭제
def isEffectBallTouched(effect_ball_position, player_center, effect_type, is_effect_applied, time_list):
    if effect_type == "slow":
        if is_effect_applied[0] == False:
            effect = 0
            slow_start = 0
        else:
            effect = 1
            slow_start = time_list[0]
    elif effect_type == "shield":
        if is_effect_applied[1] == False:
            effect = 0
            shield_start = 0
        else:
            effect = 1
            shield_start = time_list[1]
    elif effect_type == "double":
        if is_effect_applied[2] == False:
            effect = 0
            double_start = 0
        else:
            effect = 1
            double_start = time_list[2]

    if len(effect_ball_position[0]) != 0:
        for i in range(0, len(effect_ball_position[0])):
            if distance((effect_ball_position[0][i] + 10.5, effect_ball_position[1][i] + 7), player_center) < 22:
                effect = 1
                effect_ball_position[0][i] = -1
                if effect_type == "slow":
                    slow_start = time.time() + 30
                elif effect_type == "shield":
                    shield_start = time.time() + 30
                elif effect_type == "double":
                    double_start = time.time() + 30

        for i in range(0, len(effect_ball_position[0])):
            if effect_ball_position[0][i] == -1:
                del effect_ball_position[0][i]
                del effect_ball_position[1][i]
                break

    if effect == 1:
        if effect_type == "slow":
            return [effect, slow_start]
        elif effect_type == "shield":
            return [effect, shield_start]
        elif effect_type == "double":
            return [effect, double_start]
    else:
        return [0.0, 0.0]


# 일시정지
def pause():
    global done
    quit = False

    while not quit:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    quit = True


# 게임 설명 페이지
def tutorial():
    global done
    quit = False
    page = 1
    max_page = 2
    min_page = 1

    how_to_play_text = []
    how_to_play_text.append("-How to play game-")
    how_to_play_text.append("Press SPACE, W, arrow(up) to jump")
    how_to_play_text.append("Press A, arrow(left) to move left")
    how_to_play_text.append("Press D, arrow(right) to move right")
    how_to_play_text.append("Press P to pause and continue game")
    how_to_play_text.append("Press R to spawn new score ball")

    intro_text = []
    intro_text.append("-Effects of balls-")
    intro_text.append("White balls give you a score")
    intro_text.append("Red balls make the game over")
    intro_text.append(
        "Green balls give you an effect - you can get double score for 30sec")
    intro_text.append(
        "Blue balls give you an effect - you can get one shield for 30sec")
    intro_text.append(
        "Purple balls give you an effect - your speed will decrease for 30sec")

    while not quit:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit = True
                elif event.key == pygame.K_RIGHT:
                    if page < max_page:
                        page += 1
                elif event.key == pygame.K_LEFT:
                    if page > min_page:
                        page -= 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[1] >= 350 and mouse_pos[1] <= 450:
                    if mouse_pos[0] >= 1450 and mouse_pos[0] <= 1500:
                        if page < max_page:
                            page += 1
                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 50:
                        if page > min_page:
                            page -= 1

        if page == 1:
            screen.blit(keyboard, (0, 0))
        elif page == 2:
            for i in range(0, len(how_to_play_text)):
                write(how_to_play_text[i], "OpenSans-Regular.ttf", 40, WHITE, (750, 40*(i+1)+80))
            for i in range(0, len(intro_text)):
                write(intro_text[i], "OpenSans-Regular.ttf", 40, WHITE, (750, 40*(i+1)+400))

        write("-press space to quit-", "OpenSans-Regular.ttf", 30, WHITE, (750, 750))

        if page == min_page:
            screen.blit(right_arrow, (1450, 350))
        elif page == max_page:
            screen.blit(left_arrow, (0, 350))
        else:
            screen.blit(right_arrow, (1450, 350))
            screen.blit(left_arrow, (0, 350))

        pygame.display.update()


# 애니메이션 효과 (일시정지 애니메이션 미포함)
def animation(homeUI_icon_x, homeUI_text_x, gameUI_icon_x, gameUI_text_x, is_homeUI_ended, is_gameUI_ended, tmp, game_over, animation_start):
    gameUI_delta_x = easeOutQuint(tmp[0] * 0.01) * 100
    homeUI_delta_x = easeOutQuint(tmp[1] * 0.01) * 350
    if not game_over:
        if is_homeUI_ended[0] and not is_homeUI_ended[1]:
            tmp[1] += 1
            if 1150 + homeUI_delta_x < 1500:
                homeUI_icon_x[1] = 1150 + homeUI_delta_x
                homeUI_text_x[1] = 1460 + homeUI_delta_x
            else:
                homeUI_icon_x[1] = 1500
                homeUI_text_x[1] = 1810

            if 10 - homeUI_delta_x > -340:
                homeUI_icon_x[0] = 10 - homeUI_delta_x
                homeUI_text_x[0] = 320 - homeUI_delta_x
            else:
                homeUI_icon_x[0] = -340
                homeUI_text_x[0] = -30

            if homeUI_icon_x[1] >= 1500 and homeUI_icon_x[0] <= -340:
                is_homeUI_ended[1] = True
                is_homeUI_ended[0] = False
        if is_homeUI_ended[1]:
            tmp[0] += 1
            if 1400 + (100 - gameUI_delta_x) > 1400:
                gameUI_icon_x[1] = 1400 + (100 - gameUI_delta_x)
                gameUI_text_x[1] = 1460 + (100 - gameUI_delta_x)
            else:
                gameUI_icon_x[1] = 1400
                gameUI_text_x[1] = 1460
            if 4 - (100 - gameUI_delta_x) < 4:
                gameUI_icon_x[0] = 4 - (100 - gameUI_delta_x)
                gameUI_text_x[0] = 80 - (100 - gameUI_delta_x)
            else:
                gameUI_icon_x[0] = 4
                gameUI_text_x[0] = 80

            if gameUI_icon_x[1] <= 1400 and gameUI_icon_x[0] >= 4:
                is_gameUI_ended[0] = True
                is_gameUI_ended[1] = False
        if is_gameUI_ended[0] and is_homeUI_ended[1]:
            animation_start = False
    elif game_over:
        if not is_gameUI_ended[1] and is_gameUI_ended[0]:
            tmp[0] += 1
            if 1400 + gameUI_delta_x < 1500:
                gameUI_icon_x[1] = 1400 + gameUI_delta_x
                gameUI_text_x[1] = 1460 + gameUI_delta_x
            else:
                gameUI_icon_x[1] = 1500
                gameUI_text_x[1] = 1560

            if 4 - gameUI_delta_x > -96:
                gameUI_icon_x[0] = 4 - gameUI_delta_x
                gameUI_text_x[0] = 80 - gameUI_delta_x
            else:
                gameUI_icon_x[0] = -96
                gameUI_text_x[0] = -20

            if gameUI_icon_x[1] >= 1500 and gameUI_icon_x[0] <= -96:
                is_gameUI_ended[1] = True
                is_gameUI_ended[0] = False
        if is_gameUI_ended[1]:
            tmp[1] += 1
            if 1150 + (350 - homeUI_delta_x) > 1150:
                homeUI_icon_x[1] = 1150 + (350 - homeUI_delta_x)
                homeUI_text_x[1] = 1460 + (350 - homeUI_delta_x)
            else:
                homeUI_icon_x[1] = 1150
                homeUI_text_x[1] = 1460

            if 10 - (350 - homeUI_delta_x) < 10:
                homeUI_icon_x[0] = 10 - (350 - homeUI_delta_x)
                homeUI_text_x[0] = 320 - (350 - homeUI_delta_x)
            else:
                homeUI_icon_x[0] = 10
                homeUI_text_x[0] = 320

            if homeUI_icon_x[1] <= 1150 and homeUI_icon_x[0] >= 10:
                is_homeUI_ended[0] = True
                is_homeUI_ended[1] = False
        if is_gameUI_ended[1] and is_homeUI_ended[0]:
            animation_start = False
    return animation_start


# ------------------------게임 진행------------------------
def runGame():
    global done
    player_x = 750
    player_y = 370
    enemy_ball_x = []
    enemy_ball_y = []
    slow_ball_x = []
    slow_ball_y = []
    shield_ball_x = []
    shield_ball_y = []
    double_ball_x = []
    double_ball_y = []
    homeUI_icon_x = [10, 1150]
    homeUI_text_x = [320, 1460]
    gameUI_icon_x = [-96, 1500]
    gameUI_text_x = [-20, 1560]
    slow = [0, 0]
    shield = [0, 0]
    double = [0, 0]
    is_effect_ball_spawned = False
    is_effect_applied = [False, False, False]
    player_center = [player_x + 22.5, player_y + 15]
    score_ball_center = changeScoreBall()
    kind_of_effect = random.choice(["slow", "shield", "double"])
    j = 0
    criterion_of_effect_ball = 10  # 특수 공 생성의 기준 점수 (이 수의 배수마다 특수 공 생성)
    current_crit_of_eff_ball = criterion_of_effect_ball
    enemy_spawn_time = 0
    enemy_ball_count = 0
    velocity = 0
    base_velocity = 0
    delta_jump = 0
    delta_x_max = 3
    delta_x = 0
    g_accel = 7
    tick = 0
    score = 0
    game_over = True
    reset_cooldown_start = time.time() + 120
    can_use_reset = True
    current_time = 0
    animation_start = False
    is_homeUI_ended = [True, False]
    is_gameUI_ended = [False, True]
    writing_name = True
    nickname = ''
    tmp = [0, 0]
    pause_time = time.time()
    is_paused = False

    with open(".\score\previous_score.pickle", "rb") as fr:
        previous_score = pickle.load(fr)

    high_score = previous_score[:]
    high_score.sort(key=lambda s: s[1], reverse=True)
    pre_size = 15 if len(previous_score) > 15 else len(previous_score)
    high_score = high_score[:pre_size]

    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        tick += 1

        if game_over:
            player_x = 727
            player_y = 370
            velocity = 0
            base_velocity = 0
            delta_jump = 0
            delta_x_max = 3
            delta_x = 0
            score = 0
            can_use_reset = True
            tick = 0
            current_crit_of_eff_ball = criterion_of_effect_ball
            enemy_ball_count = 0
            slow = [0, 0]
            shield = [0, 0]
            double = [0, 0]
            current_time = 0

            for i in range(0, len(slow_ball_x)):
                del slow_ball_x[0]
                del slow_ball_y[0]
            for i in range(0, len(shield_ball_x)):
                del shield_ball_x[0]
                del shield_ball_y[0]
            for i in range(0, len(double_ball_x)):
                del double_ball_x[0]
                del double_ball_y[0]
            for i in range(0, len(enemy_ball_x)):
                del enemy_ball_x[0]
                del enemy_ball_y[0]

        if animation_start:
            animation_start = animation(homeUI_icon_x, homeUI_text_x,
                                        gameUI_icon_x, gameUI_text_x,
                                        is_homeUI_ended, is_gameUI_ended,
                                        tmp, game_over, animation_start)
        else:
            tmp = [0, 0]

        # 리셋 쿨타임
        if time.time() >= reset_cooldown_start:
            can_use_reset = True

        # ----------------------플레이어 컨트롤 부분--------------------------

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # 키 입력에 대한 이벤트 처리
            if event.type == pygame.KEYDOWN:
                if writing_name:
                    if event.key == pygame.K_BACKSPACE:
                        if len(nickname) > 0:
                            nickname = nickname[:-1]
                    elif event.key != pygame.K_RETURN:
                        if len(nickname) < 11:
                            nickname += event.unicode
                    else:
                        if nickname == """/ClearData""":
                            nickname = ''
                            clearScoreData()
                            with open(".\score\previous_score.pickle", "rb") as fr:
                                previous_score = pickle.load(fr)
                            high_score = previous_score[:]
                        writing_name = False

                    img1 = get_font("OpenSans-Regular.ttf", 30).render(nickname, True, BLACK)
                    rect1.size = img1.get_size()
                    cursor1.topleft = rect1.topright

                elif not writing_name:
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                        if game_over:
                            animation_start = True
                        if is_homeUI_ended[0]:
                            game_over = False
                        if not game_over:
                            delta_jump += 3
                    elif event.key == pygame.K_q:
                        done = True
                    elif event.key == pygame.K_i:
                        tutorial()
                    elif event.key == pygame.K_RETURN:
                        writing_name = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        delta_x += random.uniform(0.7, 1.2)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        delta_x -= random.uniform(0.7, 1.2)
                    elif event.key == pygame.K_r:
                        if can_use_reset == True:
                            score_ball_center = changeScoreBall()
                            reset_cooldown_start = time.time() + 120
                            can_use_reset = False
                    elif event.key == pygame.K_ESCAPE:
                        if game_over == 1:
                            done = True
                    elif event.key == pygame.K_p:
                        if not game_over and not animation_start:
                            if time.time() - pause_time >= 3:
                                is_paused = True
            # 마우스 클릭에 대한 이벤트 처리
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[0] >= homeUI_icon_x[1] and mouse_position[0] <= homeUI_icon_x[1] + 340:
                    if mouse_position[1] >= 530 and mouse_position[1] <= 580:
                        writing_name = True
                    if mouse_position[0] <= homeUI_icon_x[1] + 100:
                        if mouse_position[1] >= 600 and mouse_position[1] <= 700:
                            done = True
                if mouse_position[0] >= homeUI_icon_x[1] + 240 and mouse_position[0] <= homeUI_icon_x[1] + 340:
                    if mouse_position[1] >= 600 and mouse_position[1] <= 700:
                        tutorial()

        # 점수 출력
        write(f"{score}", "NotoSansKR-Black.otf", 800, WHITE, (size[0]//2, size[1]//2 - 50), alpha=50)

        # 화면 밖으로 나가면 반대에서 나옴
        if game_over == False:
            if player_y < -22:
                player_y = 782
            elif player_y > 782:
                player_y = -18
            if player_x < -20:
                player_x = 1480
            elif player_x > 1480:
                player_x = -20

            # 플레이어의 움직임
            base_velocity = (tick * g_accel / FPS)
            velocity = base_velocity - delta_jump
            if velocity >= 20:
                velocity = 20
                delta_jump = base_velocity - 20
            elif velocity <= -10:
                delta_jump = base_velocity + 10

            if delta_x >= delta_x_max:
                delta_x = delta_x_max
            elif delta_x <= -1 * delta_x_max:
                delta_x = -1 * delta_x_max

            player_y += velocity
            player_x += delta_x

            player_center = [player_x + 22.5, player_y + 15]

            # --------------------------플레이어 이외의 공 제어--------------------------

            # 점수 공에 닿았을 때
            if distance(score_ball_center, player_center) < 22:
                score_ball_center = changeScoreBall()
                score += 1
                enemy_ball_count += 1
                if double[0] == 1:
                    score += 1
                # 더해진 시간(sec)만큼 새로 생성된 장애물에 죽지 않음 -> 0.5초 예정
                enemy_spawn_time = time.time() + 0.5
                enemy_ball_x.append(random.randint(0, 1500 - 21))
                enemy_ball_y.append(random.randint(0, 800 - 14))
                kind_of_effect = random.choice(["slow", "shield", "double"])

            # 장애물 공에 닿았을 때
            while j < enemy_ball_count:
                if distance((enemy_ball_x[j] + 10.5, enemy_ball_y[j] + 7), player_center) < 22:
                    game_over = True
                    if shield[0] == 1:
                        game_over = False
                        shield[0] = 0
                        del enemy_ball_x[j]
                        del enemy_ball_y[j]
                        enemy_ball_count -= 1
                        is_effect_applied[1] = False
                    if game_over:
                        previous_score.insert(0, [f"{nickname}", score])
                        high_score = previous_score[:]
                        high_score.sort(key=lambda s: s[1], reverse=True)
                        pre_size = 15 if len(
                            previous_score) > 15 else len(previous_score)
                        high_score = high_score[:pre_size]
                        with open(".\score\previous_score.pickle", "wb") as fw:
                            pickle.dump(previous_score, fw)
                        animation_start = True
                    break
                j += 1
            j = 0

            # 생성된지 얼마 안된(0.5초 이내) 장에물에 사망 시 장애물 재생성 (사망 판정 X)
            if time.time() <= enemy_spawn_time and enemy_ball_count > 0:
                if distance((enemy_ball_x[enemy_ball_count - 1] + 10.5, enemy_ball_y[enemy_ball_count - 1] + 7), player_center) < 22:
                    game_over = False
                    animation_start = False
                    enemy_ball_x[enemy_ball_count -
                                 1] = random.randint(0, 1500 - 21)
                    enemy_ball_y[enemy_ball_count -
                                 1] = random.randint(0, 800 - 14)
                    # 더해진 시간(sec)만큼 새로 생성된 장애물에 죽지 않음 -> 0.5초 예정
                    enemy_spawn_time = time.time() + 0.5

            # 일정 점수에 도달 시 특수 공 스폰
            if score >= current_crit_of_eff_ball and not is_effect_ball_spawned:
                current_crit_of_eff_ball += criterion_of_effect_ball
                if kind_of_effect == "slow":  # slow 스폰
                    is_effect_ball_spawned = True
                    slow_ball_x.append(random.randint(0, 1500 - 21))
                    slow_ball_y.append(random.randint(0, 800 - 14))
                elif kind_of_effect == "shield":  # shield 스폰
                    is_effect_ball_spawned = True
                    shield_ball_x.append(random.randint(0, 1500 - 21))
                    shield_ball_y.append(random.randint(0, 800 - 14))
                elif kind_of_effect == "double":  # double 스폰
                    is_effect_ball_spawned = True
                    double_ball_x.append(random.randint(0, 1500 - 21))
                    double_ball_y.append(random.randint(0, 800 - 14))
            if score < current_crit_of_eff_ball:
                is_effect_ball_spawned = False

            screen.blit(
                score_ball, (score_ball_center[0] - 10.5, score_ball_center[1] - 7))

        time_list = [slow[1], shield[1], double[1]]
        # 특수 공의 효과 유무 저장 (리스트 : [적용 여부, 시작 시간])
        slow = isEffectBallTouched(
            (slow_ball_x, slow_ball_y), player_center, "slow", is_effect_applied, time_list)
        shield = isEffectBallTouched(
            (shield_ball_x, shield_ball_y), player_center, "shield", is_effect_applied, time_list)
        double = isEffectBallTouched(
            (double_ball_x, double_ball_y), player_center, "double", is_effect_applied, time_list)

        current_time = time.time()
        if slow[0] == 1:
            if current_time <= slow[1]:  # slow효과 적용 & slow 제한시간 값 변경
                delta_x_max = 1
                is_effect_applied[0] = True
            else:
                delta_x_max = 3
                slow[0] = 0
                is_effect_applied[0] = False
        if shield[0] == 1:
            if current_time <= shield[1]:  # shield 제한시간 값 변경
                is_effect_applied[1] = True
            else:
                shield[0] = 0
                is_effect_applied[1] = False
        if double[0] == 1:
            if current_time <= double[1]:  # double 제한시간 값 변경
                is_effect_applied[2] = True
            else:
                double[0] = 0
                is_effect_applied[2] = False

        # 특수 공 프린트
        for i in range(0, len(slow_ball_x)):
            screen.blit(slow_ball, (slow_ball_x[i], slow_ball_y[i]))
        for i in range(0, len(shield_ball_x)):
            screen.blit(shield_ball, (shield_ball_x[i], shield_ball_y[i]))
        for i in range(0, len(double_ball_x)):
            screen.blit(double_ball, (double_ball_x[i], double_ball_y[i]))

        # 장애물 공 프린트
        for i in range(0, enemy_ball_count):
            screen.blit(enemy_ball, (enemy_ball_x[i], enemy_ball_y[i]))

        # 특수효과 지속 시간 표기
        # ㄴ효과 아이콘
        screen.blit(slow_icon, (gameUI_icon_x[1], 10))
        screen.blit(shield_icon, (gameUI_icon_x[1], 50))
        screen.blit(double_icon, (gameUI_icon_x[1], 90))

        # ㄴslow 지속시간
        slow_cooltime = slow[1] - current_time + 1
        if slow_cooltime <= 0:
            slow_cooltime = 0
        write(f"{int(slow_cooltime)}", "NotoSansKR-Black.otf", 25, WHITE, (gameUI_text_x[1], 23), alpha=150)

        # ㄴshield 지속시간
        shield_cooltime = shield[1] - current_time + 1
        if shield_cooltime <= 0:
            shield_cooltime = 0
        write(f"{int(shield_cooltime)}", "NotoSansKR-Black.otf", 25, WHITE, (gameUI_text_x[1], 63), alpha=150)

        # ㄴdouble 지속시간
        double_cooltime = double[1] - current_time + 1
        if double_cooltime <= 0:
            double_cooltime = 0
        write(f"{int(double_cooltime)}", "NotoSansKR-Black.otf", 25, WHITE, (gameUI_text_x[1], 103), alpha=150)

        # reblit 아이콘 및 쿨타임
        screen.blit(score_reblit, (gameUI_icon_x[0] + 9, 10))
        reblit_cooltime = reset_cooldown_start - time.time() + 1
        if reblit_cooltime <= 0 or can_use_reset == True:
            reblit_cooltime = 0
        write(f"{int(reblit_cooltime)}", "NotoSansKR-Black.otf", 25, WHITE, (gameUI_text_x[0], 28), alpha=150)

        # 점수판 출력
        board_text_y = 70
        screen.blit(leaderboard, (homeUI_icon_x[0] - 1, 10))
        screen.blit(pre_score_board, (homeUI_icon_x[1] + 1, 10))
        pre_size = 15 if len(previous_score) > 15 else len(previous_score)

        # 순위 / 순서 출력
        for i in range(1, 16):
            write(f"#{i}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[0] - 300, board_text_y - 14), "topleft")
            write(f"#{i}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[1] - 300, board_text_y - 14), "topleft")
            board_text_y += 30
        board_text_y = 70

        for i in range(0, pre_size):
            # 리더보드 랭킹 출력
            write(f"{high_score[i][1]}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[0], board_text_y))
            write(f"{high_score[i][0]}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[0]-140, board_text_y))

            # 최근 플레이 기록 출력
            write(f"{previous_score[i][1]}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[1], board_text_y))
            write(f"{previous_score[i][0]}", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[1]-140, board_text_y))
            board_text_y += 30

        # 리더보드 / 최근 플레이 기록에 데이터가 부족하면 채워 넣기
        for i in range(0, 15 - pre_size):
            write("0", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[0], board_text_y))
            write("0", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[1], board_text_y))
            write("None", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[0]-140, board_text_y))
            write("None", "OpenSans-Regular.ttf", 20, BLACK, (homeUI_text_x[1]-140, board_text_y))
            board_text_y += 30

        # 이름 입력칸, 나가는 아이콘, 도움말 아이콘
        screen.blit(quit_button, (homeUI_icon_x[1], 600))
        screen.blit(intro_button, (homeUI_icon_x[1] + 240, 600))
        pygame.draw.rect(screen, (200, 200, 200),
                         (homeUI_icon_x[1], 530, 340, 50))
        img1 = get_font("OpenSans-Regular.ttf", 30).render(nickname, True, BLACK)
        rect1 = img1.get_rect()
        rect1.topleft = (homeUI_icon_x[1] + 10, 535)
        cursor1 = pygame.Rect(rect1.topright, (3, rect1.height))

        screen.blit(img1, rect1)
        if writing_name and time.time() % 1 > 0.5:
            pygame.draw.rect(screen, RED, cursor1)
        if len(nickname) == 0:
            write("Enter Name", "OpenSans-Regular.ttf", 30, BLACK, (homeUI_text_x[1]-300, 534), "topleft", 100)

        # 플레이어 공 프린트
        screen.blit(player_ball, (player_x, player_y))

        # 일시정지
        if not is_paused:
            screen.blit(continue_button, (gameUI_icon_x[0] + 9, 60))
        else:
            screen.blit(pause_button, (gameUI_icon_x[0] + 10, 60))
            pygame.display.update()
            is_paused = False
            pause()
            pause_time = time.time()
        pygame.display.update()


runGame()
pygame.quit()