import socket


#get broadcast ip address
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
broadcastip = s.getsockname()[0]
broadcastip = broadcastip[0:broadcastip.rindex(".")] + ".255"
s.close()

print(broadcastip)