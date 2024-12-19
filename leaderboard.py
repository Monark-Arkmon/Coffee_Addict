import tkinter as tk
from tkinter import messagebox
from bosskeyfunction import bosskey


# Function to load leaderboard data from the file
def load_leaderboard():
    leaderboard_data = []
    try:
        with open("leaderboard.txt", "r") as file:
            for line in file:
                line = line.strip()

                # Check if the line contains both name and score
                if ": " in line:
                    name, score = line.split(": ")
                    try:
                        leaderboard_data.append((name, int(score)))
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return leaderboard_data


# Function to add or update a score in the leaderboard
def add_score(name, score):
    leaderboard_data = load_leaderboard()

    # Check if the player's name already exists in the leaderboard
    found = False
    for i in range(len(leaderboard_data)):
        if leaderboard_data[i][0] == name:
            # If the new score is higher, update the score
            if score > leaderboard_data[i][1]:
                leaderboard_data[i] = (name, score)
            found = True
            break

    # Add score and name if name doesn't exist
    if not found:
        leaderboard_data.append((name, score))

    # Sort the leaderboard by score in descending order
    leaderboard_data.sort(key=lambda x: x[1], reverse=True)

    # Save the updated leaderboard back to the file
    with open("leaderboard.txt", "w") as file:
        for name, score in leaderboard_data:
            file.write(f"{name}: {score}\n")


# Function to display the leaderboard
def show_leaderboard():
    # Create a new top-level window for the leaderboard
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("300x500")
    leaderboard_window.configure(bg="#4c3010")
    leaderboard_window.bind(
        "<Control-b>", lambda event: bosskey(leaderboard_window)
    )
    leaderboard_data = load_leaderboard()

    if not leaderboard_data:
        messagebox.showinfo("Leaderboard", "No scores available.")
        return

    # Initialize the ranking index
    index = 1
    for player in leaderboard_data:
        name, score = player
        # Create a label for each player and their score
        tk.Label(
            leaderboard_window,
            text=f"{index}. {name}: {score}",
            bg="#4c3010",
            fg="white"
        ).pack()
        index += 1
