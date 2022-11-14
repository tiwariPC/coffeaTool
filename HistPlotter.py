
import mplhep
import matplotlib.pyplot as plt

def plotHist(hist):
	plt.style.use(mplhep.style.ROOT)
	fig,ax = plt.subplots()
	# Compare this to the style of the plot drawn previously
	hist.plot1d(ax=ax)#overlay="flavor", density=True)
	plt.xlabel('Mbb')  
	plt.ylabel('Events')
	plt.savefig('line_plot.pdf') 	
