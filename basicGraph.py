import time,datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick 
import matplotlib
matplotlib.rcParams.update({'font.size': 9})

eachStock = 'TSLA','AAPL'

def graphData(stock): 
	try: 
		stockFile = stock+'.txt'
		
		date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={0: mdates.strpdate2num('%Y%m%d')})

		x = 0
		y = len(date)
		candle_Ar = []
		while x < y: 
			appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
			candle_Ar.append(appendLine)
			x += 1 
		
		fig = plt.figure(facecolor='#07000d')
		axis_1 = plt.subplot2grid((5,4),(0,0), rowspan=4, colspan=4, axisbg='#07000d')
		candlestick(axis_1,candle_Ar,width=.5,colorup='#9eff15',colordown='#ff1717')
		
		axis_1.yaxis.label.set_color('w')
		axis_1.spines['bottom'].set_color("#5998ff")
		axis_1.spines['top'].set_color("#5998ff")
		axis_1.spines['left'].set_color("#5998ff")
		axis_1.spines['right'].set_color("#5998ff")
		axis_1.tick_params(axis='y', colors='w')
		plt.ylabel('Stock Price')
		
		volumeMin = volume.min()
		
		axis_1.grid(True, color='w')

		axis_2 = plt.subplot2grid((5,4), (4,0), sharex=axis_1,rowspan=1,colspan=4,axisbg='#07000d')
		axis_2.plot(date, volume, color="#00ffe8", linewidth=.8)
		axis_2.fill_between(date,volumeMin, volume, facecolor='#00ffe8',alpha=.5)	
		axis_2.axes.yaxis.set_ticklabels([])
		plt.ylabel('Volume', color='w')

		axis_2.grid(False)

		axis_2.spines['bottom'].set_color("#5998ff")
		axis_2.spines['top'].set_color("#5998ff")
		axis_2.spines['left'].set_color("#5998ff")
		axis_2.spines['right'].set_color("#5998ff")
		axis_2.tick_params(axis='x', colors='w')
		axis_2.tick_params(axis='y', colors='w')

		axis_1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		for label in axis_1.xaxis.get_ticklabels():
			label.set_rotation(45)
		for label in axis_2.xaxis.get_ticklabels():
			label.set_rotation(45)
		
		plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)
		plt.suptitle(stock, color='w')
		#plt.xlabel('Date', color='w')

		
		plt.setp(axis_1.get_xticklabels(), visible=False)
		
		plt.subplots_adjust(left=.09,bottom=.14,right=.94,top=.95,wspace=.20,hspace=0)
		plt.show()
		fig.savefig('example.png', facecolor=fig.get_facecolor())

	except Exception, e: 
		print 'Failed_main', str(e)

for stock in eachStock:
	graphData(stock)
	
