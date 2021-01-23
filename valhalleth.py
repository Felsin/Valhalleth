#valhall.eth eth 10k tracker
#start virtual environment first!
#mkvirtualenv -p $(which python3) bitcoin_notifications
#workon bitcoin_notifications
#to unpin all ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 ipfs pin rmipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 ipfs pin rm
#ipfs daemon
#cronjob scheduling - Every day at 6am PST
#crontab –e
#**** /home/pi/Desktop/Python/Website_refresh_valhalleth.py >/dev/null 2>&1
#list cronjobs crontab –l
#requires index.html and styles.html with the main section of your website starting with ETH Price and ending with last updates on their own line
#script by @felblob. Use freely with credit at your leasure
#buy ETH and BTC

#THIS RUNS ONCE A DAY AND POSTS TO TWITTER

#import

import requests
from time import sleep
from progress.bar import Bar
import os
from subprocess import run
import sys
from datetime import datetime
import sched
import time
import tweepy

#unpin old content
with open('ipfn_hashes.txt', 'r+') as f: #r+ is rw
    for line in f:
        pass
    last_liner = line
    
ipfsunpin = 'ipfs pin rm ' + str(last_liner)
print('found last pin..')
os.system(ipfsunpin)
print(ipfsunpin)



#unpin pinata
hash2 = str(last_liner)
print(last_liner)
hashs2 = hash2[:-1]
hashs3 = str(hashs2)
PINATA_API_URL1 = "https://api.pinata.cloud/pinning/unpin/" + hashs3
pinata_api_keys1 = ''
print('unpinning..')
print(pinata_api_keys1)

pinata_secret_api_keys1 = ''
myobj1 = {'hashToUnpin': hashs3}
print(myobj1)
headers = {'pinata_api_key': pinata_api_keys1,'pinata_secret_api_key':pinata_secret_api_keys1}

#lookup API and pin
print(headers)
response = requests.delete(PINATA_API_URL1,params = myobj1, headers=headers)

#response_json = response.json()
print(response.text)
time.sleep(60)

#store ticker
TICKER_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

#lookup API and print ETH in USD
response = requests.get(TICKER_API_URL)
response_json = response.json()
print('current price is:')
print(response_json["ethereum"]["usd"])

#build a progress bar
def build_progress_bar(bar_curr_num, bar_total_num):
    
    # first calculate the percentage of current progress.
    percentage = bar_curr_num / bar_total_num
    
    # get the percentage number.
    percentage_num = int(percentage * 100)
    
    # format the progress output text with above parameter's value.
    r = '\r[%s%s]%d%%' % ("#"*bar_curr_num, "-"*(bar_total_num - bar_curr_num), percentage_num)
    
    # print out the progress bar in console.
    return(r)

bar_total_num = 100

# set current progress bar number.
bar_curr_num =  int((response_json["ethereum"]["usd"]) / 100)

progresseth = str(build_progress_bar(bar_curr_num, bar_total_num))

#retrieve highest price
with open('ipfs/index.html', 'r+') as f: #r+ is rw
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("Highest") == True:
            highestever = i.replace('Highest Price Achieved: </strong>$','')
print('highest price is:')
print(highestever)

#delete the old progress bar 1/2
with open("ipfs/index.html", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("Progress:") != True:
            f.write(i)
    f.truncate()
#delete the old progress bar 2/2
with open("ipfs/index.html", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("[#") != True:
            f.write(i)
    f.truncate()
    
#delete the old price
with open("ipfs/index.html", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("Current Price:") != True:
            f.write(i)
    f.truncate()
    
#delete the old date
with open("ipfs/index.html", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("Last Updated:") != True:
            f.write(i)
    f.truncate()
    
#delete the old highest
with open("ipfs/index.html", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i.startswith("Highest Price Achieved:") != True:
            f.write(i)
    f.truncate()
    
progresseth = str(build_progress_bar(bar_curr_num, bar_total_num))

print('deleted old data..')

#get current date
now = datetime.now()

#get highest price
if response_json["ethereum"]["usd"] > float(highestever):
    highestever = response_json["ethereum"]["usd"]
       
#write the progress bar to the index.html
with open('ipfs/index.html', 'r+') as f: #r+ is rw
    lines = f.readlines()
    for i, line in enumerate(lines):
        if float(highestever) > 10000:
            lines[i] = lines[i].replace('ETH Price / $10,000 </h2><div><div><strong class ="content-bar">','ETH Price / $10,000 </h2><div><div><strong class ="content-bar">' + '\nVALHALLETH ACHIEVED. HAVE FUN STAYING RICH.'+ '\nProgress:</strong class ="content-bar">'+ progresseth +' <br><strong><br><br>' +'\nCurrent Price: </strong>$' + str(response_json["ethereum"]["usd"]) +' <br><strong>' + '\nLast Updated: </strong>' + str(now) +  '<br><strong>' + '\nHighest Price Achieved: </strong>$' + str(highestever).strip())
        elif line.startswith('ETH Price / $10,000'):
            lines[i] = lines[i].replace('ETH Price / $10,000 </h2><div><div><strong class ="content-bar">','ETH Price / $10,000 </h2><div><div><strong class ="content-bar">' + '\nProgress:</strong class ="content-bar">'+ progresseth +' <br><strong><br><br>' +'\nCurrent Price: </strong>$' + str(response_json["ethereum"]["usd"]) +' <br><strong>' + '\nLast Updated: </strong>' + str(now) +  '<br><strong>' + '\nHighest Price Achieved: </strong>$' + str(highestever).strip())
    f.seek(0)
    for line in lines:
        f.write(line)
print('writing new data..')

#publish website to ipfs
ipfshasher = 'ipfs add -r /home/pi/Desktop/Python/ipfs > ipfs_hashes.txt'
print('publishing pin to ipfs..')
os.system(ipfshasher)
time.sleep(60)

#save peer ID as trimmed variable
with open('ipfs_hashes.txt', 'r+') as f: #r+ is rw
    for line in f:
        pass
    last_line = line
last_line1 = last_line.replace('added ','')
last_line2 = last_line1.replace(' ipfs','')
     
#ipfs name publish
print('publishing to IPFN..')
ipfspub = 'ipfs name publish ' + str(last_line2)
os.system(ipfspub)

#show successful publish
print(ipfspub)

#pin to local node
ipfspin = 'ipfs pin add ' + str(last_line2)
os.system(ipfspin)

with open('ipfn_hashes.txt', 'a') as file_object:
    file_object.write(last_line2)
    
#show successful pin
print('pinning to local node..')
print(ipfspin)
time.sleep(60)

hash1 = str(last_line2)
hashs = hash1[:-1]

PINATA_API_URL = "https://api.pinata.cloud/pinning/pinByHash"
pinata_api_keys = ''
print(pinata_api_keys)

pinata_secret_api_keys = ''
myobj = {'hashToPin': hashs}
print(myobj)
headers = {'pinata_api_key': pinata_api_keys,'pinata_secret_api_key':pinata_secret_api_keys}

#lookup API and pin
print(headers)
response = requests.post(PINATA_API_URL,data = myobj, headers=headers)

#response_json = response.json()
print('pinning to pinata..')
print(response.text)
time.sleep(60)

#remove empty space from index file
with open('ipfs/index.html','r+') as file:
    for line in file:
        if line.isspace():
            file.write(line)

#Tweet 1/day
twitter_auth_keys = { 
        "consumer_key"        : "",
        "consumer_secret"     : "",
        "access_token"        : "",
        "access_token_secret" : ""}
auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
api = tweepy.API(auth)
 
tweet = 'Ethereum Price / $10,000' + '\nProgress:'+ progresseth  +'\nCurrent $ETH Price: $' + str(response_json["ethereum"]["usd"])
status = api.update_status(status=tweet) 
 
print(str(tweet))

print('script completed at..' + str(now))
with open('script_log.txt','r+') as file:
    for line in file:
            file.write('script completed at..' + str(now))
