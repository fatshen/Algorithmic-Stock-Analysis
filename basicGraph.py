import time,datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick 
import matplotlib
import pylab
import urllib2
matplotlib.rcParams.update({'font.size': 9})

eachStock = 'EBAY','AAPL'


def rsiFunction(prices,n=14): 

	deltas = np.diff(prices)
	seed = deltas[:n+1]
	down = -seed[seed<0].sum()/n
	up = seed[seed>=0].sum()/n 
	rs = up/down
	rsi = np.zeros_like(prices)
	rsi[:n] = 100. - 100. /(1. +rs)

	for i in range(n, len(prices)):
		deltaz = deltas[i-1]
		if deltaz > 0: 
			upval = deltaz
			downval = 0. 
		else:
			upval = 0. 
			downval = -deltaz

		up = (up*(n-1)+upval)/n
		down = (down*(n-1)+downval)/n
		
		rs = up/down
		rsi[i] = 100. - 100./(1.+rs)

	return rsi

def movingAverage(values, window):
	
	weights = np.repeat(1.0, window)/window
	smas = np.convolve(values, weights, 'valid')
	return smas

def expMovingAverage(values,window):
	weights = np.exp(np.linspace(-1.,0.,window))
	weights /= weights.sum()
	a = np.convolve(values, weights,mode='full')[:len(values)]
	a[:window] = a[window]
	return a


def computeMACD(x,slow=26, fast=12):
	'''
	MACD = 12ema - 26ema
	signal line = 9ema of the MACD
	histogram = MACD line - signal line
	'''
	emaslow = expMovingAverage(x, slow)
	emafast = expMovingAverage(x, fast)

	return emaslow, emafast, emafast-emaslow

def graphData(stock,MA1,MA2): 
	try: 
		try:
			print 'Pulling Data on', stock
			urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=3y/csv'
			stockFile = []
			try:
				sourceCode = urllib2.urlopen(urlToVisit).read()
				splitSource = sourceCode.split('\n')
				for eachLine in splitSource:
					splitLine = eachLine.split(',')
					if len(splitLine) == 6:
						if 'values' not in eachLine:
							stockFile.append(eachLine)
			except Exception, e: 
				print str(e), 'Error: Orginization'

		except Exception, e:
			print str(e), 'Failed to pull price Data'
	






		#stockFile = stock+'.txt'
		
		date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={0: mdates.strpdate2num('%Y%m%d')})

		x = 0
		y = len(date)
		candle_Ar = []
		while x < y: 
			appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
			candle_Ar.append(appendLine)
			x += 1


		Av1 = movingAverage(closep, MA1)
		Av2 = movingAverage(closep, MA2)
		
		SP = len(date[MA2-1:])

		label1 = str(MA1) + 'SMA'
		label2 = str(MA2) + 'SMA' 


		fig = plt.figure(facecolor='#07000d')
		
		axis_1 = plt.subplot2grid((6,4),(1,0), rowspan=4, colspan=4, axisbg='#07000d')
		candlestick(axis_1,candle_Ar[-SP:],width=.6,colorup='#53C156',colordown='#ff1717')
		axis_1.plot(date[-SP:],Av1[-SP:],"#e1edf9",label=label1,linewidth=1.5)
		axis_1.plot(date[-SP:],Av2[-SP:], "#4ee6fd", label=label2, linewidth=1.5)

		axis_1.grid(True, color='w')
		axis_1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		axis_1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
		plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
		axis_1.yaxis.label.set_color('w')
		axis_1.spines['bottom'].set_color("#5998ff")
		axis_1.spines['top'].set_color("#5998ff")
		axis_1.spines['left'].set_color("#5998ff")
		axis_1.spines['right'].set_color("#5998ff")
		axis_1.tick_params(axis='y', colors='w')
		axis_1.tick_params(axis='x', colors='w')
		plt.ylabel('Stock Price and Volume')


                maLeg = plt.legend(loc=9, ncol=2,prop={'size':6}, fancybox=True)
                maLeg.get_frame().set_alpha(0.4)
		textEd = pylab.gca().get_legend().get_texts()
		pylab.setp(textEd[0:5],color='w')

		
		rsi = rsiFunction(closep)

		rsiCol = '#1a8782'
		posCol = '#386d13'
		negCol = '#8f2020'

                ax0 = plt.subplot2grid((6,4), (0,0), sharex=axis_1, rowspan=1, colspan=4, axisbg="#07000d")
		ax0.plot(date[-SP:],rsi[-SP:], rsiCol, linewidth=1.5)
		
		ax0.axhline(70,color=negCol)
		ax0.axhline(30,color=posCol)
		ax0.fill_between(date[-SP:],rsi[-SP:],70,where=(rsi[-SP:]>=70),facecolor=negCol, edgecolor=negCol)
		ax0.fill_between(date[-SP:],rsi[-SP:],30,where=(rsi[-SP:]<=30),facecolor=posCol, edgecolor=posCol)
		#ax0.set_ylim(0,100)

		ax0.spines['bottom'].set_color("#5998ff")
		ax0.spines['top'].set_color("#5998ff")
		ax0.spines['left'].set_color("#5998ff")
		ax0.spines['right'].set_color("#5998ff")
		ax0.tick_params(axis='x', colors='w')
		ax0.tick_params(axis='y', colors='w')
		ax0.set_yticks([30,70])
		
		ax0.text(0.015, 0.95, 'RSI (14) ', va='top', color='w', transform=ax0.transAxes)

		#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))
		#plt.ylabel('RSI',color='w')
		
		volumeMin = 0

		'''
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
		
		'''
		
		ax1v = axis_1.twinx()
 	        ax1v.fill_between(date[-SP:],volumeMin, volume[-SP:], facecolor='#00ffe8',alpha=.5)	
		ax1v.axes.yaxis.set_ticklabels([])
		ax1v.grid(False)
		ax1v.spines['bottom'].set_color("#5998ff")
		ax1v.spines['top'].set_color("#5998ff")
		ax1v.spines['left'].set_color("#5998ff")
		ax1v.spines['right'].set_color("#5998ff")
		ax1v.set_ylim(0,3*volume.max())
		ax1v.tick_params(axis='x', colors='w')
		ax1v.tick_params(axis='y', colors='w')
		
		ax2 = plt.subplot2grid((6,4),(5,0),sharex=axis_1,rowspan=1,colspan=4,axisbg="#07000d")
                
		nslow = 26
		nfast = 12
		nema = 9 
		fillcolor = "#00ffe8"
		
		emaslow,emafast,macd=computeMACD(closep)
		ema9 = expMovingAverage(macd,nema)

		ax2.plot(date[-SP:],macd[-SP:],color="#4ee6fd",lw=2)
		ax2.plot(date[-SP:],ema9[-SP:],color='#e1edf9',lw=1)
		ax2.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:],0,alpha=0.5,facecolor=fillcolor,edgecolor=fillcolor)
		ax2.text(0.015, 0.95, 'MACD 12,26,9', va='top', color='w', transform=ax2.transAxes)
		#plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
		ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))


		ax2.spines['bottom'].set_color("#5998ff")
		ax2.spines['top'].set_color("#5998ff")
		ax2.spines['left'].set_color("#5998ff")
		ax2.spines['right'].set_color("#5998ff")
		ax2.tick_params(axis='x', colors='w')
		ax2.tick_params(axis='y', colors='w')
		#plt.ylabel('MACD', color='w')

		for label in ax2.xaxis.get_ticklabels():
			label.set_rotation(45)


		plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)
		plt.suptitle(stock, color='w')
		#plt.xlabel('Date', color='w')
		plt.setp(ax0.get_xticklabels(), visible=False)
		plt.setp(axis_1.get_xticklabels(), visible=False)
		
		plt.subplots_adjust(left=.09,bottom=.14,right=.94,top=.95,wspace=.20,hspace=0)
		plt.show()
		fig.savefig('example.png', facecolor=fig.get_facecolor())

	except Exception, e: 
		print 'Failed_main', str(e)

while True:
	stockToUse = raw_input('Enter a stock: ')
	graphData(stockToUse,12,24)
#for stock in eachStock:
	#graphData(stock,12,24)
	
