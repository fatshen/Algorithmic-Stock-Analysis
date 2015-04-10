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
		axis_1 = plt.subplot(1,1,1)
		axis_1.plot(date, openp)
		axis_1.plot(date, highp)
		axis_1.plot(date, lowp)
		axis_1.plot(date, closep)

		axis_1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		for label in axis_1.xaxis.get_ticklabels():
			label.set_rotation(45)

		plt.show()

	except Exception, e: 
		print 'Failed_main', str(e)

for stock in eachStock:
	graphData(stock)
	
