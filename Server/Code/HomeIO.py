import asyncore,socket, queue, struct
from datetime import date

BASE_PORT = 50000

HEADER_FORMAT = 'BBBB'

class HomeIOLink(asyncore.dispatcher):

	def __init__(self, myId, myIp, partnerId, partnerIp):
		asyncore.dispatcher.__init__(self)
		self.m_myId = myId
		self.m_parnerId = partnerId
		self.m_partnerIp = partnerIp
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.bind(myIp, BASE_PORT + myId)
		self.connect(partnerIp, BASE_PORT + partnerId)
		self.m_sendQueue = queue.Queue()
		self.m_lastReceiveTime = None

	def handle_close(self):
		self.close()

	def writable(self):
		return m_sendQueue.qsize() > 0

	def handle_write(self):
		pack = m_sendQueue.get()
		self.send(pack)

class Thermostat(HomeIOLink):

	THERMOSTAT_STATUS_FORMAT = 'BHH'
	THERMOSTAT_SCHEDULE_HEADER_FORMAT = 'BB'
	THERMOSTAT_SCHEDULE_FORMAT = ''

	def __init__(self, myId, myIp, partnerId, partnerIp):
		super.__init__(self, myId, myIp, partnerId, partnerIp)
		self.m_schedules = {}
		self.m_currentCommand = 0
		self.m_currentTemp = 0
		self.m_currentHumidity = 0

	def handle_read(self):
		recvBuffer = self.recv(8192)

		self.m_lastReceiveTime = datetime.now()


