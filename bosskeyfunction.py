import tkinter as tk


# Hides the main game window and opens a boss key screen.
def bosskey(root):
    # Hide the main game window
    root.withdraw()

    # Create a new window to display the boss key screen
    boss_window = tk.Toplevel()
    boss_window.title("Error")
    boss_window.geometry("1920x1080")
    boss_window.config(bg="white")

    Boss_BG = tk.PhotoImage(file="BosskeyBG.png")
    canvas = tk.Canvas(boss_window, width=1920, height=1080)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=Boss_BG)

    # Keep a reference to avoid garbage collection
    canvas.image = Boss_BG

    # Close the boss key window and restore the main game window.
    def return_to_game(event=None):
        boss_window.destroy()
        root.deiconify()

    boss_window.bind("<Control-r>", return_to_game)
    boss_window.protocol("WM_DELETE_WINDOW", return_to_game)
