# Python Script to Webscrap Data from User's Typeracer profile

# Imports
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Initializing Variables
dt = datetime.now()
WPM = []
accuracy = []
dates = []
runningAvg = []
raceCount = 0

# Ask for Username to run the script on 
usr = input("Username: ")

# Get the Number of Races to set the GET URL
print("Getting Number of Races...")
response = requests.get("https://data.typeracer.com/pit/profile?user="+ usr)
soup = BeautifulSoup(response.text, 'html.parser')
getRaceCount = soup.findAll('span', {"class": "Stat__Top"})
raceCount = getRaceCount[2].text

# Get HTML page with all the Race Data
print("Getting Race Information")
response = requests.get("https://data.typeracer.com/pit/race_history?user="+usr+"&n=" + raceCount + "&startDate=&universe=")
soup = BeautifulSoup(response.text, 'html.parser')

# Getting WPM and Accuracy
titles = soup.findAll('div', attrs={"class":"profileTableHeaderRaces"})
my_flag = True
for title in titles:
	if my_flag:
		WPM.insert(0, title.text.strip())
		my_flag = not my_flag
	else:
		accuracy.insert(0, title.text.strip())
		my_flag = not my_flag

# Getting dates for each races
getDates = soup.findAll('div', attrs={"class":"profileTableHeaderDate"})
for mdate in getDates:
	if(mdate.text.strip() == 'today'):
		dates.insert(0, dt.strftime('%b. %d, %Y'))
	else:
		dates.insert(0, mdate.text.strip())

# fix dates
rsum = 0
for i in range(len(dates)):
	dates[i] = dates[i].replace(',','')
	WPM[i] = WPM[i].split(" ")[0]
	rsum += int(WPM[i])
	runningAvg.append(int(rsum/(i+1)))

# write to txt file
print("Writing to text file")
with open('scores.txt', 'w') as f:
	for i in range(len(WPM)):
		f.write(dates[i]+","+WPM[i]+","+str(runningAvg[i])+","+accuracy[i]+"\n")
