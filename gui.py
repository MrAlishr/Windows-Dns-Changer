import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, PhotoImage
from dns_manager import get_active_adapter, set_dns, unset_dns
from config_manager import load_config, save_config


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
    """ Create the GUI elements and place them in the window using grid layout """
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    config = load_config()
    row_num = 0
    for key, value in config.items():
        btn = tk.Button(window, text=f"{key}: {value[0]}, {value[1]}", image=button_image, compound="center",
                        command=lambda key=key: update_dns_settings(key))
        btn.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
        window.grid_rowconfigure(row_num, weight=1)
        row_num += 1

    add_button = tk.Button(window, text="Add DNS Profile", command=add_dns_profile, highlightbackground='green',
                           foreground='white')
    add_button.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
    window.grid_rowconfigure(row_num, weight=1)
    row_num += 1

    unset_button = tk.Button(window, text="Unset DNS", command=lambda: update_dns_settings('unset'),
                             highlightbackground='red', foreground='white')
    unset_button.grid(row=row_num, column=0, sticky="ew", padx=10, pady=5)
    window.grid_rowconfigure(row_num, weight=1)

    window.grid_columnconfigure(0, weight=1)  # Make the column expand as the window resizes


def update_dns_settings(choice):
    """ Update the DNS settings based on user choice """
    config = load_config()
    adapter = get_active_adapter()
    if adapter:
        if choice in config:
            primary, secondary = config[choice]
            result = set_dns(adapter, primary, secondary)
            messagebox.showinfo("Success", f"DNS set to {primary} and {secondary}\n{result}")
        elif choice == 'unset':
            result = unset_dns(adapter)
            messagebox.showinfo("Success", "DNS has been unset.\n" + result)
        else:
            messagebox.showerror("Error", "Invalid choice")
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
    load_resources()  # Load resources dynamically
    window.title("DNS Changer")
    create_gui_elements(window)
    window.mainloop()


if __name__ == "__main__":
    create_gui()
