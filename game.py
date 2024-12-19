import tkinter as tk
import random
import datetime
from keybinds import Keybinds
from leaderboard import add_score
from gameguide import show_game_guide

# Global variables
power_ups = {
    "Shield": {"active": False, "cooldown": 0, "cost": 10,
               "duration": 15000, "timer": None, "time_left": 0},
    "Slow Down": {"active": False, "cooldown": 0, "cost": 15,
                  "duration": 10000, "timer": None, "time_left": 0},
    "Multiplier": {"active": False, "cooldown": 0, "cost": 20,
                   "duration": 10000, "Multiplier": 3, "timer": None,
                   "time_left": 0}}

score_multiplier = 1
game_over_flag = False
min_speed, max_speed, score_increment = 0, 0, 0
game_paused = False
pause_menu = None


# Collision Detection for falling beans
def check_collision(canvas, bean, coffee_cup):
    bean_bbox = canvas.bbox(bean)
    cup_bbox = canvas.bbox(coffee_cup)
    if bean_bbox and cup_bbox:
        return (bean_bbox[2] > cup_bbox[0] and
                bean_bbox[0] < cup_bbox[2] and
                bean_bbox[3] > cup_bbox[1] and
                bean_bbox[1] < cup_bbox[3])
    return False


# Defines the movement of the cup on key-press
def move_cup(canvas, coffee_cup, dx, dy):

    # Check if canvas is still valid
    if canvas.winfo_exists():
        canvas.move(coffee_cup, dx, dy)
        cup_coords = canvas.coords(coffee_cup)
        x, y = cup_coords[0], cup_coords[1]
        if x < 0:
            canvas.coords(coffee_cup, 0, y)
        elif x > 960 - coffee_cup_image.width():
            canvas.coords(coffee_cup, 960 - coffee_cup_image.width(), y)
        if y < 0:
            canvas.coords(coffee_cup, x, 0)
        elif y > 750:
            canvas.coords(coffee_cup, x, 750)
    else:
        pass


# Ends the game, displays the game-over screen, and binds restart/exit actions
def game_over(canvas, score_label, lives_label, game_window,
              score, player_name, cheat_status):
    global game_over_flag  # Use the global flag to stop the game loop
    game_over_flag = True

    # Create a new window for the game over screen
    game_over_window = tk.Toplevel(game_window)
    game_over_window.overrideredirect(True)
    game_over_window.title("Game Over")
    game_over_window.geometry("300x200+560+530")

    game_over_label = tk.Label(game_over_window, text="Game Over",
                               font=("Helvetica", 16), fg="red")
    game_over_label.pack(pady=15)

    restart_button = tk.Button(game_over_window, text="Restart Game",
                               command=lambda: restart_game(score_label,
                                                            lives_label,
                                                            game_window,
                                                            player_name,
                                                            cheat_status),
                               width=20)
    restart_button.pack(pady=15)

    exit_button = tk.Button(game_over_window, text="Exit Game",
                            command=lambda: exit_game(game_window),
                            width=20)
    exit_button.pack(pady=15)

    game_over_window.mainloop()

    # Save the score to the leaderboard
    add_score(player_name, score)


# Exit/destory main game window
def exit_game(game_window):
    game_window.destroy()


# Resets Score/Lives, destroys current window and restarts main game function
def restart_game(score_label, lives_label,
                 game_window, player_name, cheat_status):
    global score, lives, game_over_flag, power_ups
    score = 0
    lives = 5
    game_over_flag = False
    score_label.config(text=f"Score: {score}")
    lives_label.config(text=f"Lives: {lives}")
    start_game(player_name, cheat_status, old_game_window=game_window)


# Adjusts difficulty settings based on the player's score and cheat status
def difficulty_settings(score, cheat_status):
    global min_speed, max_speed, score_increment

    # Adjust speed for slow down boost
    if power_ups["Slow Down"]["active"]:
        min_speed, max_speed, score_increment = 1, 3, 1
        return min_speed, max_speed, score_increment
    else:
        pass

    # Set bean speed based on score
    if int(score) <= 15:
        min_speed, max_speed, score_increment = 1, 3, 1
    elif 15 < int(score) <= 60:
        min_speed, max_speed, score_increment = 2, 6, 2
    elif 60 < int(score) <= 90 and cheat_status == "Disable":
        min_speed, max_speed, score_increment = 3, 9, 3
    else:
        min_speed, max_speed, score_increment = 4, 12, 4

    return min_speed, max_speed, score_increment


# Displays messages temporarily on canvas when the difficulty increases
def difficulty_message(score, canvas):
    if power_ups["Slow Down"]["active"]:
        min_speed, max_speed, score_increment = 1, 3, 1
        return min_speed, max_speed, score_increment
    else:
        pass

    if int(score) == 15 or int(score) == 16:
        message = canvas.create_text(480, 400,
                                     text="Difficulty Increases!",
                                     font=("Helvetica", 16), fill="Yellow")
        canvas.after(2000, lambda: canvas.delete(message))
    elif int(score) == 60 or int(score) == 61:
        message = canvas.create_text(480, 400,
                                     text="Difficulty Increases!",
                                     font=("Helvetica", 16), fill="Yellow")
        canvas.after(2000, lambda: canvas.delete(message))
    elif int(score) == 90 or int(score) == 91:
        message = canvas.create_text(480, 400,
                                     text="Max Difficulty Reached!",
                                     font=("Helvetica", 16), fill="Yellow")
        canvas.after(2000, lambda: canvas.delete(message))
    else:
        pass


# Main game functiion, initializes and starts the game
def start_game(player_name, cheat_status,
               initial_score=0, initial_lives=5,
               coffee_bean_positions=None,
               cup_position=None, old_game_window=None):
    global score, lives, power_ups

    # Re-initialize power-up values when starting game each time
    power_ups = {"Shield": {"active": False,
                            "cooldown": 0,
                            "cost": 10,
                            "duration": 15000,
                            "timer": None,
                            "time_left": 0},
                 "Slow Down": {"active": False,
                               "cooldown": 0,
                               "cost": 15,
                               "duration": 10000,
                               "timer": None,
                               "time_left": 0},
                 "Multiplier": {"active": False,
                                "cooldown": 0,
                                "cost": 20,
                                "duration": 10000,
                                "Multiplier": 4,
                                "timer": None,
                                "time_left": 0}}
    global score_multiplier, game_over_flag, score_increment

    # Reset game state variables
    game_over_flag = False
    score = initial_score
    lives = initial_lives

    # Destroys the previous game window after restarting
    if old_game_window:
        old_game_window.destroy()

    # Create the main game window
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.geometry("1440x900")

    # Load images for game objects
    global coffee_bean_image, coffee_cup_image, background_image
    coffee_bean_image = tk.PhotoImage(file="Coffee_Bean.png")
    coffee_cup_image = tk.PhotoImage(file="Coffee_Cup.png")
    background_image = tk.PhotoImage(file="Cafe_BG.png")

    # Create gameplay and UI frames
    gameplay_frame = tk.Frame(game_window, width=960,
                              height=900, bg="lightblue")
    gameplay_frame.pack(side="left", fill="both", expand=True)

    ui_frame = tk.Frame(game_window, width=480,
                        height=900, bg="lightgrey")
    ui_frame.pack(side="right", fill="both", expand=True)

    # Create the game canvas
    canvas = tk.Canvas(gameplay_frame, bg="lightblue", width=960, height=800)
    canvas.pack(pady=50)
    canvas.create_image(0, 0, anchor="nw", image=background_image)

    # Initialize the coffee cup position
    if cup_position:
        cup_x, cup_y = cup_position
    else:
        cup_x = 480 - coffee_cup_image.width() // 2
        cup_y = 750

    coffee_cup = canvas.create_image(cup_x, cup_y, anchor="nw",
                                     image=coffee_cup_image)

    # Create score and lives labels in the UI frame
    score_label = tk.Label(ui_frame, text=f"Score: {score}",
                           font=("Helvetica", 16), bg="lightgrey")
    score_label.pack(pady=20)

    lives_label = tk.Label(ui_frame, text=f"Lives: {lives}",
                           font=("Helvetica", 16), bg="lightgrey")
    lives_label.pack(pady=20)

    # Functions to toggle and resume the pause state
    def toggle_pause(canvas, game_window):
        global game_paused

        # Unbind cup key-binds as game is paused
        game_paused = True
        canvas.unbind_all(f"<{Keybinds['move_up']}>")
        canvas.unbind_all(f"<{Keybinds['move_down']}>")
        canvas.unbind_all(f"<{Keybinds['move_left']}>")
        canvas.unbind_all(f"<{Keybinds['move_right']}>")
        show_pause_menu(game_window)

    # Displays the pause menu
    def show_pause_menu(game_window):
        global pause_menu
        pause_menu = tk.Toplevel(game_window)
        pause_menu.overrideredirect(True)
        pause_menu.geometry("300x200+560+530")
        pause_label = tk.Label(pause_menu, text="Game Paused",
                               font=("Helvetica", 16))
        pause_label.pack(pady=20)
        resume_button = tk.Button(pause_menu, text="Resume",
                                  command=lambda: resume_game())
        resume_button.pack(pady=10)
        help_button = tk.Button(pause_menu, text="Help",
                                command=lambda: show_game_guide())
        help_button.pack(pady=20)

    # Resumes the game after pausing
    def resume_game():
        global game_paused, pause_menu
        game_paused = False
        pause_menu.destroy()

        # Rebind movement keys
        canvas.bind_all(f"<{Keybinds['move_up']}>",
                        lambda event: move_cup(canvas, coffee_cup, 0, -20))
        canvas.bind_all(f"<{Keybinds['move_down']}>",
                        lambda event: move_cup(canvas, coffee_cup, 0, 20))
        canvas.bind_all(f"<{Keybinds['move_left']}>",
                        lambda event: move_cup(canvas, coffee_cup, -20, 0))
        canvas.bind_all(f"<{Keybinds['move_right']}>",
                        lambda event: move_cup(canvas, coffee_cup, 20, 0))

        # Restart power-up timers if active
        for p_type, power_up in power_ups.items():
            if power_up["active"]:
                power_up["timer"] = canvas.after(1000,
                                                 update_power_up_time,
                                                 p_type)
            elif power_up["cooldown"] > 0:
                power_up["timer"] = canvas.after(1000,
                                                 start_cooldown,
                                                 p_type)
            else:
                pass
        game_loop()

    # Initialize coffee beans (use loaded positions if available)
    beans = {}
    if coffee_bean_positions:
        for i, (x, y) in enumerate(coffee_bean_positions):
            bean = canvas.create_image(x, y, image=coffee_bean_image)
            speed = random.randint(2, 10)
            beans[bean] = speed
    else:
        for i in range(5):
            start_x = random.randint(0, 960 - coffee_bean_image.width())
            bean = canvas.create_image(start_x, 0, image=coffee_bean_image)
            speed = random.randint(2, 10)
            beans[bean] = speed

    # Bind movement keys
    canvas.bind_all(f"<{Keybinds['move_up']}>",
                    lambda event: move_cup(canvas, coffee_cup, 0, -20))
    canvas.bind_all(f"<{Keybinds['move_down']}>",
                    lambda event: move_cup(canvas, coffee_cup, 0, 20))
    canvas.bind_all(f"<{Keybinds['move_left']}>",
                    lambda event: move_cup(canvas, coffee_cup, -20, 0))
    canvas.bind_all(f"<{Keybinds['move_right']}>",
                    lambda event: move_cup(canvas, coffee_cup, 20, 0))

    # Game loop logic
    def game_loop():
        global score, lives, game_over_flag, score_increment, game_paused

        game_window.bind("<Control-b>",
                         lambda event: bosskey(canvas, game_window))

        # Stop the loop if the game is paused or over
        if game_paused or game_over_flag:
            return

        # Apply difficulty speeds and score boosts
        (min_speed,
         max_speed,
         score_increment) = difficulty_settings(score, cheat_status)
        difficulty_message(score, canvas)

        # Update bean positions and check for collisions
        for bean, speed in beans.items():
            if cheat_status == "Disable":
                canvas.move(bean, 0, random.randint(min_speed, max_speed))
            else:
                canvas.move(bean, 0, random.randint(1, 3))
            bean_bbox = canvas.bbox(bean)

            if bean_bbox:
                x1, y1, x2, y2 = bean_bbox

                # Check for collision, inc. score, restart bean fall randomly
                if y2 < 800:
                    if check_collision(canvas, bean, coffee_cup):
                        score = int(score)
                        score += score_increment * score_multiplier
                        score_label.config(text=f"Score: {score}")
                        start_x = random.randint(0,
                                                 960-coffee_bean_image.width())
                        canvas.moveto(bean, start_x, 0)
                        beans[bean] = random.randint(2, 10)

                # Bean hits bottom, -1 life if shield not active
                else:
                    start_x = random.randint(0,
                                             960-coffee_bean_image.width())
                    canvas.moveto(bean, start_x, 0)
                    beans[bean] = random.randint(2, 10)
                    if not power_ups["Shield"]["active"]:
                        lives = int(lives)
                        lives -= 1
                        lives_label.config(text=f"Lives: {lives}")
                    if lives <= 0:
                        game_over(canvas, score_label, lives_label,
                                  game_window, score, player_name,
                                  cheat_status)
                    else:
                        pass

        # Repeat game loop after 50 ms
        canvas.after(50, game_loop)

    game_loop()

    # Activates the specified power-up if conditions are met
    def power_on(p_type):
        global score, score_multiplier, game_paused

        # Proceed only if the game is not paused
        if not game_paused:
            power_up = power_ups[p_type]

            # Check if enough points and power-up not on cooldown
            if score >= power_up["cost"] and power_up["cooldown"] == 0:
                # Deduct the cost from the score
                score -= power_up["cost"]
                # Mark the power-up as active
                power_up["active"] = True
                # Set the active duration, //100
                power_up["time_left"] = power_up["duration"] // 1000
                update_ui()
                # Power-up activated mssg
                message = canvas.create_text(480, 400,
                                             text=f'{p_type} Activated!',
                                             font=("Helvetica", 16),
                                             fill="green")
                canvas.after(2000, lambda: canvas.delete(message))
                # Set score multiplier if power up is activated
                if p_type == "Multiplier":
                    score_multiplier = power_up["Multiplier"]
                power_up["timer"] = canvas.after(1000,
                                                 update_power_up_time,
                                                 p_type)
                power_up["cooldown"] = 30
                update_ui()

    # Deactivates the specified power-up after its duration ends
    def depower_on(p_type):
        global score_multiplier, game_paused
        if not game_paused:
            power_up = power_ups[p_type]
            power_up["active"] = False
            if p_type == "Multiplier":
                score_multiplier = 1
            power_up["timer"] = None
            start_cooldown(p_type)
            update_ui()

    # Decrements the cooldown timer for a power-up every second
    def start_cooldown(p_type):
        global game_paused

        # Proceed only if the game is not paused
        if not game_paused:
            power_up = power_ups[p_type]

            if power_up["cooldown"] > 0:
                power_up["cooldown"] -= 1
                update_ui()
                # Call this function again after 1 second
                power_up["timer"] = canvas.after(1000,
                                                 start_cooldown,
                                                 p_type)
            # Reset cooldown
            else:
                power_up["cooldown"] = 0
                update_ui()

    # Decrements the active timer for a power-up every second
    def update_power_up_time(p_type):
        global game_paused

        # Proceed only if the game is not paused
        if not game_paused:
            power_up = power_ups[p_type]
            if power_up["time_left"] > 0:
                power_up["time_left"] -= 1
                update_ui()
                # Call this function again after 1 second
                power_up["timer"] = canvas.after(1000,
                                                 update_power_up_time,
                                                 p_type)
            # Deactivate the power-up if time is up
            else:
                depower_on(p_type)

    # Updates the UI labels for power-ups to show their status
    def update_ui():
        global game_paused

        # Proceed only if the game is not paused
        if not game_paused:
            # Update Shield Label
            if power_ups['Shield']['active']:
                s_txt = f"{power_ups['Shield']['time_left']}s left"
            else:
                if power_ups['Shield']['cooldown'] == 0:
                    s_txt = "Shield: Ready"
                else:
                    s_txt = f"Cooldown: {power_ups['Shield']['cooldown']}s"
            shield_label.config(text=s_txt)

            # Update Slow Down Label
            if power_ups['Slow Down']['active']:
                sl_txt = f"{power_ups['Slow Down']['time_left']}s left"
            else:
                if power_ups['Slow Down']['cooldown'] == 0:
                    sl_txt = "Slow Down: Ready"
                else:
                    sl_txt = f"Cooldown: {power_ups['Slow Down']['cooldown']}s"
            slow_label.config(text=sl_txt)

            # Update Multiplier Label
            if power_ups['Multiplier']['active']:
                m_txt = f"{power_ups['Multiplier']['time_left']}s left"
            else:
                if power_ups['Multiplier']['cooldown'] == 0:
                    m_txt = "Multiplier: Ready"
                else:
                    m_txt = f"Cooldown: {power_ups['Multiplier']['cooldown']}s"
            multiplier_label.config(text=m_txt)

    # Saves the current game state to a txt file
    def save_game(player_name, score, lives, coffee_beans, cup_position):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format coffee beans and cup positions as strings
        beans_positions = "|".join([f"{x},{y}" for x, y in coffee_beans])
        cup_position_str = f"{cup_position[0]},{cup_position[1]}"

        game_data = [player_name, str(score),
                     str(lives), str(beans_positions),
                     cup_position_str, current_time]
        line = ", ".join(game_data)
        # Append the game data to the file
        with open("game_scores.txt", "a") as file:
            file.write(line + "\n")

        # Display a confirmation message on the canvas temporarily
        message = canvas.create_text(480, 400, text="Game Saved Successfully!",
                                     font=("Helvetica", 16), fill="green")
        canvas.after(2000, lambda: canvas.delete(message))

    # Function to get the current positions of all coffee beans
    def get_bean_positions(beans):
        bean_positions = {}
        for bean in beans.keys():
            bean_coords = canvas.coords(bean)  # Get center position
            if bean_coords:
                bean_positions[bean] = bean_coords
        return bean_positions

# Function to save game with current positions
    def save_game_state(player_name, score, lives, beans, cup_id):
        # Get positions of coffee beans
        coffee_positions = get_bean_positions(beans)

        # Get cup position
        cup_coords = canvas.coords(cup_id)
        if cup_coords:
            cup_center = cup_coords  # Center of cup (x, y)

        # Call save_game function with positions
        save_game(
            player_name=player_name,
            score=score,
            lives=lives,
            coffee_beans=list(coffee_positions.values()),
            cup_position=cup_center
        )

    # Buttons work only if game is not paused
    if not game_paused:
        # Shield Power-Up
        shield_button = tk.Button(ui_frame, text="Activate Shield",
                                  width=15,
                                  command=lambda: power_on("Shield"))
        shield_button.pack(pady=10)
        shield_label = tk.Label(ui_frame, text="Shield: Ready",
                                font=("Helvetica", 12), bg="lightgrey")
        shield_label.pack(pady=10)
        shield_cost_label = tk.Label(ui_frame, text="Cost: 10 Points",
                                     font=("Helvetica", 10), bg="lightgrey")
        shield_cost_label.pack(pady=5)

        # Spacer for extra space between power-ups
        spacer1 = tk.Label(ui_frame, text="", bg="lightgrey")
        spacer1.pack(pady=10)

        # Slow Down Power-Up
        slow_down_button = tk.Button(ui_frame, text="Activate Slow Down",
                                     width=15,
                                     command=lambda: power_on("Slow Down"))
        slow_down_button.pack(pady=10)
        slow_label = tk.Label(ui_frame, text="Slow Down: Ready",
                              font=("Helvetica", 12), bg="lightgrey")
        slow_label.pack(pady=10)
        slow_down_cost_label = tk.Label(ui_frame, text="Cost: 15 Points",
                                        font=("Helvetica", 10), bg="lightgrey")
        slow_down_cost_label.pack(pady=5)

        # Spacer for extra space between power-ups
        spacer2 = tk.Label(ui_frame, text="", bg="lightgrey")
        spacer2.pack(pady=10)

        # Multiplier Power-Up
        multiplier_button = tk.Button(ui_frame, text="Activate Multiplier",
                                      width=15,
                                      command=lambda: power_on("Multiplier"))
        multiplier_button.pack(pady=10)
        multiplier_label = tk.Label(ui_frame, text="Multiplier: Ready",
                                    font=("Helvetica", 12), bg="lightgrey")
        multiplier_label.pack(pady=10)
        multiplier_cost_label = tk.Label(ui_frame, text="Cost: 20 Points",
                                         font=("Helvetica", 10),
                                         bg="lightgrey")
        multiplier_cost_label.pack(pady=5)

        # Spacer for extra space between power-ups and save/pause buttons
        spacer3 = tk.Label(ui_frame, text="", bg="lightgrey")
        spacer3.pack(pady=15)

        # Help Label
        help_label = tk.Label(ui_frame,
                              text="Game Guide (Help) in Pause Menu",
                              font=("Helvetica", 12), bg="lightgrey")
        help_label.pack(pady=10)

        # Pause Button
        pause_button = tk.Button(ui_frame, text="Pause",
                                 width=15,
                                 command=lambda: toggle_pause(canvas,
                                                              game_window))
        pause_button.pack(pady=20)

        # Save Game Button
        save_button = tk.Button(ui_frame, text="Save Game",
                                width=15,
                                command=lambda: save_game_state(player_name,
                                                                score,
                                                                lives,
                                                                beans,
                                                                coffee_cup))
        save_button.pack(pady=10)
    else:
        pass

    # Activates a cheat code that sets the player's score and lives
    def cheat_code():
        global score, lives
        if cheat_status == "Enable_1":
            score = 0
            lives = 100
        elif cheat_status == "Enable_2":
            score = 600
            lives = 5
        else:
            score = 600
            lives = 100

        # Update the UI labels
        score_label.config(text=f"Score: {score}")
        lives_label.config(text=f"Lives: {lives}")

    # Activate the cheat code if the cheat mode is enabled
    if not cheat_status == "Disable":
        cheat_code()
    else:
        pass

    # Hide the game window, show a screen when activated
    def bosskey(canvas, game_window):
        global game_paused
        # Hide the main game window
        game_window.withdraw()

        # Create a new window for the boss key screen
        boss_window = tk.Toplevel()
        boss_window.title("Error")
        boss_window.geometry("1920x1080")
        boss_window.config(bg="white")
        Boss_BG = tk.PhotoImage(file="BosskeyBG.png")
        canvas = tk.Canvas(boss_window, width=1920, height=1080)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=Boss_BG)
        canvas.image = Boss_BG
        toggle_pause(canvas, game_window)

        # Restores the main game window and closes the boss key screen
        def return_to_game(event=None):
            boss_window.destroy()
            game_window.deiconify()
            pause_menu.deiconify()

        boss_window.bind("<Control-r>", return_to_game)
        boss_window.protocol("WM_DELETE_WINDOW", return_to_game)
