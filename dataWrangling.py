#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 12:40:22 2018

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
import csv


df = pd.read_csv("/Users/tylerjones/Desktop/INPUT.csv", sep=",")

cities = df.iloc[:, 2]

path = "/Users/tylerjones/Desktop/finalData.csv"

stateList = []
cityList = []
for i in range (len(df)):
    stateList.append(str(df.iloc[i][0]))
    cityList.append(str(df.iloc[i][1]))
    
def getCarCount(strURL):
    
    newStr = "https://" + str(strURL) + ".craigslist.org/search/cta"
    #Connect to appropriate URL
    page = requests.get(newStr)
    
    #Open BeautifulSoup Object
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #Craigslist makes it easy to find all the data we want in the "result row" class
    mydivs = list(soup.findAll("li", {"class": "result-row"}))
    
    #Y is the vector that holds the cost of each car
    myCount = 0
    
    #Loop through and pull cost of each car on front page
    for i in range(len(mydivs)):
        car = mydivs[i]
        cost = list(car.children)[1]
        
        try:
            costFlt = float(cost.get_text().replace("$",""))
            myCount += 1
        except:
            myCount += 0
        
    return myCount

def genOutPut(dataArray):
    
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range(len(dataArray)):
            writer.writerow(dataArray[i])

            
def testLink(city, printErrors):
    
    if city == "NaN":
        city = cityList[i]
    
    if "/" in str(city):
        city = city.split("/")[0]
        city = city.strip()
    
    if "-" in str(city):
        city = city.split("-")[0]
        city = city.split()
        
    newStr = "https://" + str(city) + ".craigslist.org/search/cta"
    print(newStr)
    
    try:
        page = requests.get(newStr)
        return True
    except:
        return False




data = []
for i in range(10):
    
    if testLink(cities[i], True):
#        print("Success: " + str(cityList[i]))
        data.append([df.iloc[i][0], cityList[i], cityList[i], getCarCount(cityList[i])])
    else:
#        print("Fail: " + str(cityList[i]))
        data.append([df.iloc[i][0], cityList[i], "Nan", "0"])

            
genOutPut(data)
    

       
        
        
        
