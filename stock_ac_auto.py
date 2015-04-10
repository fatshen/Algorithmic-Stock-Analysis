import urllib2, datetime, time

stocksToPull = 'AAPL', 'GOOG', 'MSFT', 'CMG', 'AMZN', 'EBAY', 'TSLA'

def pullData(stock): 
	try: 
		print'Currently Pulling',stock
		print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:$M:$S'))
		urlToVisit = 'http://chatapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=5d/csv'
		saveFileLine = stock+'.txt'
		
		try:
			readExistingData = open(saveFileLine, 'r').read()
			splitExisting = readExistingData.split('\n')
			mostRecentLine = splitExisting[-2]
			lastUnix = int(mostRecentLine.split(',')[0])
		except:
			lastUnix = 0 

	except Exception,e:
		print 'main_loop', str(e)


for eachStock in stocksToPull:
	pullData(eachStock)
