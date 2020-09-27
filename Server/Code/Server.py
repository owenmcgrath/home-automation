import HomeIO
import time
import threading

SERVER_ID = 0

timer = 0

broadcaster = HomeIO.HomeIOBroadcast(SERVER_ID)

while True:
	broadcaster.ProcessReadQueue()
	currTime = time.time()
	if currTime - timer > 1:
		timer = currTime
		print("Sending Broadcast")
		broadcaster.SendBroadcast()




