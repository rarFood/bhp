import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host,local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" (local_host,local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connections information

        print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket,remote_host,remote_port,receive_first))

        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:

        remote_buffer= receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_socket)

        # if we have data to send to our local client, send it
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    # now lets loop and read from local,
    # send remote, send to local
    # rinse and repeat
    while True:

        # read from local host
        local_buffer = receive_from(client_socket)


        if len(local_buffer):

            print "[==>] Received %d bytes from localhost." % len(local_buffe )
            hexdump(local_buffer)

            # send it to our reuqest handler
            local_buffer = request_handler (local_buffer)

            # send off the data to the remote host
            print "[==>] Send to remote."

            # receive back the reponse
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print "[<==] Received %d bytes from remote."  % len(remote_buffer)
                hexdump(remote_buffer)

                # send to our response handler
                remote_buffer = response_handler(remote_buffer)

                # send the response to the local socket
                client_socket.send(remote_buffer)

                print "[<==] Sent to localhost."

            # if no more data on either side, close the connections
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] NO more data. Closing connections."

                break


def main() :

    # no fancy command-line paring here
    if len(sys.argv[1:]) != 5 :
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remotehost] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data
    # before sending to remote host
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else :
        receive_first = False

    # no spin up our listening socket
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

main()
