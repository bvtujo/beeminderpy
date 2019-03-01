import beeminderpy as beem
import sys
import time
import datetime
import settings

def timeTupleFromTimestamp(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).timetuple()

def timestampFromTimeTuple(timeTuple):
	return time.mktime(timeTuple)

def timestampFromYMD(year, month, day, h=0, m=0):
	if month<1:
	dt = datetime.datetime(year, month, day, h, m)
	return time.mktime(dt.timetuple())

def timestampNow():
	return time.time()

def timeTupleNow():
	return timeTupleFromTimestamp(time.time())

def addData()

if __name__=="__main__":
	print(sys.argv)
	BEEMINDER_USER = settings.BEEMINDER_USER
	BEEMINDER_API_TOKEN = settings.BEEMINDER_AUTH_TOKEN

	BEEMINDER_GOAL = ''
	DATAPOINT_TIME = 0
	DATAPOINT_VALUE = 0
	DATAPOINT_COMMENT = ''
	NOW = time.time()
	NOW_T = timeTupleFromTimestamp(NOW)
	NOW_D = NOW_T[2]
	HMSFMT = "%H:%M:%S"

	logfile = "../misc/beecli.log"

	bmndr = beem.Beeminder(BEEMINDER_API_TOKEN)

	args = sys.argv
	print(args)

	BEEMINDER_GOAL = args[1]

	if len(args) < 3:
		print("Too few arguments")
		time.sleep(2)
		quit()
	elif len(args) == 3:
		#assume goal, value, fill in time=now
		DATAPOINT_TIME = NOW
		DATAPOINT_VALUE = args[2]
		strtime = time.strftime(HMSFMT,time.localtime())
		DATAPOINT_COMMENT = f"added at {strtime} by beecli"
	elif len(args) == 4:
		if int(args[2]) > NOW_D:
			DATAPOINT_TIME = timestampFromYMD(NOW_T[0], NOW_T[1]-1, int(args[2]))
		else:
			DATAPOINT_TIME = timestampFromYMD(NOW_T[0], NOW_T[1], int(args[2]))
		DATAPOINT_VALUE = args[3]
		strtime = time.strftime(HMSFMT,time.localtime())
		DATAPOINT_COMMENT = f"added at {strtime} by beecli"
	else:
		print("too many arguments")
		time.sleep(2)
		quit()
	try:
		bmndr.create_datapoint(BEEMINDER_USER, BEEMINDER_GOAL, DATAPOINT_TIME, DATAPOINT_VALUE, 
			comment=DATAPOINT_COMMENT)
		with open(logfile, 'a+') as f:
			f.write(f"added datapoint of {DATAPOINT_VALUE} to {BEEMINDER_GOAL} at {strtime}\n")
	except:
		with open(logfile, 'a+') as f:
			f.write(f"failed to add datapoint of {DATAPOINT_VALUE} to {BEEMINDER_GOAL} at {strtime}\n")


