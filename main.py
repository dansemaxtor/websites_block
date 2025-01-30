import sqlite3
import getpass
import os
import hashlib
import schedule
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox

# Путь переадресации
redirect = "127.0.0.1"
db_path = os.path.join(os.getcwd(), 'app_data.db')  # Одна база данных
websites_file = 'websites_list.txt'  # Путь к файлу с сайтами

# Функция хэширования паролей
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Создание таблиц базы данных
def create_tables():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Получение хэшированного пароля из базы данных
def get_password_from_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM passwords WHERE id = 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Сохранение хэшированного пароля в базу данных
def save_password_to_db(password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (id, password) VALUES (1, ?)', (password,))
    conn.commit()
    conn.close()

# Добавление сайтов в базу данных
def add_websites_to_db(websites):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for site in websites:
        cursor.execute('SELECT COUNT(*) FROM websites WHERE url = ?', (site,))
        if cursor.fetchone()[0] == 0:  # Если сайт не найден в базе
            cursor.execute('INSERT INTO websites (url) VALUES (?)', (site,))
            print(f"Сайт {site} добавлен в базу данных.")
        else:
            print(f"Сайт {site} уже существует в базе данных.")
    conn.commit()
    conn.close()

# Запись сайтов из базы данных в файл
def write_sites_to_file():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM websites')
    all_sites = cursor.fetchall()
    conn.close()

    with open(websites_file, 'w') as f:
        for site in all_sites:
            f.write(f"{redirect} {site[0]}\n")
    messagebox.showinfo("Успех", "Сайты Заблокированы")
    print(f'Сайты записаны в "{websites_file}".')

# Очистка файла websites_list.txt
def clear_websites_file():
    if os.path.exists(websites_file):
        open(websites_file, 'w').close()  # Очищаем файл
        print(f'Файл {websites_file} очищен.')

# Очистка базы данных и файла
def clear_websites():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM websites')
    conn.commit()
    conn.close()
    clear_websites_file()
    messagebox.showinfo("Успех", "Сайты разблокированы")

# Ввод сайтов пользователем
def create_list(sites_input):
    websites = sites_input.split("\n")
    websites = [site.strip() for site in websites if site.strip()]
    if websites:
        add_websites_to_db(websites)
        write_sites_to_file()
    else:
        print("Не введены адреса сайтов.")

# Получение всех сайтов из базы данных
def get_all_websites():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM websites')
    websites = cursor.fetchall()
    conn.close()
    return [site[0] for site in websites]

# Проверка пароля
def password_check():
    create_tables()  # Убедимся, что таблицы существуют
    stored_password = get_password_from_db()

    if stored_password:
        # Если пароль уже существует, проверяем его
        return stored_password, True
    else:
        # Если пароль отсутствует, создаем новый
        return None, False

# Запуск и завершение программы по расписанию
def start_program(sites_input):
    print("Программа запущена!")
    create_list(sites_input)

def stop_program():
    print("Программа завершена!")
    clear_websites_file()  # Очищаем файл с сайтами
    exit(0)

def schedule_tasks(start_time, stop_time, sites_input):
    schedule.every().day.at(start_time).do(start_program, sites_input)
    schedule.every().day.at(stop_time).do(stop_program)

    print(f"Программа будет запущена в {start_time} и завершена в {stop_time}.")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Функция для запуска планировщика в отдельном потоке
def start_scheduler_thread(start_time, stop_time, sites_input):
    scheduler_thread = threading.Thread(target=schedule_tasks, args=(start_time, stop_time, sites_input))
    scheduler_thread.daemon = True
    scheduler_thread.start()

# Графический интерфейс с Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа с расписанием")

        self.password_window()

    def password_window(self):
        self.password_frame = tk.Frame(self.root)
        self.password_frame.pack(padx=30, pady=30)

        self.password_label = tk.Label(self.password_frame, text="Введите пароль:")
        self.password_label.grid(row=0, column=0)

        self.password_entry = tk.Entry(self.password_frame, show="*")
        self.password_entry.grid(row=0, column=1)

        self.password_button = tk.Button(self.password_frame, text="Войти", command=self.check_password)
        self.password_button.grid(row=0, column=2)

    def check_password(self):
        stored_password, is_existing = password_check()

        entered_password = self.password_entry.get()

        if is_existing:
            if hash_password(entered_password) == stored_password:
                self.password_frame.pack_forget()  # Убираем окно пароля
                self.main_window()  # Открываем основное окно
            else:
                messagebox.showerror("Ошибка", "Неверный пароль.")
        else:
            if entered_password.strip():
                save_password_to_db(hash_password(entered_password))
                messagebox.showinfo("Успех", "Пароль сохранен. Перезапустите приложение.")
                self.root.quit()

    def main_window(self):
        # Фрейм для ввода сайтов
        self.sites_frame = tk.Frame(self.root)
        self.sites_frame.pack(padx=20, pady=20)

        self.sites_label = tk.Label(self.sites_frame, text="Введите сайты (через новую строку):")
        self.sites_label.grid(row=0, column=0)

        self.sites_text = tk.Text(self.sites_frame, height=5, width=40)
        self.sites_text.grid(row=1, column=0)

        # Загружаем сайты из базы данных и показываем в поле
        all_sites = get_all_websites()
        for site in all_sites:
            self.sites_text.insert(tk.END, site + "\n")

        # Фрейм для ввода времени запуска и завершения
        self.time_frame = tk.Frame(self.root)
        self.time_frame.pack(padx=10, pady=10)

        self.start_time_label = tk.Label(self.time_frame, text="Время запуска (HH:MM):")
        self.start_time_label.grid(row=0, column=0)

        self.start_time_entry = tk.Entry(self.time_frame)
        self.start_time_entry.grid(row=0, column=1)

        self.stop_time_label = tk.Label(self.time_frame, text="Время завершения (HH:MM):")
        self.stop_time_label.grid(row=1, column=0)

        self.stop_time_entry = tk.Entry(self.time_frame)
        self.stop_time_entry.grid(row=1, column=1)

        # Кнопки для запуска программы
        self.mode_button_frame = tk.Frame(self.root)
        self.mode_button_frame.pack(padx=10, pady=10)

        self.schedule_button = tk.Button(self.mode_button_frame, text="Запуск по расписанию", command=self.set_schedule)
        self.schedule_button.grid(row=0, column=0)

        self.immediate_button = tk.Button(self.mode_button_frame, text="Немедленный запуск", command=self.start_immediately)
        self.immediate_button.grid(row=0, column=1)

        # Кнопка для очистки списка сайтов
        self.clear_button = tk.Button(self.mode_button_frame, text="Очистить список", command=self.clear_websites)
        self.clear_button.grid(row=0, column=2)

    def set_schedule(self):
        start_time = self.start_time_entry.get()
        stop_time = self.stop_time_entry.get()

        if start_time and stop_time:
            sites_input = self.sites_text.get("1.0", "end-1c")  # Получаем список сайтов из текстового поля
            if sites_input.strip():
                start_scheduler_thread(start_time, stop_time, sites_input)
                messagebox.showinfo("Расписание", f"Запуск в {start_time}, завершение в {stop_time}.")
            else:
                messagebox.showerror("Ошибка", "Не введены сайты.")
        else:
            messagebox.showerror("Ошибка", "Не указано время.")

    def start_immediately(self):
        sites_input = self.sites_text.get("1.0", "end-1c")
        if sites_input.strip():
            start_program(sites_input)
        else:
            messagebox.showerror("Ошибка", "Не введены сайты.")

    def clear_websites(self):
        clear_websites()
        self.sites_text.delete("1.0", tk.END)  # Очищаем текстовое поле с сайтами

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()