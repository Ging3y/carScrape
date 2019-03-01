#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 23:07:02 2018

@author: tylerjones
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn
import sys
import numpy as np
import pandas as pd
import statistics

df = pd.read_csv("data/output.csv", sep="\n")

cityList = []
for i in range (len(df)):
    cityList.append(str(df.iloc[i][0]))
    

""" Basic Links And Structure """
#Organization: p = page number
# https://grandisland.craigslist.org/search/cta?s=120*(p)
urlProvo = "https://provo.craigslist.org/search/cta"
urlPortland = "https://portland.craigslist.org/search/cta"
urlGrandIsland = "https://grandisland.craigslist.org/search/cta"
totalCities = []
totalCities.append(urlProvo)
totalCities.append(urlPortland)
totalCities.append(urlGrandIsland)

def genLink(city):
    
    newStr = "https://" + str(city) + ".craigslist.org/search/cta"
    return newStr


def testLinks(url):
      
    try:
        page = requests.get(genLink(url))
    except:
        print(url)

#Param: url, Output Graph, Print Errors
def genCarGraph(strURL, genGraph, printErrors):
    
    #Connect to appropriate URL
    try:
        page = requests.get(strURL)
    except:
        if printErrors:
            print("No connection or page not found")
            print("URL: " + strURL)
        return
    
    #page = requests.get(strURL) //Print raw page html if needed
    
    #Generate Header Title For Graph Based On Location
    header = strURL[strURL.index("//")+2:strURL.index("craigslist")-1]
    
    #Open BeautifulSoup Object
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #Craigslist makes it easy to find all the data we want in the "result row" class
    mydivs = list(soup.findAll("li", {"class": "result-row"}))
    
    #Y is the vector that holds the cost of each car
    Y = []
    
    #Loop through and pull cost of each car on front page
    for i in range(len(mydivs)):
        car = mydivs[i]
        cost = list(car.children)[1]
        
        #Occasionally the text is left blank, if it is valid, we add it to our vector Y
        try:
            costFlt = float(cost.get_text().replace("$",""))
            Y.append(costFlt)
        except:
            if printErrors: 
                Z = Y
                #print("Blank space, moving on...")
    
    #Create X axis vector based on number of valid car prices collected        
    X = np.arange(len(Y))
    Y.sort()
    
    #Generate a simple bar graph 
    if genGraph and (len(X) != 0):
        costMedian = statistics.median(Y)
        plt.figure(figsize=(10,10))
        plt.axes().get_xaxis().set_visible(False)
        plt.title(str(len(X)) + " Craiglist Car Prices - " + header.title() + " \n $" + str(costMedian), fontsize=20)
        plt.bar(X, Y)
        plt.show()
        
def getCarData(strURL, printErrors):
    
    #Connect to appropriate URL
    try:
        page = requests.get(strURL)
    except:
        if printErrors:
            print("No connection or page not found")
        return
    
    #Open Beautiful Soup Module
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #Target the class which contains all of the data
    mydivs = list(soup.findAll("li", {"class": "result-row"}))
    
    #Count of cars with full data
    totalCars = 0
    
    #Loop through each of the 120 front page listing cars
    for i in range(len(mydivs)):
        car = mydivs[i]
        completeData = True
        #print(car)
        
        carTitle = car.find_all("a", {"class": "result-title hdrlnk"})[0].get_text()
        
        try:
            carPrice = car.find_all("span", {"class": "result-price"})[0].get_text()
        except:
            carPrice = "Nan"
            completeData = False
#            print("ERROR - Car Price")
#            print(car)
#            return
        try:
            carLoc = car.find_all("span", {"class": "result-hood"})[0].get_text().replace(" ","")
        except:
            carLoc = "Nan"
            completeData = False
#            print("ERROR - Car Location")
#            print(car)
#            return
        carDate = str(car.find_all("time", {"class": "result-date"}))
        carDate = carDate[carDate.index("time=")+6:carDate.index("title=")-2]
        
        if completeData:
            totalCars += 1
            
            print(carTitle)
            print(carLoc)
            print(carPrice)
            print(carDate)
            print("\n")
        
    print("Total Full Info Cars: " + str(totalCars))

for i in totalCities:
    genCarGraph(i, True, False)
    
    
    
#for i in range(len(cityList)):
#    genCarGraph(genLink(cityList[i]), True, False)
   
#for i in range(len(cityList)):
#    testLinks(cityList[i])
    
    
        
#print(genLink(cityList[-4]))

#getCarData(genLink(cityList[-4]), True)

#genCarGraph(genLink(cityList[cityList.index("hawaii")]), True, True)
    
    





