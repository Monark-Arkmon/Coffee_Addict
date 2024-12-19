import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for combobox
from bosskeyfunction import bosskey

# Default keybinds
Keybinds = {
    'move_left': 'a',
    'move_right': 'd',
    'move_up': 'w',
    'move_down': 's',
}


# Function to show the current keybinds
def show_keybinds(root):
    keybind_window = tk.Toplevel(root)
    keybind_window.title("Keybinds")
    keybind_window.geometry("300x500")
    keybind_window.configure(bg="#4c3010")
    keybind_window.bind(
        "<Control-b>", lambda event: bosskey(keybind_window)
    )

    label = tk.Label(
        keybind_window,
        text="Current Keybinds",
        font=("Arial", 14),
        bg="#4c3010",
        fg="white",
    )
    label.pack(pady=10)

    # Display the current keybinds
    for action, key in Keybinds.items():
        label = tk.Label(
            keybind_window,
            text=f"{action.replace('_', ' ').title()}: {key}",
            bg="#4c3010",
            fg="white",
        )
        label.pack(pady=5)

    # Dropdown to select action to update
    label_select = tk.Label(
        keybind_window,
        text="Select action to update:",
        font=("Arial", 10),
        bg="#4c3010",
        fg="white",
    )
    label_select.pack(pady=10)

    # Create a combobox to select the action to update
    action_list = list(Keybinds.keys())
    action_combobox = ttk.Combobox(
        keybind_window, values=action_list, state="readonly"
    )
    action_combobox.pack(pady=5)
    action_combobox.set(action_list[0])

    # Label for instructions on entering a new key
    label_key = tk.Label(
        keybind_window,
        text="Press a key (letter or arrow key) to bind:",
        font=("Arial", 10),
        bg="#4c3010",
        fg="white",
    )
    label_key.pack(pady=10)

    # Entry field to display the selected key
    key_entry = tk.Entry(keybind_window)
    key_entry.pack(pady=5)

    # Bind letter and arrow keys to the entry field
    key_entry.bind("<Key>", lambda event: on_key_press(event, key_entry))

    # Button to update the keybind
    update_button = tk.Button(
        keybind_window,
        text="Update Keybind",
        command=lambda: update_keybind(
            action_combobox.get(), key_entry.get(), keybind_window
        ),
        bg="#4c3010",
        fg="white",
    )
    update_button.pack(pady=10)

    # Button to reset the keybinds to default (WASD)
    reset_button = tk.Button(keybind_window,
                             text="Reset Keybinds",
                             command=lambda: reset_keybinds(keybind_window),
                             bg="#4c3010", fg="white")
    reset_button.pack(pady=10)

    # Reset keybinds to WASD
    def reset_keybinds(window):
        Keybinds['move_left'] = 'a'
        Keybinds['move_right'] = 'd'
        Keybinds['move_up'] = 'w'
        Keybinds['move_down'] = 's'

        messagebox.showinfo("Keybinds Reset",
                            "Keybinds have been reset to default (WASD).")

        window.destroy()


# Function for key press and updating the entry field
def on_key_press(event, entry_widget):
    if event.keysym in ['Left', 'Right', 'Up', 'Down']:
        # Use the keysym for arrow keys
        key = event.keysym
    else:
        # Use the alphabets for regular keys
        key = event.char
    # Only update if there's a key
    if key:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, key)
    return "break"


# Function to update the keybind
def update_keybind(action, new_key, window):
    if new_key in Keybinds.values():
        messagebox.showwarning(
            "Key Already Taken",
            '''This key is already bound to another action.
            Please choose a different key.'''
        )
        return

    if action in Keybinds:
        if new_key:

            # Update the keybind in the Keybinds dictionary
            Keybinds[action] = new_key
            messagebox.showinfo(
                "Keybind Updated",
                "Keybind Updated Successfully",
            )
            window.destroy()
        else:

            # If no key was entered, show a warning
            messagebox.showwarning(
                "Invalid Key",
                "Please enter a valid key."
            )
    else:
        messagebox.showwarning(
            "Invalid Action",
            "Invalid action selected. Please try again."
        )
