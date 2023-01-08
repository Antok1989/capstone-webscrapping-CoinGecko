from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.coingecko.com/en/coins/ethereum/historical_data/?start_date=2020-01-01&end_date=2021-06-30' 
url_get = requests.get(url,  headers = { 'User-Agent': 'Popular browser\'s user-agent', })
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'})
row = table.find_all('th', attrs={'class':'font-semibold text-center'})

row_length = len(row)

temp = [] #initiating a tuple

for i in range(0, row_length):

    #Get tanggal
    Date = table.find_all('th', attrs={'class':'font-semibold text-center'})[i].text
    
    volume = table.find_all('td', attrs={'class':'text-center'})[1 + i*4].text
    volume = volume.strip() #to remove excess white space
          
    temp.append((Date,volume))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date','volume'))

#insert data wrangling here
df['Date'] = pd.to_datetime(df['Date'], format = '%Y-%m-%d')
df['volume'] = df['volume'].str.replace(",","")
df['volume'] = df['volume'].str.replace("$","")
df['volume'] = df['volume'].astype('int64')
df = df.set_index('Date')


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["volume"].mean().round(2)}' #be careful with the " and ' 
	
	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)