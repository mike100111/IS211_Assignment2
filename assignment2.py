# -*- coding: cp1252 -*-

import urllib2
import datetime
import logging
import argparse
import sys
import os

##Mehtod to download the data from the specified url
def downloadData(url):
    ##open url
    f = urllib2.urlopen(url)
    ##read data
    data = f.read()
    ##return read data to calling Method
    return data

##Method to parse the downloaded data in a valid dictionary
def processData(data):
    ##Get the configured logger
    logger = getLogger()
    ##Split the data int a list
    dataList = data.splitlines()
    ##Dictionary to store processed information
    processedData = {}
    ##loop throuhg data skipping first header line 
    for x in xrange(1, len(dataList)):
        ##Split data on commas
        splitData = dataList[x].split(",")       
        try:
            ## Attempt to parse data into dictionary{integer, tuple(string, date)}
            processedData[int(splitData[0])] = (splitData[1], datetime.datetime.strptime(splitData[2], "%d/%m/%Y"))
        except:
            ## Log error
            logger.error("Error processing line #{0} for ID #{1}".format( x, splitData[0]))
            
    return processedData  

## Method to display a persons data based on passed in Id
def displayPerson(id, personData):
    if id in personData:
        print("Person #{0} is {1} with a birthday of {2}".format(id, personData[id][0],personData[id][1].strftime("%Y-%m-%d")))
    else:
        print("No user found with that id")

def getLogger():

     ##configure logger
    logger = logging.getLogger(__name__)
    hdlr = logging.FileHandler('C:\Users\Meir\Documents\IS211\IS211_Assignment2\errors.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.ERROR)
    return logger

def main():

    ##Add the --url parameter requirement
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()   

    ##donwlaod csv data
    csvData = downloadData(sys.argv[1])

    ##Process csv data
    personData = processData(csvData)

    ## Request initial id
    id = input("Enter an id -> ")
    ##Continue loop while Id is greater than 0
    while id > 0:
        ## Display Person information
        displayPerson(id, personData)
        ##Request teh next ID
        id = input("Enter another id -> ")
    

main() 
