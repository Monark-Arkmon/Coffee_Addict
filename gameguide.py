import tkinter as tk
from bosskeyfunction import bosskey


def show_game_guide():
    # Create a new top-level window for the guide
    guide_window = tk.Toplevel()
    guide_window.title("Game Guide")
    guide_window.geometry("800x600")
    guide_window.configure(bg="#4c3010")
    guide_window.bind("<Control-b>", lambda event: bosskey(guide_window))

    # Create a Text widget to display the guide text
    guide_text = tk.Text(
        guide_window,
        wrap=tk.WORD,
        width=90,
        height=30,
        font=("Helvetica", 12),
        bg="#4c3010",
        fg="#f1e0c6"
    )
    guide_text.pack(padx=20, pady=20)

    # Game guide content
    guide_content = (
        """
        Coffee Bean Catcher Game Guide
        ------------------------------------------------

        Objective:
        --------------
        - Catch falling coffee beans with your coffee cup.
        - Earn points for each bean you catch.
        - Avoid letting beans fall to the ground, or you will lose lives.
        - Activate power-ups to help you during the game.
        - Aim for the highest score!

        Gameplay Controls:
        ----------------------------
        - Move Up: Arrow Key / W (Move the coffee cup upwards)
        - Move Down: Arrow Key / S (Move the coffee cup downwards)
        - Move Left: Arrow Key / A (Move the coffee cup left)
        - Move Right: Arrow Key / D (Move the coffee cup right)
        - Pause Game: P (Pause the game and open the pause menu)
        - Resume Game: P again or click "Resume" in the pause menu
        - Restart Game: Press R to restart after game over

        Power-Ups:
        -----------------
        1. Shield:
           - Cost: 10 points
           - Effect: Protects you from losing lives when beans fall.
           - Duration: 15 seconds
           - Cooldown: 30 seconds

        2. Slow Down:
           - Cost: 15 points
           - Effect: Slows down falling beans for a short period.
           - Duration: 10 seconds
           - Cooldown: 30 seconds

        3. Multiplier:
           - Cost: 20 points
           - Effect: Doubles points for each bean caught during the power-up.
           - Duration: 10 seconds
           - Cooldown: 30 seconds

        Difficulty Levels:
        -----------------------
        - Up to 15 points: Easy difficulty.
        - 16 to 60 points: Medium difficulty.
        - 61 to 90 points: Hard difficulty.
        - 90+ points: Max difficulty.

        Strategy Tips:
        --------------------
        - Use power-ups wisely! Activate them when you're in a tough spot.
        - Be strategic and focus on catching more beans at once.
        - Use the Multiplier power-up in a good position to rack up points!

        Saving & Leaderboard:
        ---------------------------------
        - Save your game by clicking "Save Game".

        FAQs:
        ---------
        Q: How do I use power-ups?
        A: Click the buttons to activate them.

        Q: What happens when I run out of lives?
        A: The game ends and you can restart.

        Q: Can I pause the game?
        A: Yes, you can use the Pause button on the right side.

        Q: How do I change controls?
        A: You can modify key bindings in the main menu.

        Q: How do I activate the Boss Key?
        A: Press Ctrl + B to instantly hide the game and display a fake screen.

        Q: How do I return from the Boss Key screen?
        A: Press Ctrl + R or click the close button on the decoy screen.

        Good luck and have fun catching those coffee beans!
        """
    )

    # Insert the guide content into the text widget
    guide_text.insert(tk.END, guide_content)

    # Make the text widget read-only
    guide_text.config(state=tk.DISABLED)
