import tkinter as tk
from tkinter import ttk
from handlers import show_filtered_table, show_recommendations

def create_main_interface(root, load_csv_callback):
    info_text = tk.StringVar()
    root.info_text = info_text
    tk.Label(root, textvariable=info_text).pack(pady=10)

    tk.Button(root, text="Загрузить CSV", command=lambda: load_csv_callback(root)).pack(pady=5)

    tk.Label(root, text="Фильтрация").pack(pady=10)
    frame = tk.Frame(root)
    frame.pack()

    # Переменные
    year_var = tk.StringVar()
    fuel_var = tk.StringVar()
    owners_var = tk.StringVar()

    # Глобальные ссылки
    root.year_var = year_var
    root.fuel_var = fuel_var
    root.owners_var = owners_var

    # Выпадающие меню
    tk.Label(frame, text="Год регистрации:").grid(row=0, column=0)
    root.year_combo = ttk.Combobox(frame, textvariable=year_var, width=15)
    root.year_combo.grid(row=0, column=1)

    tk.Label(frame, text="Тип топлива:").grid(row=1, column=0)
    root.fuel_combo = ttk.Combobox(frame, textvariable=fuel_var, width=15)
    root.fuel_combo.grid(row=1, column=1)

    tk.Label(frame, text="Кол-во владельцев:").grid(row=2, column=0)
    root.owners_combo = ttk.Combobox(frame, textvariable=owners_var, width=15)
    root.owners_combo.grid(row=2, column=1)

    # Кнопки
    tk.Button(root, text="Показать таблицу", command=lambda: show_filtered_table(root)).pack(pady=10)
    tk.Button(root, text="Вывод рекомендаций", command=lambda: show_recommendations(root)).pack()