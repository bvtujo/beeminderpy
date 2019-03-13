import beeminderpy as beem
import sys
import time
import datetime
import settings
import re

NOW = datetime.datetime.now().timetuple()
CURRENTYEAR = NOW.tm_year
CURRENTMONTH = NOW.tm_mon
CURRENTDAY = NOW.tm_mday


monsterRegex = r'^\s*((?:(?:0?[1-9]|1\d|2\d|3[01])|(?:0?[1-9]|1[012])\s+(?:0?[1-9]|1\d|2\d|3[01])|(?:19[789]\d|20\d\d)\s+(?:0?[1-9]|1[012])\s+(?:0?[1-9]|1\d|2\d|3[01]))|\^+)\s+([\+\-]?(?:\d+\.?\d*|\.\d+)|\d+st(?:\d+\.?\d*|\.\d+)?|(?:\d*\:[0-5]\d(?:\:[0-5]\d)?|0?0?\:\d\d))(?:(?:\s+-(.*))|(?:\s+[\"\'\u201c\u201d](.*)[\"\'\u201c\u201d])?)\s*$'
m = re.match(monsterRegex, "2019 3 9 75 -comment")
n = re.match(monsterRegex, "2019 3 8 75 \"fdsj\"")
print(m.groups())
print(n.groups())

def timeTupleFromTimestamp(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).timetuple()

def timestampFromTimeTuple(timeTuple):
	return time.mktime(timeTuple)

def timestampFromYMD(year, month, day, h=0, m=0):
	dt = datetime.datetime(year, month, day, h, m)
	return time.mktime(dt.timetuple())

def timestampNow():
	return time.time()

def timeTupleNow():
	return timeTupleFromTimestamp(timestampNow())
 

def parseArgs(args, now=NOW):
	l = len(args)
	G = args[1]; #arg 1 is always goalname

	reDig = r'^\d+$' #match any number of digits
	reAl = r':alpha:+'
	argMatches = [re.match(reDig, i)  for i in args[1:]]
	nums = [(i,args[i+1]) for i in range(len(argMatches)) if argMatches[i] != None]
	comment = True if re.match(reAl, args[-1]) else False
	print(args)
	print(nums)
	print("comment", comment)


	HMSFMT = "%H:%M:%S"
	strtime = time.strftime(HMSFMT,now)
	if l < 3:
		print("Too few arguments")
	elif l == 3:
		#assume goal & value, date=today
		DT = now
		DV = args[2]
		DC = f"via beecli at {strtime}"
	elif l == 4:
		#assume goal, day of month, value
		DV = args[3]
	else:
		return

	return G, DT, DV, DC


if __name__=="__main__":

	print(sys.argv)
	print(parseArgs(sys.argv))
	input("press any key")
	BEEMINDER_USERNAME = settings.BEEMINDER_USERNAME
	BEEMINDER_AUTH_TOKEN = settings.BEEMINDER_AUTH_TOKEN

	BEEMINDER_GOAL = ''
	DATAPOINT_TIME = 0
	DATAPOINT_VALUE = 0
	DATAPOINT_COMMENT = ''
	HMSFMT = "%H:%M:%S"

	logfile = "../misc/beecli.log"

	bmndr = beem.Beeminder(BEEMINDER_AUTH_TOKEN)

	args = sys.argv
	BEEMINDER_GOAL = args[1]
	print("Beeminder goal: " + BEEMINDER_GOAL)

	if len(args) < 3:
		print("Too few arguments")
		quit()
	elif len(args) == 3:
		#assume goal, value, fill in time=now
		DATAPOINT_TIME = timestampFromTimeTuple(NOW)
		DATAPOINT_VALUE = args[2]
		strtime = time.strftime(HMSFMT,time.localtime())
		DATAPOINT_COMMENT = f"added at {strtime} by beecli"
		print(DATAPOINT_TIME)
		print(DATAPOINT_VALUE)
	elif len(args) == 4:
		if int(args[2]) > CURRENTDAY:
			DATAPOINT_TIME = timestampFromYMD(NOW[0], NOW[1]-1, int(args[2]), h=12)
		else:
			DATAPOINT_TIME = timestampFromYMD(NOW[0], NOW[1], int(args[2]), h=12)
		DATAPOINT_VALUE = args[3]
		strtime = time.strftime(HMSFMT,time.localtime())
		DATAPOINT_COMMENT = f"added at {strtime} by beecli"
	else:
		print("too many arguments")
		time.sleep(2)
		quit()
	try:
		print("creating beeminder datapoint")
		res = bmndr.create_datapoint(BEEMINDER_USERNAME, BEEMINDER_GOAL, DATAPOINT_TIME, DATAPOINT_VALUE, 
			comment=DATAPOINT_COMMENT)
		print(res)
		print("beeminder datapoint sent")
		with open(logfile, 'a+') as f:
			f.write(f"added datapoint of {DATAPOINT_VALUE} to {BEEMINDER_GOAL} at {strtime}\n")
	except:
		print("in except case")
		with open(logfile, 'a+') as f:
			f.write(f"failed to add datapoint of {DATAPOINT_VALUE} to {BEEMINDER_GOAL} at {strtime}\n")


