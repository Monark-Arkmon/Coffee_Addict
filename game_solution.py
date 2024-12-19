import tkinter as tk
from tkinter import messagebox, simpledialog
from game import start_game
from keybinds import show_keybinds
from leaderboard import show_leaderboard
from load import load_game_details
from gameguide import show_game_guide
from bosskeyfunction import bosskey

# Define global variables
player_name = ""
chosen_difficulty = ""


# Prompts the player to enter their nam e
def enter_name():
    global player_name
    player_name = simpledialog.askstring("Input", "Please enter your name:")
    if player_name:
        messagebox.showinfo("Name Entered", f"Welcome, {player_name}!")


# Checks if the player has entered a name and starts the game
def game_check():
    global player_name
    if not player_name:
        messagebox.showwarning(
            "Name Required", "Please enter your name before starting the game."
        )
    else:

        # Checks for the various cheat codes from player
        if player_name == "Arkapratim":
            mode = "Enable_1"
        elif player_name == "Mondal":
            mode = "Enable_2"
        elif player_name == "Arkapratim Mondal":
            mode = "Enable_3"
        else:
            mode = "Disable"
        start_game(player_name, mode)


# Creates the main menu of the game
def create_main_menu():
    global root

    # Initialize the main application window
    root = tk.Tk()
    root.title("The Coffee Addict")
    root.geometry("1280x720")
    root.configure(bg="#4c3010")

    root.bind("<Control-b>", lambda event: bosskey(root))

    # Display the game logo
    logo = tk.PhotoImage(file="Logo.png")
    image_label = tk.Label(root, image=logo, bg="#4c3010")
    image_label.pack(pady=10)

    # Add a button to prompt the player to enter their name
    name_button = tk.Button(
        root, text="Enter Name", command=enter_name,
        width=11, bg="#4c3010", fg="white")
    name_button.pack(pady=10)

    # Add a button to start the game
    start_button = tk.Button(
        root, text="Start Game", command=game_check,
        width=11, bg="#4c3010", fg="white")
    start_button.pack(pady=10)

    # Add a button to show/change keybinds
    keybinds_button = tk.Button(
        root, text="Keybinds", command=lambda: show_keybinds(root),
        width=11, bg="#4c3010", fg="white")
    keybinds_button.pack(pady=10)

    # Add a button to display the leaderboard
    leaderboard_button = tk.Button(
        root, text="Leaderboard", command=show_leaderboard,
        width=11, bg="#4c3010", fg="white"
    )
    leaderboard_button.pack(pady=10)

    # Add a button to load a saved game
    load_game_button = tk.Button(
        root, text="Load Game", command=lambda: load_game_details(root),
        width=11, bg="#4c3010", fg="white"
    )
    load_game_button.pack(pady=10)

    # Add a button to show the game guide
    guide_button = tk.Button(
        root, text="Game Guide", command=show_game_guide,
        width=11, bg="#4c3010", fg="white")
    guide_button.pack(pady=10)

    # Add a button to quit the game
    quit_button = tk.Button(
        root, text="Quit", command=root.quit,
        width=11, bg="#4c3010", fg="white")
    quit_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_main_menu()
