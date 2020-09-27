import socketserver, socket, queue, struct
import time

BASE_PORT = 50000

HEADER_FORMAT = 'BBBB'
COMMAND = 1
REPORT = 0
HEARTBEAT_ID = 0


class UDPHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = self.request[0].strip()
		self.m_received = data

	def GetData(self):
		#print(str(hasattr(self, 'm_receiveQueue'))) #+ " " + str(self.m_receiveQueue.qsize())
		if(hasattr(self, 'm_received')):
			data = self.m_received
			return data
		else:
			return None


class HomeIOLink():

	def __init__(self, myId, partnerId, partnerIp, isBroadcast):
		self.m_myId = myId
		self.m_partnerId = partnerId
		self.m_partnerIp = partnerIp
		self.m_server = socketserver.UDPServer((self.GetLocalIp(), BASE_PORT + myId), UDPHandler)
#		self.m_server.RequestHandlerClass.__init__(self.m_server.RequestHandlerClass)
		self.m_server.timeout = .1
		self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		if isBroadcast:
			self.m_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.m_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	def Write(self, msg):
		print(str(msg) + " " + str(self.m_partnerId) + " " + str(self.m_partnerIp))
		self.m_socket.sendto(msg, (self.m_partnerIp, self.m_partnerId + BASE_PORT))

	def GetLocalIp(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		localIp = s.getsockname()[0]
		s.close()
		return localIp

class HomeIOThermostat(HomeIOLink):

	THERMOSTAT_STATUS_FORMAT = 'BH'
	THERMOSTAT_SCHEDULE_HEADER_FORMAT = 'BB'
	THERMOSTAT_SCHEDULE_FORMAT = 'BBB'
	THERMOSTAT_STATE_ID = 10

	p_setting = 0
	p_temperature = 0
	p_receivedCommandTime = 0
	p_lastReceivedTime = 0


	def __init__(self, myId, partnerId, partnerIp):
		super(Thermostat, self).__init__(self, myId, partnerId, partnerIp)
		self.m_schedules = {}
		self.m_currentCommand = 0
		self.m_currentTemp = 0
		self.m_currentHumidity = 0
		self.m_lastReceiveTime = 0

	def handle_read(self):
		recvBuffer = self.recv(8192)

		sourceId, destinationId, msgType, messageId = unpack(HEADER_FORMAT, recvBuffer[0:4])
		if destinationId != self.m_myId: return
		
		if messageId == THERMOSTAT_STATUS_ID:
			self.p_setting, self.p_temperature = unpack(THERMOSTAT_STATUS_FORMAT, recvBuffer[4:6])
			self.p_temperature = self.p_temperature / 10
			if msgType == COMMAND:
				self.p_receivedCommandTime = time.time()
			

		self.p_lastReceiveTime = time.time()

	def SendStatus(self, setting, temperature):
		header = pack(HEADER_FORMAT, self.m_myId, self.m_partnerId, REPORT, THERMOSTAT_STATE_ID)
		msg = pack(THERMOSTAT_STATUS_FORMAT, setting, temperature * 10)
		self.m_sendQueue.put(header + msg)

	def SendSettingsCommand(self, setting):
		header = pack(HEADER_FORMAT, self.m_myId, self.m_partnerId, COMMAND, THERMOSTAT_STATE_ID)
		msg = pack(THERMOSTAT_STATUS_FORMAT, setting, 0)
		self.m_sendQueue.put(header + msg)

class HomeIOBroadcast(HomeIOLink):

	p_devicesConnected = {}

	def __init__(self, myId):
		broadcastIp = self.GetBroadcastIP()
		super().__init__(0, 0, broadcastIp, True)
		self.m_broadcastIp = broadcastIp
		self.localID = myId

	def ProcessReadQueue(self):
		self.m_server.handle_request()
		data = self.m_server.RequestHandlerClass.GetData()
		while(data != None):			

			print("Gets To Here")
			if len(data) != 4:
				return 

			sourceId, destinationId, msgType, msgId = unpack(HEADER_FORMAT, recvBuffer)

			if sourceId not in p_devicesConnected.keys():
				p_devicesConnected[sourceId] = addr

			data = self.m_server.RequestHandlerClass.GetData(self.m_server.RequestHandlerClass)

	def SendBroadcast(self):
		header = struct.pack(HEADER_FORMAT, self.localID, 0, REPORT, HEARTBEAT_ID)
		self.Write(header)

	def GetBroadcastIP(self):
		localIp = self.GetLocalIp()
		broadcastip = localIp[0:localIp.rindex(".")] + ".255"
		return broadcastip

