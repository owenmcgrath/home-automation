import HomeIO
import time
import threading

SERVER_ID = 10

timer = 0

broadcaster = HomeIO.HomeIOBroadcast(SERVER_ID)

while True:
	broadcaster.ProcessReadQueue()
	currTime = time.time()
	if currTime - timer > 1:
		timer = currTime
		print("Sending Broadcast")
		broadcaster.SendBroadcast()
		for x in broadcaster.p_devicesConnected:
			print(x)




