import xmpp
import redis
import json
import ast
import copy

user = 'k'
password = 'k'
station_no = '1'
resp ={}
msg = {}
def message_handler(conn, mesg):

	print "received"
	data = str(mesg.getBody())
	rep = str(mesg.getFrom()).split('@')[0]
	t = ast.literal_eval(data)['timestamps']
	for s in t:
		if not(s in resp[user]):
			resp[user][s] = copy.copy(msg[s]) 
	
	resp[rep] = ast.literal_eval(data)['timestamps']
	f = open('data.json','w')
	f.write(json.dumps(resp))
	f.close()
	print resp

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

	for to in recipients:
		message = xmpp.Message(to,msg)
		message.setAttr('type', 'chat')
		connection.send(message)
		print "sent message to "+to


connection = xmpp.Client('localhost',debug=[])
connection.connect(server=('localhost',5222))
connection.auth(user,password,'Online')
connection.sendInitPresence()
connection.RegisterHandler('message',message_handler)
roster = connection.getRoster()
recipients = roster.getItems()
recipients.remove(user+'@localhost')
#print recipients
#print msg
#l = recipients.leen
msgString = get_local_data()
send_msg(msgString,recipients)
while connection.Process(1):
	pass
