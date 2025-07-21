import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

df = pd.DataFrame()

def load_csv_file(root):
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        root.info_text.set(f"Загружено {df.shape[0]} строк, {df.shape[1]} столбцов.")
        update_filters(root)

def update_filters(root):
    root.year_combo['values'] = sorted(df['registration_year'].dropna().unique())
    root.fuel_combo['values'] = sorted(df['fuel_type'].dropna().unique())
    root.owners_combo['values'] = sorted(df['previous_owners'].dropna().unique())

def show_filtered_table(root):

    if df.empty:
        messagebox.showinfo("Нет данных", "Сначала загрузите CSV-файл.")
        return

    year = root.year_var.get()
    fuel = root.fuel_var.get()
    owners = root.owners_var.get()

    filtered = df.copy()

    # Фильтрация с проверками
    try:
        if year.strip():
            filtered = filtered[filtered['registration_year'].astype(str) == year.strip()]
        if fuel.strip():
            filtered = filtered[filtered['fuel_type'] == fuel.strip()]
        if owners.strip():
            filtered = filtered[filtered['previous_owners'].astype(str) == owners.strip()]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при фильтрации: {e}")
        return

    if filtered.empty:
        messagebox.showinfo("Результат", "Нет записей по заданным фильтрам.")
        return

    # Создаем окно с результатами
    top = tk.Toplevel(root)
    top.title("Результаты фильтрации")
    tree = ttk.Treeview(top, columns=list(filtered.columns), show='headings')
    for col in filtered.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for _, row in filtered.iterrows():
        tree.insert('', 'end', values=list(row))
    tree.pack(fill=tk.BOTH, expand=True)


def show_recommendations(root):
    if df.empty:
        messagebox.showinfo("Нет данных", "Сначала загрузите CSV-файл.")
        return

    # Получаем фильтры из интерфейса
    year = root.year_var.get()
    fuel = root.fuel_var.get()
    owners = root.owners_var.get()

    # Применяем фильтры
    filtered = df.copy()

    try:
        if year.strip():
            filtered = filtered[filtered['registration_year'].astype(str) == year.strip()]
        if fuel.strip():
            filtered = filtered[filtered['fuel_type'].astype(str).str.lower().str.strip() == fuel.strip().lower()]
        if owners.strip():
            filtered = filtered[filtered['previous_owners'].astype(str) == owners.strip()]
    except Exception as e:
        messagebox.showerror("Ошибка фильтрации", f"Ошибка при применении фильтров: {e}")
        return

    if filtered.empty:
        messagebox.showinfo("Рекомендации", "Нет автомобилей по выбранным фильтрам.")
        return

    # Готовим рекомендации по отфильтрованным данным
    recs = []
    try:

        avg_price = df['price'].mean(skipna=True)

        if filtered['price'].mean(skipna=True) > avg_price:
            recs.append("Цены на выбранные авто выше средней, ищите варианты с меньшим пробегом или 1 владельцем.")

        fuel_counts = filtered['fuel_type'].value_counts()
        if fuel_counts.get('diesel', 0) > fuel_counts.get('petrol', 0):
            recs.append("Дизельные авто преобладают, рассмотрите их как приоритет.")

        gearbox_counts = filtered['gearbox'].value_counts()
        if gearbox_counts.get('automatic', 0) > gearbox_counts.get('manual', 0):
            recs.append("Авто с автоматической коробкой передач преобладают, рассмотрите их как приоритет.")

        if (filtered['mileage'] < 40000).sum() > len(filtered) * 0.3:
            recs.append("Много авто с пробегом до 40 000 миль, они могут быть более ликвидны.")

        if 'doors' in filtered.columns and not filtered['doors'].isna().all():
            most_common_doors = int(filtered['doors'].mode().iloc[0])
            if most_common_doors >= 5:
                recs.append("Пятидверные авто доминируют, предпочтительны для семейных клиентов.")

        if not recs:
            recs.append("Нет особых рекомендаций по выбранным фильтрам.")

    except Exception as e:
        messagebox.showerror("Ошибка анализа", f"Ошибка при вычислении рекомендаций: {e}")
        return

    # Показываем рекомендации
    top = tk.Toplevel(root)
    top.title("Рекомендации по фильтру")
    tk.Label(top, text="\n".join(recs), wraplength=400, justify="left").pack(padx=10, pady=10)