import tkinter as tk
from tkinter import messagebox
from game import start_game
from bosskeyfunction import bosskey


def load_saved_games():
    # Load saved game data from the game_scores.txt file.
    global saved_games
    saved_games = []
    try:
        with open("game_scores.txt", "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                name = parts[0]
                score = int(parts[1])
                lives = int(parts[2])
                beans_data = parts[3]
                cup_data = parts[4]
                timestamp = parts[5]

                # Parse coffee bean positions
                coffee_beans = []
                for pos in beans_data.split("|"):
                    positions = pos.split(",")
                    bean_tuple = tuple(map(float, positions))
                    coffee_beans.append(bean_tuple)

                # Parse cup position
                cup_position = []
                cup_positions = cup_data.split(",")
                for pos in cup_positions:
                    cup_position.append(float(pos))

                # Append tuple of all data
                saved_games.append((name, score, lives,
                                    coffee_beans, cup_position,
                                    timestamp))
    except FileNotFoundError:
        pass


def load_game_details(root):
    # Create a dropdown menu to select a saved game.
    load_saved_games()
    if not saved_games:
        messagebox.showinfo("Error", "There are no saved games to load.")
        return

    # Create a new window for selecting saved game
    load_window = tk.Toplevel(root)
    load_window.title("Load Game")
    load_window.geometry("500x400")
    load_window.configure(bg="#4c3010")
    load_window.bind("<Control-b>", lambda event: bosskey(load_window))

    label = tk.Label(load_window, text="Select a saved game",
                     bg="#4c3010", fg="white")
    label.pack(pady=10)

    # Dropdown menu to select saved game
    game_names = [
        f"| Name: {game[0]} | Score: {game[1]} | Lives: {game[2]} | "
        f"Date/Time: {game[5]} |" for game in saved_games
    ]
    game_var = tk.StringVar(value=game_names[0])
    game_menu = tk.OptionMenu(load_window, game_var, *game_names)
    game_menu.pack(pady=20)

    # Loads the selected game and starts it
    def on_load():
        selected_game = game_var.get()

        # Find the selected game's index
        index = game_names.index(selected_game)

        # Extract the selected game's details from the saved_games list
        selected_game_data = saved_games[index]
        selected_game_name = selected_game_data[0]
        selected_game_score = selected_game_data[1]
        selected_game_lives = selected_game_data[2]
        selected_game_beans = selected_game_data[3]  # Coffee beans positions
        selected_game_cup = selected_game_data[4]    # Cup position

        # Start the game with the loaded details, including positions
        start_game(
            selected_game_name,
            "Disable",  # Default cheat status for loaded games
            selected_game_score,
            selected_game_lives,
            selected_game_beans,
            selected_game_cup
        )

    load_button = tk.Button(load_window,
                            text="Load Game",
                            command=on_load,
                            bg="#4c3010", fg="white")
    load_button.pack(pady=10)

    cancel_button = tk.Button(load_window,
                              text="Cancel",
                              command=load_window.destroy,
                              bg="#4c3010", fg="white")
    cancel_button.pack(pady=10)
