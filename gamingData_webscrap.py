### import libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
import pandas as pd
import matplotlib.pyplot as plt

### function list:

# convert a percentage string to numeric float
def percentageToFloat(x):
    return float(x.strip('%')) / 100

# remove comma and convert a string to numeric
def stringToNumeric(x):
    return int(re.sub(',','',x))

# extract and clean up the content from the website
def getContent(e):
    start = e.get_attribute('innerHTML')
    # remove HTML tags from our content if it exists.
    soup = BeautifulSoup(start, features="lxml")
    return soup.get_text()


### webscraping process:
DRIVER_PATH = "E:/python/ChromeDriver/chromedriver"
URL = "https://www.op.gg/statistics/champions?region=global"

browser = webdriver.Chrome(service=Service(DRIVER_PATH))
browser.get(URL)

# Give the browser time to load all content.
time.sleep(6)

rawChampion = browser.find_elements(by=By.CSS_SELECTOR, value='strong')
champion = []
for e in rawChampion:
    rawString = getContent(e)
    champion.append(rawString)
# remove the last/invalid data instance
champion.pop()


rawGamesPlayed = browser.find_elements(by=By.CSS_SELECTOR, value='.css-16dwbfw')
gamesPlayed = []
for e in rawGamesPlayed:
    rawString = getContent(e)
    rawString = stringToNumeric(rawString)
    gamesPlayed.append(rawString)



rawKDA = browser.find_elements(by=By.CSS_SELECTOR, value='.e1alsbyt4')
KDA = []
for e in rawKDA:
    rawString = getContent(e)
    KDA.append(rawString)


rawWinRate = browser.find_elements(by=By.CSS_SELECTOR, value='.exo2f211+ .e1alsbyt6 .e1alsbyt0')
winRate = []
for e in rawWinRate:
    rawString = getContent(e)
    rawString = percentageToFloat(rawString)
    winRate.append(rawString)


rawPickRate = browser.find_elements(by=By.CSS_SELECTOR, value='.css-12go93c')
pickRate = []
for e in rawPickRate:
    rawString = getContent(e)
    rawString = percentageToFloat(rawString)
    pickRate.append(rawString)


rawBanRate = browser.find_elements(by=By.CSS_SELECTOR, value='.e1alsbyt6+ .e1alsbyt3')
banRate = []
for e in rawBanRate:
    rawString = getContent(e)
    rawString = percentageToFloat(rawString)
    banRate.append(rawString)


rawCS = browser.find_elements(by=By.CSS_SELECTOR, value='.e1alsbyt3:nth-child(8)')
CS = []
for e in rawCS:
    rawString = getContent(e)
    rawString = float(rawString)
    CS.append(rawString)


rawGold = browser.find_elements(by=By.CSS_SELECTOR, value='.css-r5hguk~ .e1alsbyt3+ .e1alsbyt3')
gold = []
for e in rawGold:
    rawString = getContent(e)
    rawString = stringToNumeric(rawString)
    gold.append(rawString)



# create a zipped list of tuples from above lists
zippedList = list(zip(champion,gamesPlayed,KDA,winRate,pickRate,banRate,
                      CS,gold))

# create data frame from zipped list
df = pd.DataFrame(zippedList,columns=['champion','games played',
                                      'KDA','win rate','pick rate',
                                      'ban rate','CS','gold'])

# save as a csv file
df.to_csv('leagueData.csv')
