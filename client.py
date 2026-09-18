import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# --- ОКНО АВТОРИЗАЦИИ В СТИЛЕ СТАРЫХ ПРОГРАММ ---
root_init = tk.Tk()
root_init.withdraw()
nickname = simpledialog.askstring("Авторизация", "Введите ваш Никнейм (Сетевое имя):", parent=root_init)

if not nickname:
    nickname = "Xakep_2000"

# Попытка установить сетевое соединение с большим сервером
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    connection_success = True
except:
    connection_success = False

# --- ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ (РЕТРО-ИНТЕРФЕЙС) ---
root = tk.Tk()
root.title(f"Ретро-Служба v2.0b - [{nickname}]")
root.geometry("460x560")
root.configure(bg="#d4d0c8")  # Классический серо-бежевый системный цвет

# Шрифты из эпохи старых мониторов
old_school_font = ("Tahoma", 10)
log_font = ("Courier New", 10)

# Применение классической темы для вкладок (как в Windows 2000)
style = ttk.Style()
style.theme_use('classic')
style.configure('TNotebook', background='#d4d0c8', bd=2)
style.configure('TNotebook.Tab', background='#d4d0c8', foreground='black', padding=6, font=("Tahoma", 9))
style.map('TNotebook.Tab', background=[('selected', '#e4e0d8')], expand=[('selected',)])

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=5, pady=5)

# ====================================================================
# ВКЛАДКА 1: ICQ МЕССЕНДЖЕР
# ====================================================================
tab_chat = tk.Frame(notebook, bg="#d4d0c8")
notebook.add(tab_chat, text=" 📟 ICQ Мессенджер ")

chat_log = tk.Text(tab_chat, bg="white", fg="black", font=log_font, height=21, width=52)
chat_log.pack(padx=10, pady=10)

if connection_success:
    chat_log.insert(tk.END, "--- Успешно подключено к серверу 2000-х! ---\n")
    chat_log.insert(tk.END, "--- АНТИ-БРОНИ ФИЛЬТР: АКТИВИРОВАН ---\n\n")
else:
    chat_log.insert(tk.END, "--- Ошибка: Большой server оффлайн. ---\n")
    chat_log.insert(tk.END, "--- Чат запущен в локальном демо-режиме. ---\n\n")

entry_field = tk.Entry(tab_chat, bg="white", fg="black", font=old_school_font, width=38)
entry_field.pack(side=tk.LEFT, padx=10, pady=10)

def send_message():
    text = entry_field.get().strip()
    if text:
        # --- ЧЕРНЫЙ СПИСОК СЛОВ (АНТИ-БРОНИ) ---
        forbidden_words = ["пони", "брони", "pony", "brony", "май литл", "my little pony", "вайфу"]
        
        text_lower = text.lower()
        if any(word in text_lower for word in forbidden_words):
            messagebox.showerror(
                "СИСТЕМНАЯ БЛОКИРОВКА", 
                "ОШИБКА 403: Контент брони строго запрещен администрацией чата!\nСообщение удалено."
            )
            entry_field.delete(0, tk.END)
            return

        if connection_success:
            try:
                full_chat_msg = f"CHAT:[{nickname}]: {text}"
                client_socket.send(full_chat_msg.encode('utf-8'))
                entry_field.delete(0, tk.END)
            except:
                chat_log.insert(tk.END, "--- Ошибка отправки: связь потеряна ---\n")
        else:
            chat_log.insert(tk.END, f"[{nickname} (оффлайн)]: {text}\n")
            entry_field.delete(0, tk.END)

send_button = tk.Button(tab_chat, text="Отправить", command=send_message, bg="#d4d0c8", fg="black", font=old_school_font, relief=tk.RAISED, bd=2)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# ====================================================================
# ВКЛАДКА 2: ПОЧТОВЫЙ СЕРВИС
# ====================================================================
tab_mail = tk.Frame(notebook, bg="#d4d0c8")
notebook.add(tab_mail, text=" 📬 Почта Экспресс ")

tk.Label(tab_mail, text="Кому (Локальный ник или Email адрес):", bg="#d4d0c8", font=old_school_font).pack(anchor='w', padx=15, pady=(15, 2))
mail_to = tk.Entry(tab_mail, bg="white", fg="black", font=old_school_font, width=50)
mail_to.pack(padx=15, pady=2)

tk.Label(tab_mail, text="Тема письма (для генерации имени файла):", bg="#d4d0c8", font=old_school_font).pack(anchor='w', padx=15, pady=(10, 2))
mail_subject = tk.Entry(tab_mail, bg="white", fg="black", font=old_school_font, width=50)
mail_subject.pack(padx=15, pady=2)

tk.Label(tab_mail, text="Текст электронного письма:", bg="#d4d0c8", font=old_school_font).pack(anchor='w', padx=15, pady=(10, 2))
mail_body = tk.Text(tab_mail, bg="white", fg="black", font=log_font, height=11, width=50)
mail_body.pack(padx=15, pady=2)

def send_email():
    to_user = mail_to.get().strip()
    subject = mail_subject.get().strip()
    body = mail_body.get("1.0", tk.END).strip()
    
    if not to_user or not subject or not body:
        messagebox.showwarning("Внимание", "Заполните абсолютно все поля письма!")
        return
        
    if connection_success:
        mail_packet = f"MAIL|FROM:{nickname}|TO:{to_user}|SUBJ:{subject}|BODY:{body}"
        try:
            client_socket.send(mail_packet.encode('utf-8'))
            messagebox.showinfo("Успех", "Письмо передано на большой сервер!\nТам будет сгенерирован текстовый файл.")
            mail_to.delete(0, tk.END)
            mail_subject.delete(0, tk.END)
            mail_body.delete("1.0", tk.END)
        except:
            messagebox.showerror("Ошибка", "Связь разорвана. Не удалось передать почту.")
    else:
        messagebox.showerror("Ошибка", "Большой сервер находится в оффлайне!")

send_mail_btn = tk.Button(tab_mail, text=" 📪 Отправить почту ", command=send_email, bg="#d4d0c8", fg="black", font=old_school_font, relief=tk.RAISED, bd=2)
send_mail_btn.pack(anchor='e', padx=15, pady=15)

# ====================================================================
# ПОТОК ДЛЯ ПРИЕМА СООБЩЕНИЙ ЧАТА ПО СЕТИ
# ====================================================================
def receive_messages():
    while connection_success:
        try:
            message = client_socket.recv(4096).decode('utf-8')
            if message:
                if message.startswith("CHAT:"):
                    clean_msg = message.replace("CHAT:", "", 1)
                    chat_log.insert(tk.END, clean_msg + "\n")
                else:
                    chat_log.insert(tk.END, message + "\n")
                chat_log.see(tk.END)
        except:
            break

if connection_success:
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

root.mainloop()
