#Francisco Francillon :) Final Project; Programming analytics
import time #this module provides various time-related functions
import itertools #provides various functions that work on iterateors to produce complex iterators
import requests #allows to send HTTP/1.1 requests 
import json #JavaScript Object Notation/ the data in the API is stored in the format 
import pandas as pd #use to create dataframe
from bs4 import BeautifulSoup # parsing HTML document, and extracting data from HTML
from matplotlib import pyplot as plt #allow the creation of visual graph such as bar, line, and scatter graph  

#list of url to scrape from 3 sources
url = ['https://en.wikipedia.org/wiki/East_Coast_of_the_United_States',
       'https://en.wikipedia.org/wiki/Southeastern_United_States', 
      'https://en.wikipedia.org/wiki/List_of_largest_cities_on_the_United_States_West_Coast']

city = [] #hold city data scrape from each url
population = [] #hold population data scrape from each url
state = [] #hold state data scrape from each url
wind = [] #hold wind data collected from API
aqicn = [] #hold Air Quality China MEP stadard Data from API
aqius = [] # hold Air Quality US EPA stadard data from API 
url_list = [] #will store url generated from the API

def webScrape(): #function for webscrapping
    #webscrapping from first url
    page = requests.get(url[0]) #making the request to the server for the fitst url
    soup = BeautifulSoup(page.content, 'html.parser') #parsing through the content using BeutifulSoup creates a parse tree for parsed pages that can be used to extract data from HTML
    letGetit = soup.find_all('table', class_="wikitable")#find all table and class "wiketable" this is where the data we looking for is
    correct_table = letGetit[0]# the table is index 0
    rows = correct_table.find_all('tr') #table row need to find all tr
    for row in rows:
        cells = row.find_all('td')#the tag for table data is strored in the td tag
        if (len(cells)== 4): #table consist of 4 rows
            #the reason for replacing the blank space to %20 is so the api can make the request, according to the documentation city and state with space needs %20 
            city.append(cells[0].get_text().strip(' ').strip('\n').replace('[a]','').replace(' ','%20'))#appending city from scrapped data
            population.append(cells[1].get_text().rstrip('\n').replace(',','')) #appending population from scrape data
            state.append(cells[3].get_text().rstrip('\n').replace('\xa0','').replace(' ','%20')) #appending state from scapped data
           
    #scrapping data from 2nd url 
    page = requests.get(url[1]) #making the request to the server for the 2nd url
    soup1 = BeautifulSoup(page.content, 'html.parser')#parsing through the content using BeutifulSoup creates a parse tree for parsed pages that can be used to extract data from HTML
    letGetit1 = soup1.find_all('table', class_="wikitable")#find all table and class "wiketable" this is where the data we looking for is
    correct_table1 = letGetit1[2]# the table is index 2
    rows1 = correct_table1.find_all('tr') #table row need to find all tr
    for row in rows1:
        cells = row.find_all('td')#the tag for table data is strored in the td tag
         #the reason for replacing the blank space to %20 is so the api can make the request, according to the documentation city and state with space needs %20 
        if (len(cells)== 4):#table consist of 4 rows
            city.append(cells[1].get_text().strip(' ').strip('\n').replace('[a]','').replace(' ','%20')) #appending city from scrapped data
            state.append(cells[2].get_text().rstrip('\n').strip('\xa0')) #appending state from scapped data
            population.append(cells[3].get_text().rstrip('\n').replace(',','').replace(' ','%20')) #appending population from scrape data
#scrapping data from 2nd url 
    page = requests.get(url[2]) #making the request to the server for the 2nd url
    soup2 = BeautifulSoup(page.content, 'html.parser')#parsing through the content using BeutifulSoup creates a parse tree for parsed pages that can be used to extract data from HTML
    letGetit2 = soup2.find_all('table', class_="wikitable")#find all table and class "wiketable" this is where the data we looking for is
    correct_table2 = letGetit2[1] # the table is index 1
    rows2 = correct_table2.find_all('tr') #table row need to find all tr
    for row in rows2:
        cells = row.find_all('td')#the tag for table data is strored in the td tag
        #the reason for replacing the blank space to %20 is so the api can make the request, according to the documentation city and state with space needs %20 
        if (len(cells)== 7):#table consist of 7 rows
            city.append(cells[1].get_text().strip(' ').strip('\n').replace('[a]','').replace(' ','%20'))#appending city from scrapped data
            state.append(cells[2].get_text().rstrip('\n').strip('\xa0')) #appending state from scapped data
            population.append(cells[4].get_text().rstrip('\n').replace(',','').replace(' ','%20'))#appending population from scrape data
            

def Dataframe():
    #removing those index below because of bugs that was raised by thr API
    city.pop(66)
    state.pop(66)
    population.pop(66)
    #removing those index below because of bugs that was raised by thr API
    city.pop(11)
    state.pop(11)
    population.pop(11)
    #removing those index below because of bugs that was raised by thr API
    city.remove('Washington,%20D.C.')
    state.remove('District%20of%20Columbia')
    population.remove('705749')
    #removing those index below because of bugs that was raised by thr API
    city.pop(40)
    state.pop(40)
    population.pop(40)
    #removing those index below because of bugs that was raised by thr API
    city.pop(43)
    state.pop(43)
    population.pop(43)
    #removing those index below because of bugs that was raised by thr API
    city.remove('Washington')
    state.remove('District of Columbia')
    population.remove('672228')
    #deleting index 105 and stopping at 186 to reduce data, API allows 5 API call, having all those city and state would take close to 2hrs to collec data
    del city[105:186]
    del state[105:186]
    del population[105:186]
    
    df = pd.DataFrame()#creating data frame 
    df['city'] = city #naming city column
    df['state'] = state #naming state column
    df['population'] = population #naming population column
    df['population'] = df.population.astype(float) #converting population from string to float
    

    key = 'API KEY GO HERE'#my API key, allows 5 calls per min, and 500 per day
    for(i,j) in zip(city, state):#creating the API with scrapped city and state, and also adding API key; will be stored in url_list
        apiUrl = f'http://api.airvisual.com/v2/city?city={i}&state={j}&country=USA&key={key}'
        x = apiUrl
        url_list.append(x)
    for i in url_list:
        response = requests.request("GET", i)#making request to API
        #print(i) this was used to debug the request to see which link was not working 
        data = response.json() #getting the json file and storing in data variable 
        aqicn.append(data['data']['current']['pollution']['aqicn'])#appeding the Air Quality China MEP stadard
        aqius.append(data['data']['current']['pollution']['aqius'])#appeding the Air Quality US EPA stadard
        wind.append(data['data']['current']['weather']['ws']) #appeding the wind 
        time.sleep(14) #setting a 14 second timer so I do not go over the 5 calls per min. doing 4 call per min to be safe

    df2 = pd.DataFrame()#second data frame to store data from API
    df2['Air Quality China MEP stadard'] = aqicn #naming the column for Air Quality China MEP standard
    df2['Air Quality US EPA stadard'] = aqius #naming the column for Air Quality US EP standard
    df2['wind'] = wind #naming column for wind
    df3 = pd.concat([df,df2], axis=1) # merging fist dataframe with df2
    print(df3.head(10))#displaying the first 10 row
    print(df3.describe())#print statistical description of df3
    df3.to_csv('Totalpolution.csv')#saving df3 as csv file
#function for scatter graph
def create_graph_scatter(width, height, x, y, title, x_label, y_label):
    #creating scatter graph for city an AQ US EPA stadard
    plt.figure(figsize=(width, height)) #setting adjucing size
    plt.scatter(x,y) #x, and y axis
    plt.title(title) #title of scatter graph
    plt.xlabel(x_label) #naming x lable
    plt.ylabel(y_label)#naming y label
    print(plt.show) #displaying graph
#function for bar graph
def create_graph_bar(width, height, x, y, title, x_label, y_label):
    #creating scatter graph for city an AQ US EPA stadard
    plt.figure(figsize=(width, height)) #setting adjucing size
    plt.barh(x,y) #x, and y axis
    plt.title(title) #title of bar graph
    plt.xlabel(x_label) #naming x lable
    plt.ylabel(y_label)#naming y label
    print(plt.show) #displaying graph

webScrape()#calling function that is responsible for web scrapping
Dataframe()#calling function to create dataframe and work on API
create_graph_scatter(20,20,aqius,city, 'Air Quality US EPA stadard vs Population','Air Quality US EPA stadard','City')#this is the first scatter graph showing relationship Air Quality US EPA stadard vs Population
create_graph_scatter(10,10,wind,aqius, 'Air Quality US EPA stadard vs Wind','Wind','Air Quality US EPA stadard')#this is the second scatter graph showing relationship Air Quality US EPA stadard vs Wind
create_graph_bar(5,20,city,aqius, 'Air Quality US EPA stadard vs City','Air Quality US EPA stadard','City')#this is the bargraph showing relationship Air Quality US EPA stadard vs City



