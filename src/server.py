import socket

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        conn, addr = s.accept()

        conn2, addr2 = s.accept()

        turn = 1 # it'll start at 0

        with conn and conn2:
            conn.sendall(b"white")
            conn2.sendall(b"black")
            while True:
                turn = (turn + 1) % 2

                if turn == 0:
                    data = conn.recv(4096)
                    if not data: break
                    conn2.sendall(data)
                
                else:
                    data = conn2.recv(4096)
                    if not data: break
                    conn.sendall(data)

if __name__ == "__main__":
    main()