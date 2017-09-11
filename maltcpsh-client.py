import sys, getopt
import socket

def showHelp():
    print("This will display the command options")
    print("-h, --help . . . . print this message")
    print("-t, --target <IP>  . . . .  target IP")
    print("-p, --port <port>  . . . . . . . port")
    print("-d, --data <command>   commmand input")

def spinTCP(h, p, d):
    target_host = h
    target_port = p
    data = d
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect the client
    client.connect((target_host,target_port))
    # send some data
    client.send(data)
    # receive some data
    response = client.recv(4096)
    print response

def main(argv):

    tmp_host = ""
    tmp_port = 0
    tmp_data = ""
    try:
        opts, args = getopt.getopt(argv,"ht:p:d:",["help","target=","port=","data="])
    except getopt.GetoptError:
        showHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            showHelp()
            sys.exit()
        elif opt in ("-t", "--target"):
            tmp_host = arg
        elif opt in ("-p", "--port"):
            tmp_port = int(arg)
        elif opt in ("-d", "--data"):
            tmp_data = arg
        else:
            showHelp()
            sys.exit()

    spinTCP(tmp_host, tmp_port, tmp_data)

if __name__ == "__main__":
   main(sys.argv[1:])
