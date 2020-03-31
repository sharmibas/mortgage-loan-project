# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 2017

@author(s): Jai Crespo and Daniel Mower
This script downloads the Freddie Mac Single Family Loan Level Dataset

"""
import requests, zipfile, io, lxml.html
from bs4 import BeautifulSoup as bs

def ExtractHiddenItems(response):
    login_html = lxml.html.fromstring(response.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    payload = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    return payload




downloadToPath = 'C:\\Users\\DanielMower\\Desktop\\FreddieMac_SFLL_Dataset'  # <=  ENTER THE PATH TO WHICH YOU WOULD LIKE TO SAVE THE DATA  EX: 'C:\\Users\\billybob\\Desktop\\FreddieData'


userName = ''  # <=  ENTER YOUR ACCOUNT HERE  EX: 'billybob@gmail.com'
passWord = '' # <=  ENTER YOUR PASSWORD HERE  EX: 'iSDKJ[}09'

origin = "https://freddiemac.embs.com"
authURL = origin + '/FLoan/secure/auth.php'
loginURL = origin + '/FLoan/secure/login.php'
downloadURL = origin + '/FLoan/Data/download.php'

#------------------------------------------------------------------------------
#-- Create session and Add Headers
#------------------------------------------------------------------------------
mySession = requests.Session()
mySession.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.57'
mySession.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
mySession.headers['Content-Type']='application/x-www-form-urlencoded'
mySession.headers['Accept-Encoding']='gzip, deflate, br'
mySession.headers['Accept-Language']='en-US,en;q=0.8'
mySession.headers['Upgrade-Insecure-Requests']='1'
mySession.headers['Cache-Control']= 'max-age=0'
mySession.headers['referer']= loginURL
mySession.headers['origin']= origin

#------------------------------------------------------------------------------
#-- Get login page html and extract hidden items. 
#-- This will also grab the needed session token
#------------------------------------------------------------------------------
response = mySession.get(loginURL, verify=False)

#------------------------------------------------------------------------------
#-- need to set payload manually as poor parsing practice on
#-- server side requires username appear first in form request
#------------------------------------------------------------------------------
userName = userName.replace('@', '%40');
passWord = passWord.replace('@', '%40');
payload='username=' + userName + '&password=' + passWord

#------------------------------------------------------------------------------
#-- Mimic request from login.php to auth.php
#------------------------------------------------------------------------------
response = mySession.post(authURL, verify=False, data=payload)
mySession.headers['referer']= loginURL
response=mySession.get(downloadURL, verify=False)

#------------------------------------------------------------------------------
#-- Set up payload for download page
#------------------------------------------------------------------------------
payload = ExtractHiddenItems(response)
payload['accept']='Yes'
payload['action']='acceptTandC'
payload['acceptSubmit']='Continue'
mySession.headers['referer']= loginURL

response=mySession.post(downloadURL, verify=False, data=payload)
#print(response.text)

#------------------------------------------------------------------------------
#-- Download and extract the data files.
#------------------------------------------------------------------------------

soup = bs(response.text, "lxml") # lxml is just the parser for reading the html

links = soup.find_all('a')
#linkList = list()
#[linkList.append(link.string) for link in links]
counter = 0
startCount = 0

for link in links:
    if counter >= startCount:
        fileURL = origin + "/FLoan/Data/" + link.string
        fileName = link.string
        print(fileURL, '\n', fileName, '\n')
        r = requests.get(fileURL)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(downloadToPath)
        counter += 1

mySession.close
