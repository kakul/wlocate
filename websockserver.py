import json
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleEcho(WebSocket):

	def handleMessage(self):
		with open('data.json') as f:
			r = json.loads(f)
			
			print r
		print type(self.data)
		#	s = json.dumps(data)
		self.sendMessage(self.data)
		


	def handleConnected(self):
		print self.address, 'connected'

	def handleClose(self):
		print self.address, 'closed'

server = SimpleWebSocketServer('', 8004, SimpleEcho)
server.serveforever()