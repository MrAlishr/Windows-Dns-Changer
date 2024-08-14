#  /*******************************************************************************
#   *
#   *  * Copyright (c)  2024.
#   *  * All Credits Goes to MrAlishr
#   *  * Email : Alishariatirad@gmail.com
#   *  * Github: github.com/MrAlishr
#   *  * Telegram : Alishrr
#   *  *
#   *
#   ******************************************************************************/

import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage

from config_manager import load_config, save_config
from dns_manager import get_active_adapter, set_dns, unset_dns, async_ping_dns


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, relative_path)
    print("Attempting to access:", full_path)  # Debugging to see the actual path accessed
    return full_path


def load_resources():
    """ Load images from resources dynamically, allowing for PyInstaller bundling. """
    global bg_image, button_image
    bg_image = PhotoImage(file=resource_path("assets/background.png"))
    button_image = PhotoImage(file=resource_path("assets/button.png"))


def create_gui_elements(window):
    """ Create GUI elements with improved styling """
    window.title("DNS Changer")
    config = load_config()  # Load DNS configurations

    row_num = 0
    for key, value in config.items():
        btn_text = f"{key}: {value[0]}, {value[1]}"
        btn = tk.Button(window, text=btn_text, font=('Helvetica', 12, 'bold'), pady=10, background='pale green')
        btn.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
        window.grid_rowconfigure(row_num, weight=1)

        # Update button text asynchronously as pings complete
        def update_button_text(latency, b=btn, k=key, v=value):
            b.config(text=f"{k}: {v[0]}, {v[1]} - Latency: {latency}")

        async_ping_dns(value[0],
                       lambda latency, b=btn, k=key, v=value: window.after(0, update_button_text, latency, b, k, v))

        row_num += 1

    # Add DNS Profile button
    add_button = tk.Button(window, text="Add DNS Profile", command=add_dns_profile,
                           highlightbackground='green', foreground='white', background='cyan',
                           font=('Helvetica', 12, 'bold'), pady=10)
    add_button.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
    window.grid_rowconfigure(row_num, weight=1)
    row_num += 1

    # Unset DNS button
    unset_button = tk.Button(window, text="Unset DNS", command=lambda: update_dns_settings('unset'),
                             highlightbackground='green', foreground='white', background='cyan',
                             font=('Helvetica', 12, 'bold'), pady=10)
    unset_button.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
    window.grid_rowconfigure(row_num, weight=1)

    window.grid_columnconfigure(0, weight=1)  # Make the column expand as the window resizes


def update_dns_settings(choice):
    """ Update the DNS settings based on user choice """
    adapter = get_active_adapter()
    if adapter:
        if choice == 'unset':
            result = unset_dns(adapter)
            messagebox.showinfo("Success", "DNS has been unset.\n" + result)
        else:
            primary, secondary = load_config()[choice]
            result = set_dns(adapter, primary, secondary)
            messagebox.showinfo("Success", f"DNS set to {primary} and {secondary}\n{result}")
    else:
        messagebox.showerror("Error", "No active network adapter found")


def add_dns_profile():
    """ Add a custom DNS profile via dialogues """
    config = load_config()
    name = simpledialog.askstring("Profile Name", "Enter a name for the new DNS profile:")
    if not name:
        return  # User cancelled the operation
    primary = simpledialog.askstring("Primary DNS", "Enter the primary DNS IP:")
    if not primary:
        return  # User cancelled the operation
    secondary = simpledialog.askstring("Secondary DNS", "Enter the secondary DNS IP:")
    if not secondary:
        return  # User cancelled the operation

    config[name] = (primary, secondary)
    save_config(config)
    refresh_gui(window)  # Refresh the GUI within the app


def refresh_gui(window):
    """ Refresh the GUI by rebuilding the GUI elements """
    for widget in window.winfo_children():
        widget.destroy()
    create_gui_elements(window)


def create_gui():
    """ Main function to create GUI window """
    window = tk.Tk()
    window.title("DNS Changer")

    # Load window to get dimensions
    window.update_idletasks()  # Updates the window so you get correct info
    width = window.winfo_width()
    height = window.winfo_height()
    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # Calculate the center coordinates
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Set the geometry of tkinter frame
    window.geometry(f'+{x}+{y}')

    create_gui_elements(window)
    window.mainloop()


if __name__ == "__main__":
    create_gui()
