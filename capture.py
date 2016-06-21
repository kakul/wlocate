from scapy.all import *
import datetime
import redis
import atexit
st_no = '1'
#i = "wlx00c0ca81b9a2"
#i = "wlx00c0ca761abd"
i = "wlp6s0"
probes = {}
r1 = None
r2 = None

def save_all():
	if not(r2 == None):
		r2.save()
		print "data saved successfully"

def connect_server():
	try:
		r1 = redis.Redis('192.168.111.187', port = 6379, db = 0)
		print "Connected to server database"
	except Exception, (e):
		print str(e)
	return r1
def connect_local():
	try:
		r2 = redis.Redis('localhost', port = 6379, db = 0)
		print "Connected to local database"
	except Exception, (e):
		print str(e)
	return r2

def read_data():
	probes = r2.hgetall('station_'+st_no)
	print "read data into dictionary"
	return probes

def handler(p):
	#print
	if p.haslayer(Dot11ProbeReq):
		bssid = p.addr2
		##if bssid == "e0:2c:b2:ce:c5:da":
		print bssid
		if len(bssid) == 0:
			return
		timestamp  = datetime.datetime.now()

		ts = r2.hget('station_'+st_no,bssid)

		if ts is None:
			try:
				#r1.hmset('station_'+st_no,{bssid:timestamp})
				r2.hmset('station_'+st_no,{bssid:timestamp})
				#r1.rpush('station'+st_no+'_'+bssid,timestamp)
				r2.rpush(bssid+"_"+st_no,timestamp)
				
				print bssid,"inserted"
			except Exception, e:
				print str(e)
		else:
			if type(ts) == str:
				#timeString, microsec = probes[bssid].split('.')
				dt = datetime.datetime.strptime(ts,"%Y-%m-%d %H:%M:%S.%f")
				ts = dt
			
			if ts + datetime.timedelta(minutes=15) <= timestamp:
				ts = timestamp
				try:
				#r1.rpush('station'+st_no+'_'+bssid,timestamp)
					r2.rpush(bssid+"_"+st_no,timestamp)
					r2.hset('station_'+st_no,bssid,ts)
					print bssid+" updated"
				except Exception, e:
					print str(e)	
#r1 = connect_server()
r2 = connect_local()
atexit.register(save_all)				
#probes = read_data()
				
sniff(iface=i,prn=handler,store=0)