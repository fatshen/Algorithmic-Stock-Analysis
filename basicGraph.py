import time,datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

eachStock = 'TSLA', 'AAPL'

def graphData(stock): 
	try: 
		stockFile = stock+'.txt'
		
		date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={0: mdates.strpdate2num('%Y%m%d')})

		fig = plt.figure()
		axis_1 = plt.subplot(2,1,1)
		axis_1.plot(date, openp)
		axis_1.plot(date, highp)
		axis_1.plot(date, lowp)
		axis_1.plot(date, closep)
		plt.ylabel('Stock Price')
		axis_1.grid(True)

		axis_2 = plt.subplot(2,1,2,sharex=axis_1)
		axis_2.bar(date, volume)
		plt.ylabel('Volume')
		axis_2.grid(True)



		axis_1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		for label in axis_1.xaxis.get_ticklabels():
			label.set_rotation(45)
		for label in axis_2.xaxis.get_ticklabels():
			label.set_rotation(45)
		
		plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)
		plt.suptitle(stock+' Stock Price')
		plt.xlabel('Date')
		plt.show()

	except Exception, e: 
		print 'Failed_main', str(e)

for stock in eachStock:
	graphData(stock)
	
