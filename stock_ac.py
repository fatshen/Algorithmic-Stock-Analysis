import urllib2

stocksToPull = 'AAPL', 'GOOG', 'MSFT', 'CMG', 'TSLA', 'EBAY', 'AMZN'

def pullData(stock): 
	try: 
		fileLine = stock+'.txt'
		urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' +stock+ '/chartdata;type=quote;range=1y/csv' 
		sourceCode = urllib2.urlopen(urlToVisit).read()
		splitSource = sourceCode.split('\n') 
		
		for eachL in splitSource:
			splitLine = eachL.split(',')
			if len(splitLine) == 6: 
				if 'values' not in eachL:
					saveFile = open(fileLine, 'a')
					lineToWrite = eachL+'\n'
					saveFile.write(lineToWrite)
		print 'Pulled', stock

	except Exception, e: 
		print 'main_loop_exception', str(e) 

for eachStock in stocksToPull: 
	pullData(eachStock)


pullData(stocksToPull) 
