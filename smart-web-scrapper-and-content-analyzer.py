import os
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.probability import ConditionalFreqDist 
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
import pandas as pd
import matplotlib.pyplot as plt



# Code to read all files from a directory
basepath = "D:\\py-scripts\\WebScraper1\\files\\"
regionDictionary = {}
wordDictionary = []
associationDictionary = {}
nltk.download('stopwords')
# Create a reference variable for Class SExprTokenizer 
def main():
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            htmlfile = open("D:\\py-scripts\\WebScraper1\\files\\"+entry, 'r')
            soup = BeautifulSoup(htmlfile, "html5lib")
            text = soup.get_text()
            #Get Region Meta Tag Value
            myregion = soup.find('meta',attrs={'name':'region'}).get("value",None)
            
            #check if meta tag content value is having multiple comma separated values
            if myregion.find(',')>-1:
                listRegion = myregion.split(',')
                for item in listRegion:
                    if item in regionDictionary:
                        getDictionay = regionDictionary[item]
                        addWordFrequency(getDictionay, text, item)
                        
                    else:
                        regionDictionary[item] = {}
                        getDictionay = regionDictionary[item]
                        addWordFrequency(getDictionay, text, item)
                        #print(regionDictionary)
            else:
                if myregion in regionDictionary:
                    getDictionay = regionDictionary[myregion] 
                    addWordFrequency(getDictionay, text, myregion)
                else:
                    regionDictionary[myregion] = {}
                    getDictionay = regionDictionary[myregion] 
                    addWordFrequency(getDictionay, text, myregion)
                    #print(regionDictionary)

        
def addWordFrequency(getDictionay, text, item):        
    tokenizer = RegexpTokenizer('\w+')
    # Create tokens
    tokens = tokenizer.tokenize(text)
    freqdist1 = nltk.FreqDist(tokens)
    stop_words = set(stopwords.words('english'))
    for myword, frequency in freqdist1.most_common():
        if myword not in stop_words:
            if myword in getDictionay:
                getDictionay[myword] = int(getDictionay[myword]) + frequency
            else:
                getDictionay[myword] = frequency

            if myword not in wordDictionary:
                wordDictionary.append(myword)
            
    regionDictionary[item] = getDictionay

def createAssociationTable():
    associationDictionary["words"] = wordDictionary
    for keys in  regionDictionary:
        associationDictionary[keys] = []

    for eachWords  in wordDictionary:
        for keys in  regionDictionary:
            getDictionay = regionDictionary[keys]
            if eachWords in getDictionay:
                getTempDict = associationDictionary[keys] 
                getTempDict.append(getDictionay[eachWords])
            else:
                getTempDict = associationDictionary[keys] 
                getTempDict.append(0)
    
    associationDictionary["words"] = wordDictionary
   

if __name__ == "__main__": 
    # calling the main function 
    main()
    createAssociationTable()
    #print(regionDictionary)  
    #print(wordDictionary)
    #print(associationDictionary)
    df = pd.DataFrame.from_dict(associationDictionary)
    df.to_csv(r'D:\py-scripts\WebScraper1\output.csv', index = False)
    print(pd.DataFrame.from_dict(associationDictionary))
    # Figures inline and set visualization style
    %matplotlib inline
    #sns.set()
    #freqdist1 = nltk.FreqDist(words_ns)
    # gca stands for 'get current axis'
    #ax = plt.gca()
    forgraph = pd.DataFrame.from_dict(associationDictionary).head(25)
    forgraph.plot(kind='bar',x='words',y='asia',figsize=(8, 8))
    forgraph.plot(kind='bar',x='words',y='us',figsize=(8, 8), color='red')
    forgraph.plot(kind='bar',x='words',y='europe',figsize=(8, 8), color='orange')
    #df.plot(25)
