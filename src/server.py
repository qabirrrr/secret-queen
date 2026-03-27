import socket

def main():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("Server is running!")

        conn, addr = s.accept()
        print("User 1 has connected")

        conn2, addr2 = s.accept()
        print("User 2 has connected")

        turn = 1 # it'll start at 0

        with conn and conn2:
            print("\nBoth users have joined\n")
            while True:
                turn = (turn + 1) % 2

                if turn == 0:
                    data = conn.recv(1024)
                    a,b,c = data.decode().split(",")
                    print(a,b,c)
                    if not data: break
                    conn.sendall(data)
                
                else:
                    data = conn2.recv(1024)
                    a,b,c = data.decode().split(",")
                    print(a,b,c)
                    if not data: break
                    conn2.sendall(data)

if __name__ == "__main__":
    main()