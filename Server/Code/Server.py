import HomeIO
import time
import asyncore
import threading

def RunAsyncore():
	asyncore.loop();

SERVER_ID = 0

broadcaster = HomeIO.HomeIOBroadcast(SERVER_ID)

timer = 0

threading.Thread(target = RunAsyncore)

while True:
	currTime = time.time()
	if currTime - timer > 1:
		timer = currTime
		print("Sending Broadcast")
		broadcaster.SendBroadcast()
