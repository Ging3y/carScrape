#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 18:04:30 2018

@author: tylerjones
"""

import requests
from bs4 import BeautifulSoup
import csv


def writeCSV(myArray):
    
    try:
        with open("/Users/tylerjones/Desktop/output.csv", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            for item in myArray:
                writer.writerow([item])
        print("File written to desktop")
    except Exception as e:
        print("Error: " + str(e))

url = "https://www.craigslist.org/about/sites#US"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


sections = list(soup.find_all("div", {"class": "colmask"}))
secAlt = soup.find_all("li")

X = []
for tag in secAlt:
    print(str(tag.text))
    X.append(str(tag.text))
    
    

writeCSV(X)
    
    
    
    
#    tdTags = tag.find_all("a")
#    for tag2 in tdTags:
#        print(tag2.text)
        
#        box = headers.find_all("div", {"class": "box box_1"})
#        for boX in box:
#            print(boX.text)
#        print(tag2.text)
        
    
#    print(testTag.get_text())

#print(sections[0])






#divTag = soup.find_all("div", {"class": "tablebox"}):
#for tag in divTag:
#    tdTags = tag.find_all("td", {"class": "align-right"})
#    for tag in tdTags:
#        print tag.text