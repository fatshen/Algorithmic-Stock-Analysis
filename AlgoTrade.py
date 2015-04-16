import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time 

date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True, 
				  delimiter=',', 
				  converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')}); 

patternAr = []
pAr = []
avgLine = ((bid+ask)/2)

def precentChange(startPoint, currentPoint):
        return ((float(currentPoint)-startPoint)/abs(startPoint))*100.00

def patternStorage():
        patStartTime = time.time()
        x = len(avgLine)-30
        y = 11
        while y < x:
                pattern = []
                
                p1 = precentChange(avgLine[y - 10], avgLine[y - 9])
                p2 = precentChange(avgLine[y - 10], avgLine[y - 8])
                p3 = precentChange(avgLine[y - 10], avgLine[y - 7])
                p4 = precentChange(avgLine[y - 10], avgLine[y - 6])
                p5 = precentChange(avgLine[y - 10], avgLine[y - 5])
                p6 = precentChange(avgLine[y - 10], avgLine[y - 4])
                p7 = precentChange(avgLine[y - 10], avgLine[y - 3])
                p8 = precentChange(avgLine[y - 10], avgLine[y - 2])
                p9 = precentChange(avgLine[y - 10], avgLine[y - 1])
                p10 = precentChange(avgLine[y - 10], avgLine[y])

                outcomeRange = avgLine[y+20:y+30]
                currentPoint = avgLine[y]
                try:
                        avgOutcome = reduce(lambda x, y: x+y, outcomeRange) / len(outcomeRange)
                except Exception, e:
                        print str(e)
                        avgOutcome = 0

                futureOutcome = precentChange(currentPoint, avgOutcome)
                
                pattern.append(p1)
                pattern.append(p2)
                pattern.append(p3)
                pattern.append(p4)
                pattern.append(p5)
                pattern.append(p6)
                pattern.append(p7)
                pattern.append(p8)
                pattern.append(p9)
                pattern.append(p10)
                
                patternAr.append(pattern)
                pAr.append(futureOutcome)
               
                y += 1

        patEndTime = time.time()
        print len(patternAr)
        print len(pAr)
        print 'Pattern Storage took: ', patEndTime - patStartTime, 'Seconds'

def patternRecongnition():
        patForRec = []

        cP1 = precentChange(avgLine[-11], avgLine[-10])
        cP2 = precentChange(avgLine[-11], avgLine[-9])
        cP3 = precentChange(avgLine[-11], avgLine[-8])
        cP4 = precentChange(avgLine[-11], avgLine[-7])
        cP5 = precentChange(avgLine[-11], avgLine[-6])
        cP6 = precentChange(avgLine[-11], avgLine[-5])
        cP7 = precentChange(avgLine[-11], avgLine[-4])
        cP8 = precentChange(avgLine[-11], avgLine[-3])
        cP9 = precentChange(avgLine[-11], avgLine[-2])
        cP10 = precentChange(avgLine[-11], avgLine[-1])

        patForRec.append(cP1)
        patForRec.append(cP2)
        patForRec.append(cP3)
        patForRec.append(cP4)
        patForRec.append(cP5)
        patForRec.append(cP6)
        patForRec.append(cP7)
        patForRec.append(cP8)
        patForRec.append(cP9)
        patForRec.append(cP10)
                
        print patForRec
        

def graphRawFx(): 

	fig = plt.figure(figsize=(10,7))
	axis_1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)

	axis_1.plot(date,bid)
	axis_1.plot(date,ask)
	plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

	axis_1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H: %M: %S')) 
	for label in axis_1.xaxis.get_ticklabels(): 
		label.set_rotation(45)

	axis_1_2 = axis_1.twinx()
	axis_1_2.fill_between(date, 0, (ask-bid), facecolor='g', alpha=.3)

	
	plt.subplots_adjust(bottom=.23) 
	
	
	
	plt.grid(True) 
	plt.show()

