from imports import *

## -------- PyMunk Initialization --------
space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, GRAVITY  # Set its gravity

# Game
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()

## Common To both modes
p_img = skins[0]
player_speed_factor = 1.2  ## Experimental value
max_speed = 100
player = DynamicBall((WW // 2, WH // 2), 10, 0, p_img, space)
flag = VictoryFlag((WW - 100, WH - 100))


## -------------------- Some functions --------------------
def load_level_by_num(name, i, is_survival=False):
    if not is_survival:
        try:
            return Levels.levels[i - 1]
        except IndexError:
            return Levels.levels[0]
    elif is_survival:
        try:
            return Levels.levels[i - 1]
        except IndexError:
            return "finish"


def remove_lines_and_balls_of_level_by_number(i, lines, balls):
    '''
    Returns empty list, assign this to the lines and balls list
    '''
    for rl in lines:
        space.remove(rl.body, rl.shape)  # Extremely Necessary
    for rb in balls:
        space.remove(rb.body, rb.shape)  # Extremely Necessary
    return []  # Deleting the lines of the prev level


def reset_player_pos(player, WW, WH, current_level):
    if player.body.position[0] > WW or player.body.position[0] < 0:
        player.body.position = current_level.dict["player"][0]  ## Player
        player.body.velocity = (0, 0)
    if player.body.position[1] > WH:
        player.body.position = current_level.dict["player"][0]  ## Player
        player.body.velocity = (0, 0)


## ========================= Survival Mode =========================
def survival_mode(screen, current_level):
    score = 0
    if User_data.save is not None:
        data = User_data.get_save()
        score = data['score']
        current_level = load_level_by_num('', int(data['level']))
    ## -------------------- Initializing Game --------------------
    st_time = 0  # Time
    death_time = 0  # Death time
    clicked = False

    ## -------------------- Initializing Level --------------------
    player.image = p_img  ## Player
    player.body.position = current_level.dict["player"][0]  ## Player
    player.body.velocity = (0, 0)  ## Player
    flag.rect.bottomleft = current_level.dict["victory"][0]  ## Flag
    moves = current_level.dict["moves"]  ## Moves
    ## Lines
    lines = []
    line_number = 0
    for s, e in zip(current_level.dict["start"],
                    current_level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
        l = StaticLine(s, e, current_level.dict["thickness"][line_number], space)
        lines.append(l)
        line_number += 1
    line_number = 0
    ## Dummy Balls
    balls = []
    try:  ## Incase there are no balls ;)
        for p, r in zip(current_level.dict["ball_center"],
                        current_level.dict["ball_radius"]):  # can't use nested cuz it makes wierd things happen xD
            b = DynamicBallWithColor(p, 0, 0, r, space)
            balls.append(b)
    except KeyError:
        pass
    ## Portals
    portals = []
    try:
        for s, e in zip(current_level.dict["portal_start"],
                        current_level.dict["portal_end"]):  # can't use nested cuz it makes wierd things happen xD
            p = Portal(s, e, 32)
            portals.append(p)
    except KeyError:
        pass
    ## Coins
    coins = []
    coins_collected_in_current_level = 0
    try:
        print(current_level)
        for p in current_level.dict["coin_pos"]:
            c = Coins(p)
            coins.append(c)
    except KeyError:
        pass

    ## ---------------------------------------- MAIN LOOP ----------------------------------------
    while True:
        screen.fill(Themes.active_theme.background)
        ## -------------------- Time and stuff --------------------
        if st_time == 0:

            # load level
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
            player.body.position = current_level.dict["player"][0]  ## Player
            player.body.velocity = (0, 0)  ## Player
            flag.rect.bottomleft = current_level.dict["victory"][0]  ## Flag
            moves = current_level.dict["moves"]  ## Moves
            ## Lines

            lines = []
            line_number = 0
            for s, e in zip(current_level.dict["start"],
                            current_level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
                l = StaticLine(s, e, current_level.dict["thickness"][line_number], space)
                lines.append(l)
                line_number += 1
            line_number = 0
            ## Dummy Balls
            balls = []
            try:  ## Incase there are no balls ;)
                for p, r in zip(current_level.dict["ball_center"],
                                current_level.dict[
                                    "ball_radius"]):  # can't use nested cuz it makes wierd things happen xD
                    b = DynamicBallWithColor(p, 0, 0, r, space)
                    balls.append(b)
            except KeyError:
                pass
            ## coins
            coins = []
            try:
                for p in current_level.dict["coin_pos"]:
                    c = Coins(p)
                    coins.append(c)
            except KeyError:
                pass
            ## Portals
            portals = []
            try:
                for s, e in zip(current_level.dict["portal_start"],
                                current_level.dict[
                                    "portal_end"]):  # can't use nested cuz it makes wierd things happen xD
                    p = Portal(s, e, 32)
                    portals.append(p)
            except KeyError:
                pass

            st_time = time.time()
        if death_time != 0:
            if death_time - int(time.time()) + 10 <= 0:
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                return ['death', 'dead', score]

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time != 0:
                screen.blit(
                    small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c),
                    (WW - 50, 31))

        ## -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if moves == 0 and event.key == pygame.K_r:
                    lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                    current_level = load_level_by_num('noname', 1)
                    player.body.angular_velocity = 0
                    return ['death', 'dead', score]

        ## -------------------- Events --------------------
        if moves == 0:
            heading_text = medium_font.render("PRESS 'R' TO quit", True, Themes.active_theme.font_c)
            heading_text.set_alpha(200)
            heading_rect = heading_text.get_rect()
            heading_rect.center = (WW // 2, WH // 2)
            screen.blit(heading_text, heading_rect.topleft)

        ## -------------------- Player --------------------

        # Drawing the direction in which a force will b applied
        mx, my = pygame.mouse.get_pos()
        distx = mx - player.body.position.x
        disty = my - player.body.position.y
        pygame.draw.aaline(screen, Themes.active_theme.mouse_line, player.body.position, (mx, my), 10)

        # Adding a velocity to the ball if it clicked
        if clicked:
            if moves > 0:
                moves -= 1
                player.body.velocity = (distx * player_speed_factor, disty * player_speed_factor)

            if moves == 0 and death_time == 0:  # Start Death timer if not already running
                death_time = int(time.time())
            clicked = False

        # Limiting the player's velocity (so that it doesn't flies across like hell xD)
        if distx > max_speed:
            distx = max_speed
        if disty > max_speed:
            disty = max_speed

        # reseting player's
        reset_player_pos(player, WW, WH, current_level)

        ## -------------------- Lines, balls and Portals --------------------
        for line in lines:
            line.draw(screen, Themes.active_theme.platform_c)
        for ball in balls:
            ball.draw(screen, Themes.active_theme.bouncing_ball_c)
        for portal in portals:
            portal.draw(screen, space)
            portal.teleport(player)
            for ball in balls:
                portal.teleport(ball)

        ## -------------------- Flag --------------------
        flag.draw(screen)
        player.draw(screen)
        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            score += 100 + int(25 * moves) + int(25 - (time.time() - st_time))*4
            st_time = 0
            death_time = 0
            current_level = load_level_by_num('noname', current_level.number + 1, is_survival=True)
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
            player.body.angular_velocity = 0

            score_data = score_screen(screen, score, data={"score": score, "level": current_level.number}, 
                                                     coins=coins_collected_in_current_level)

            if score_data[0] == 'quit': return ['quit']
            if score_data[0] == 'welcome': return ['welcome']
            if current_level == "finish": return ['death', 'completed', score]

        ## -------------------- Coins --------------------
        for coin in coins:
            coins_collected_in_current_level += coin.collect(player.rect)
            coin.draw(screen)
            # coins_collected_in_current_level += coin.collect(player.rect)           ## Go to it's definition to add the coin increment system
            # print(coins_collected_in_current_level)

        ## -------------------- In-game UI --------------------
        # Displaying the number of moves left
        moves_text = small_font.render('Moves Left: ' + str(moves), True, Themes.active_theme.font_c)
        moves_rect = moves_text.get_rect()
        moves_rect.center = (WW // 2, 50)
        screen.blit(moves_text, moves_rect.topleft)
        # Displaying the level
        level_text = small_font.render(f"level: {current_level.number}", True, Themes.active_theme.font_c)
        screen.blit(level_text, (20, 31))

        ## -------------------- Updating--------------------
        space.step(1.5 / FPS)
        clock.tick(FPS)
        pygame.display.update()


## ========================= Campaign Mode =========================
def campaign(screen, current_level):
    ## -------------------- Initializing Game --------------------
    score = 0
    st_time = 0  # Time
    death_time = 0  # Death time
    clicked = False

    ## -------------------- Initializing Level --------------------
    player.image = p_img  ## Player
    player.body.position = current_level.dict["player"][0]  ## Player
    player.body.velocity = (0, 0)  ## Player
    flag.rect.bottomleft = current_level.dict["victory"][0]  ## Flag
    moves = current_level.dict["moves"]  ## Moves
    ## Lines
    lines = []
    line_number = 0
    for s, e in zip(current_level.dict["start"],
                    current_level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
        l = StaticLine(s, e, current_level.dict["thickness"][line_number], space)
        lines.append(l)
        line_number += 1
    line_number = 0
    ## Dummy Balls
    balls = []
    try:  ## Incase there are no balls ;)
        for p, r in zip(current_level.dict["ball_center"],
                        current_level.dict["ball_radius"]):  # can't use nested cuz it makes wierd things happen xD
            b = DynamicBallWithColor(p, 0, 0, r, space)
            balls.append(b)
    except KeyError:
        pass
    ## Portals
    portals = []
    try:
        for s, e in zip(current_level.dict["portal_start"],
                        current_level.dict["portal_end"]):  # can't use nested cuz it makes wierd things happen xD
            p = Portal(s, e, 32)
            portals.append(p)
    except KeyError:
        pass
    # ## Coins
    # coins = []
    # coins_collected_in_current_level = 0
    # try:
    #     for p in current_level.dict["coin_pos"]:
    #         c = Coins(p)
    #         coins.append(c)
    # except KeyError:
    #     pass

    ## ---------------------------------------- MAIN LOOP ----------------------------------------
    while True:
        screen.fill(Themes.active_theme.background)
        ## -------------------- Time and stuff --------------------
        if st_time == 0:

            # load level
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
            player.body.position = current_level.dict["player"][0]  ## Player
            player.body.velocity = (0, 0)  ## Player
            flag.rect.bottomleft = current_level.dict["victory"][0]  ## Flag
            moves = current_level.dict["moves"]  ## Moves
            ## Lines
            lines = []
            line_number = 0
            for s, e in zip(current_level.dict["start"],
                            current_level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
                l = StaticLine(s, e, current_level.dict["thickness"][line_number], space)
                lines.append(l)
                line_number += 1
            line_number = 0
            ## Dummy Balls
            balls = []
            try:  ## Incase there are no balls ;)
                for p, r in zip(current_level.dict["ball_center"],
                                current_level.dict[
                                    "ball_radius"]):  # can't use nested cuz it makes wierd things happen xD
                    b = DynamicBallWithColor(p, 0, 0, r, space)
                    balls.append(b)
            except KeyError:
                pass
            ## Portals
            portals = []
            try:
                for s, e in zip(current_level.dict["portal_start"],
                                current_level.dict[
                                    "portal_end"]):  # can't use nested cuz it makes wierd things happen xD
                    p = Portal(s, e, 32)
                    portals.append(p)
            except KeyError:
                pass

            st_time = time.time()
        if death_time != 0:
            if death_time - int(time.time()) + 10 <= 0:
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                temp_death_data = campaign_death_screen(screen)
                if temp_death_data[0] == 'quit':
                    return ['quit']
                elif temp_death_data[0] == 'level_map':
                    return ['campaign', 'select']
                if temp_death_data[0] == 'restart':
                    return ['campaign', 'continue', current_level.number]

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time != 0:
                screen.blit(
                    small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c),
                    (WW - 50, 31))

        ## -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if moves == 0 and event.key == pygame.K_r:
                    lines = balls = remove_lines_and_balls_of_level_by_number(current_level, lines, balls)
                    player.body.angular_velocity = 0
                    temp_death_data = campaign_death_screen(screen)
                    if temp_death_data[0] == 'quit':
                        return ['quit']
                    elif temp_death_data[0] == 'level_map':
                        return ['campaign', 'select']
                    if temp_death_data[0] == 'restart':
                        return ['campaign', 'continue', current_level.number]

        ## -------------------- Player --------------------
        player.draw(screen)
        # Drawing the direction in which a force will b applied
        mx, my = pygame.mouse.get_pos()
        distx = mx - player.body.position.x
        disty = my - player.body.position.y
        pygame.draw.aaline(screen, Themes.active_theme.mouse_line, player.body.position, (mx, my), 10)

        # Adding a velocity to the ball if it clicked
        if clicked:
            if moves > 0:
                moves -= 1
                player.body.velocity = (distx * player_speed_factor, disty * player_speed_factor)

            if moves == 0 and death_time == 0:  # Start Death timer if not already running
                death_time = int(time.time())
            clicked = False

        # Limiting the player's velocity (so that it doesn't flies across like hell xD)
        if distx > max_speed:
            distx = max_speed
        if disty > max_speed:
            disty = max_speed

        # reseting player's position
        reset_player_pos(player, WW, WH, current_level)

        ## -------------------- Lines, balls and Portals --------------------
        for line in lines:
            line.draw(screen, Themes.active_theme.platform_c)
        for ball in balls:
            ball.draw(screen, Themes.active_theme.bouncing_ball_c)
        for portal in portals:
            portal.draw(screen, space)
            portal.teleport(player)
            for ball in balls:
                portal.teleport(ball)

        ## -------------------- Flag --------------------
        flag.draw(screen)
        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            score += 100 + int(float(100 * current_level.dict['moves'] / (current_level.dict['moves'] - moves)) / float(
                time.time() - st_time))
            st_time = 0
            death_time = 0
            if current_level.number == User_data.current_level:
                DB.update_level_progress(str(current_level.number + 1))
            current_level = load_level_by_num('noname', current_level.number + 1)
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level, lines, balls)
            player.body.angular_velocity = 0

            next_data = campaign_continue_screen(screen)
            if next_data[0] == 'quit':
                return ['quit']
            if next_data[0] == 'level_map':
                return ['campaign', 'select']
            if next_data[0] == 'continue':
                return ['campaign', 'continue', current_level.number]
        ## -------------------- Coins --------------------
        # for coin in coins:
        #     coins_collected_in_current_level += coin.collect(player.rect
        #     coin.draw(screen)

        ## -------------------- In-game UI --------------------
        # Displaying the number of moves left
        moves_text = small_font.render('Moves Left: ' + str(moves), True, Themes.active_theme.font_c)
        moves_rect = moves_text.get_rect()
        moves_rect.center = (WW // 2, 50)
        screen.blit(moves_text, moves_rect.topleft)
        # Displaying the level
        level_text = small_font.render(f"level: {current_level.number}", True, Themes.active_theme.font_c)
        screen.blit(level_text, (20, 31))

        ## -------------------- Updating--------------------
        space.step(1.5 / FPS)
        clock.tick(FPS)
        pygame.display.update()


for error in errors:
    if error == "no name":
        temp_to_do = name_screen(screen)
        if temp_to_do == 'quit':
            to_do[0] = 'quit'
        else:
            User_data.name = DB.fetch_name()
# Main Loop
while True:
    if to_do[0] == 'game':
        to_do = game_select_screen(screen)

    elif to_do[0] == 'welcome':
        to_do = welcome_screen(screen)

    elif to_do[0] == 'survival':
        to_do = survival_mode(screen, load_level_by_num('noname', 1))

    elif to_do[0] == 'settings':
        to_do = settings_screen(screen)

    elif to_do[0] == 'campaign':
        if to_do[1] == 'continue':
            level_num = to_do[2]
        else:
            level_num = level_select_screen(screen, number_buttons)

        if level_num == 'back':
            to_do = ['game']
        elif level_num == 'quit':
            to_do = ['quit']
        else:
            to_do = campaign(screen, load_level_by_num('noname', level_num))

    elif to_do[0] == 'themes':
        to_do = theme_screen(screen)

    elif to_do[0] == 'leaderboard':
        to_do = leaderboard_screen(screen)

    elif to_do[0] == 'death':
        to_do = death_screen(screen, to_do[1], to_do[2])

    elif to_do[0] == 'ball':
        to_do = skin_select_screen(screen)
        p_img = to_do[1]

    elif to_do[0] == 'quit':
        break

pygame.quit()
