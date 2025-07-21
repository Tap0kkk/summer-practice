import tkinter as tk
from gui_elements import create_main_interface
from handlers import load_csv_file

root = tk.Tk()
root.title("Анализ подержанных авто UK")
root.geometry("700x400")

# Центрирование окна
window_width = 700
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

create_main_interface(root, load_csv_file)

root.mainloop()