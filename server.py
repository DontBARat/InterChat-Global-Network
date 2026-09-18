import socket
import threading

HOST = '0.0.0.0'
PORT = 12345
SECRET_KEY = 42

def encrypt_decrypt(text):
    return "".join(chr(ord(c) ^ SECRET_KEY) for c in text)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

# База комнат (Без Китая!)
rooms = {
    "UN_HQ": [], "Russia": [], "USA": [], 
    "UK": [], "Canada": [], "Israel": [], "Germany": []
}
client_rooms = {}

def handle_client(client, address):
    current_room = "UN_HQ"
    rooms[current_room].append(client)
    client_rooms[client] = current_room
    print(f"[СЕРВЕР] Агент {address} вошел в штаб ООН.")

    while True:
        try:
            data = client.recv(4096)
            if not data: break
            
            try: decrypted_text = encrypt_decrypt(data.decode('utf-8'))
            except: decrypted_text = ""
            
            if decrypted_text.startswith("JOIN|"):
                new_room = decrypted_text.split("|")[1]
                if new_room in rooms:
                    if client in rooms[current_room]: rooms[current_room].remove(client)
                    current_room = new_room
                    rooms[current_room].append(client)
                    client_rooms[client] = current_room
                    client.send(f"SYSTEM:Безопасный канал активирован.".encode('utf-8'))
                    print(f"[СЕРВЕР] Агент {address} перешел в комнату: {current_room}")
            else:
                for c in rooms[current_room]:
                    if c != client:
                        try: c.send(data)
                        except: pass
        except:
            break
            
    if client in rooms[current_room]: rooms[current_room].remove(client)
    client.close()

print("--- ЦЕНТРАЛЬНЫЙ СЕРВЕР INTERCHAT v5.5 ОНЛАЙН ---")
while True:
    client, address = server.accept()
    threading.Thread(target=handle_client, args=(client, address), daemon=True).start()
