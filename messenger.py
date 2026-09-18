import tkinter as tk
from tkinter import messagebox, ttk
import socket
import threading
import os

# КРИПТОГРАФИЯ XOR (Ключ шифрования)
SECRET_KEY = 42

def encrypt_decrypt(text):
    return "".join(chr(ord(c) ^ SECRET_KEY) for c in text)

# --- ЧТЕНИЕ НАСТРОЕК ИЗ CONFIG.TXT ---
HOST = '127.0.0.1'
PORT = 12345

if os.path.exists("config.txt"):
    try:
        with open("config.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                HOST = lines[0].strip()
                PORT = int(lines[1].strip())
    except:
        print("Config error. Using localhost.")

# Попытка установить зашифрованный туннель
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    connection_success = True
except:
    connection_success = False

# --- ГЛАВНОЕ ОКНО INTERCHAT ---
root = tk.Tk()
root.title("🔐 InterChat Global Network v5.5")
root.geometry("650x540")
root.configure(bg="#d4d0c8")

# Убираем синее перо
if os.path.exists("icon.ico"):
    try: root.iconbitmap("icon.ico")
    except: pass
else:
    try: root.iconbitmap(default='')
    except: pass

old_school_font = ("Tahoma", 10)
log_font = ("Courier New", 10)

# Словарь для мгновенного перевода ВСЕГО интерфейса и стран
translations = {
    "ru": {
        "rooms_title": "Комнаты / Страны",
        "btn_send": "Отправить",
        "welcome": f"--- Подключено к узлу {HOST}:{PORT} ---\n",
        "secure": "--- АППАРАТНОЕ ШИФРОВАНИЕ XOR: АКТИВНО ---\n\n",
        "offline": "--- ОШИБКА: СЕРВЕР МАСКИРОВКИ ОФФЛАЙН ---\n\n",
        "ban": "Запрещено политикой безопасности чата!",
        "switch": "ТУННЕЛЬ ПЕРЕКЛЮЧЕН НА ",
        "countries": [
            "Глобальный чат (ООН)", "Россия", "США", 
            "Великобритания", "Канада", "Израиль", "Германия"
        ]
    },
    "en": {
        "rooms_title": "Channels / Countries",
        "btn_send": "Send",
        "welcome": f"--- Connected to military node {HOST}:{PORT} ---\n",
        "secure": "--- HARDWARE XOR ENCRYPTION: ACTIVE ---\n\n",
        "offline": "--- ERROR: SECURE SERVER OFFLINE ---\n\n",
        "ban": "Forbidden by chat security policy!",
        "switch": "TUNNEL SWITCHED TO ",
        "countries": [
            "Global Chat (UN)", "Russia", "USA", 
            "United Kingdom", "Canada", "Israel", "Germany"
        ]
    }
}

current_lang = "ru"  # По умолчанию русский

# --- ВЕРХНЯЯ ПАНЕЛЬ НАСТРОЕК ЯЗЫКА ---
lang_frame = tk.Frame(root, bg="#d4d0c8")
lang_frame.pack(fill="x", padx=10, pady=(5, 0))

# Боковая панель геополитических комнат
rooms_frame = tk.LabelFrame(root, text=translations[current_lang]["rooms_title"], bg="#d4d0c8", font=old_school_font, bd=2, relief=tk.GROOVE)
rooms_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10)

rooms_listbox = tk.Listbox(rooms_frame, bg="white", fg="black", font=old_school_font, width=24)
rooms_listbox.pack(padx=5, pady=5, fill="both", expand=True)

# Функция для обновления списка стран на нужном языке
def update_rooms_list():
    rooms_listbox.delete(0, tk.END)
    for country in translations[current_lang]["countries"]:
        rooms_listbox.insert(tk.END, country)
    rooms_listbox.select_set(0)

update_rooms_list()

# Основная зона секретного чата
chat_frame = tk.Frame(root, bg="#d4d0c8")
chat_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=10)

chat_log = tk.Text(chat_frame, bg="white", fg="black", font=log_font, height=21, width=45)
chat_log.pack(padx=5, pady=5, fill="both", expand=True)

entry_field = tk.Entry(chat_frame, bg="white", fg="black", font=old_school_font)
entry_field.pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=True)

# Функция динамической смены языка прямо в работающей программе
def change_language(lang):
    global current_lang
    current_lang = lang
    rooms_frame.config(text=translations[current_lang]["rooms_title"])
    send_button.config(text=translations[current_lang]["btn_send"])
    
    # Обновляем страны на новом языке!
    update_rooms_list()
    
    if lang == "ru":
        btn_ru.config(relief=tk.SUNKEN, bg="#e4e0d8")
        btn_en.config(relief=tk.RAISED, bg="#d4d0c8")
    else:
        btn_en.config(relief=tk.SUNKEN, bg="#e4e0d8")
        btn_ru.config(relief=tk.RAISED, bg="#d4d0c8")

btn_ru = tk.Button(lang_frame, text="Русский", font=("Tahoma", 8), command=lambda: change_language("ru"), relief=tk.SUNKEN, bg="#e4e0d8")
btn_ru.pack(side=tk.RIGHT, padx=2)
btn_en = tk.Button(lang_frame, text="English", font=("Tahoma", 8), command=lambda: change_language("en"), relief=tk.RAISED, bg="#d4d0c8")
btn_en.pack(side=tk.RIGHT, padx=2)

# Вывод стартовых логов
if connection_success:
    chat_log.insert(tk.END, translations[current_lang]["welcome"])
    chat_log.insert(tk.END, translations[current_lang]["secure"])
else:
    chat_log.insert(tk.END, translations[current_lang]["offline"])

def switch_room(event):
    try:
        selected_index = rooms_listbox.curselection()[0]
        # Сервер всегда использует английские имена комнат в фоне, чтобы не путаться
        server_rooms = ["UN_HQ", "Russia", "USA", "UK", "Canada", "Israel", "Germany"]
        selected_room = server_rooms[selected_index]
        
        if connection_success:
            cmd = f"JOIN|{selected_room}"
            client_socket.send(encrypt_decrypt(cmd).encode('utf-8'))
            
            display_name = translations[current_lang]["countries"][selected_index]
            chat_log.insert(tk.END, f"\n--- {translations[current_lang]['switch']}{display_name} ---\n")
    except:
        pass

rooms_listbox.bind('<<ListboxSelect>>', switch_room)

def send_message():
    text = entry_field.get().strip()
    if text:
        if any(w in text.lower() for w in ["пони", "брони", "pony", "brony"]):
            messagebox.showerror("SECURITY", translations[current_lang]["ban"])
            entry_field.delete(0, tk.END)
            return

        if connection_success:
            try:
                full_msg = f"[User]: {text}"
                encrypted_msg = encrypt_decrypt(full_msg)
                client_socket.send(encrypted_msg.encode('utf-8'))
                entry_field.delete(0, tk.END)
            except:
                chat_log.insert(tk.END, "--- Connection lost ---\n")

send_button = tk.Button(chat_frame, text=translations[current_lang]["btn_send"], command=send_message, bg="#d4d0c8", fg="black", font=old_school_font, relief=tk.RAISED, bd=2)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)

def receive_messages():
    while connection_success:
        try:
            raw_data = client_socket.recv(4096).decode('utf-8')
            if raw_data:
                if raw_data.startswith("SYSTEM:"):
                    decrypted_msg = raw_data.replace("SYSTEM:", "", 1)
                else:
                    decrypted_msg = encrypt_decrypt(raw_data)
                
                chat_log.insert(tk.END, decrypted_msg + "\n")
                chat_log.see(tk.END)
        except:
            break

if connection_success:
    threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
