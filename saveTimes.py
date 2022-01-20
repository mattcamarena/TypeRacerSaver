import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

dt = datetime.now()
WPM = []
percents = []
dates = []
runningAvg = []
# if I want to choose the username
usr = input("Username: ")

print("Getting Number of Races...")
# first reponse to get number of races to use on second request
response = requests.get("https://data.typeracer.com/pit/profile?user="+ usr)
soup = BeautifulSoup(response.text, 'html.parser')
getRaceCount = soup.findAll('span', {"class": "Stat__Top"})
raceCount = getRaceCount[2].text

print("Getting Race Information")
response = requests.get("https://data.typeracer.com/pit/race_history?user="+usr+"&n=" + raceCount + "&startDate=&universe=")
soup = BeautifulSoup(response.text, 'html.parser')

# Setting up times and percents variables
times = soup.findAll('div', attrs={"class":"profileTableHeaderRaces"})
my_flag = True
for title in times:
	if my_flag:
		WPM.insert(0, title.text.strip())
		my_flag = not my_flag
	else:
		percents.insert(0, title.text.strip())
		my_flag = not my_flag
# dates will need fix today into date...
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



print("Writing to text file")
# write to txt file
with open('scores.txt', 'w') as f:
	for i in range(len(WPM)):
		f.write(dates[i]+","+WPM[i]+","+str(runningAvg[i])+","+percents[i]+"\n")

