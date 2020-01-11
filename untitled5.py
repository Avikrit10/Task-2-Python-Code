# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 02:54:35 2019

@author: avikr
"""
import time
import re
import urllib.request
start_time=time.time()
request_url = urllib.request.urlopen('https://www.atg.world/view-article/How%20to%20Edit%20or%20Change%20your%20PlayStation%20Network%20NameOnline%20ID-30528') 
print("--- %s seconds ---" % (time.time() - start_time))
data=request_url.read()
data=data.decode("UTF-8") 
Post=re.search("How to Edit or.{47}",data).group()
print("Post is",Post)
print("HTTP Code is",request_url.code)
if request_url.code==200:
    print("Working")
