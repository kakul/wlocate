import xmpp
import redis
from threading import Timer
user = 'k'
password = 'k'
station_no = '1'
def get_local_data():
	
	try:
		r = redis.Redis('localhost', port = 6379, db = 0)
	except Exception, (e):
		print str(e)
	macs = r.hkeys('station_'+station_no)
	for i in macs:
		msg[i] = r.lrange(i+"_"+station_no,0,-1)
	resp[user] = {}
	return json.dumps(msg)
	
def send_msg(msg,recipients):
	msgString = get_local_data()
	for to in recipients:
		message = xmpp.Message(to,msg)
		message.setAttr('type', 'chat')
		connection.send(message)
		print "sent message to "+to


connection = xmpp.Client('localhost',debug=[])
connection.connect(server=('localhost',5222))
connection.auth(user,password,'Online')
connection.sendInitPresence()
roster = connection.getRoster()
recipients = roster.getItems()
recipients.remove(user+'@localhost')
t = Timer(3.0,send_msg(recipients))
t.start()