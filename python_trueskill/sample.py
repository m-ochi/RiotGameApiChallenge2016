# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 18:40:56 2016

@author: nishinolab
"""

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
#import os
#import sys
#import shutil
#import datetime as dt
import pymongo
import pandas as pd
from sklearn.cluster import KMeans
from trueskill import Rating,rate_1vs1

mongoDBCollection = "lol"
con = pymongo.MongoClient(host="localhost",port=27017)
db =  con["yusuke"]

col = db[mongoDBCollection]
cursor = col.find()
all = pd.DataFrame({'matchID' : 0,
                'teamID' :0,
                'winorlose' : 0,
                '0_lane' : 0,
                '0_role' : 0,
                '0_champion_attr' : 0,
                '1_lane' : 0,
                '1_role' : 0,
                '1_champion_attr' : 0,
                '2_lane' : 0,
                '2_role' : 0,
                '2_champion_attr' : 0,
                '3_lane' : 0,
                '3_role' : 0,
                '3_champion_attr' : 0,
                '4_lane' : 0,
                '4_role' : 0,
                '4_champion_attr' : 0},
                index=[1])

# championdata-create
f = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=tags&api_key=ed4ee1b9-d78a-4eb6-a42b-2f3977ae9536")
ff = f.json()
k = list(ff["data"].keys())
idtag = {"noid":"notag"}
for i in range(0,len(k)):
    idtag.update({ff["data"][k[i]]["id"]:ff["data"][k[i]]["tags"][0]})

var = cursor.count()
for i in range(1,10000):
    if(cursor[i]["season"]=="SEASON2015"):
       if(len(cursor[i]["participants"])==10): 
           c = [""] * 10
           for k in range(0,10):
               c[k] = idtag[cursor[i]["participants"][k]["championId"]]
        
           temp1 = pd.DataFrame({ 'matchID' : i,
           'teamID' :cursor[i]["teams"][0]["teamId"],
            'winorlose' : cursor[i]["teams"][0]["winner"],
            '0_lane' : cursor[i]["participants"][0]["timeline"]["lane"],
            '0_role' : cursor[i]["participants"][0]["timeline"]["role"],
            '0_champion_attr' : c[0],
            '1_lane' : cursor[i]["participants"][1]["timeline"]["lane"],
            '1_role' : cursor[i]["participants"][1]["timeline"]["role"],
            '1_champion_attr' : c[1],
            '2_lane' : cursor[i]["participants"][2]["timeline"]["lane"],
            '2_role' : cursor[i]["participants"][2]["timeline"]["role"],
            '2_champion_attr' : c[2],
            '3_lane' : cursor[i]["participants"][3]["timeline"]["lane"],
            '3_role' : cursor[i]["participants"][3]["timeline"]["role"],
            '3_champion_attr' : c[3],              
            '4_lane' : cursor[i]["participants"][4]["timeline"]["lane"],
            '4_role' : cursor[i]["participants"][4]["timeline"]["role"],
            '4_champion_attr' : c[4]},
            index=[1])
           temp2 = pd.DataFrame({ 'matchID' : i,
                'teamID' :cursor[i]["teams"][1]["teamId"],
                'winorlose' : cursor[i]["teams"][1]["winner"],
                '0_lane' : cursor[i]["participants"][5]["timeline"]["lane"],
                '0_role' : cursor[i]["participants"][5]["timeline"]["role"],
                '0_champion_attr' : c[5],
                '1_lane' : cursor[i]["participants"][6]["timeline"]["lane"],
                '1_role' : cursor[i]["participants"][6]["timeline"]["role"],
                '1_champion_attr' : c[6],
                '2_lane' : cursor[i]["participants"][7]["timeline"]["lane"],
                '2_role' : cursor[i]["participants"][7]["timeline"]["role"],
                '2_champion_attr' : c[7],
                '3_lane' : cursor[i]["participants"][8]["timeline"]["lane"],
                '3_role' : cursor[i]["participants"][8]["timeline"]["role"],
                '3_champion_attr' : c[8],
                '4_lane' : cursor[i]["participants"][9]["timeline"]["lane"],
                '4_role' : cursor[i]["participants"][9]["timeline"]["role"],
                '4_champion_attr' : c[9]},
                index=[1]);
           all = pd.concat([all,temp1,temp2]);
            
all = all.reset_index()
all = all.drop("index",axis=1)
all = all.drop("Index" == 0)
all = all.reset_index()
all = all.drop("index",axis=1)

# Convert
all["0_role"] = all["0_role"].map({"SOLO":0,"DUO_SUPPORT":1,"DUO_CARRY":2,"DUO":3,"NONE":4})
all["1_role"] = all["1_role"].map({"SOLO":0,"DUO_SUPPORT":1,"DUO_CARRY":2,"DUO":3,"NONE":4})
all["2_role"] = all["2_role"].map({"SOLO":0,"DUO_SUPPORT":1,"DUO_CARRY":2,"DUO":3,"NONE":4})
all["3_role"] = all["3_role"].map({"SOLO":0,"DUO_SUPPORT":1,"DUO_CARRY":2,"DUO":3,"NONE":4})
all["4_role"] = all["4_role"].map({"SOLO":0,"DUO_SUPPORT":1,"DUO_CARRY":2,"DUO":3,"NONE":4})

all["0_lane"] = all["0_lane"].map({"TOP":0,"MIDDLE":1,"BOTTOM":2,"JUNGLE":3})
all["1_lane"] = all["1_lane"].map({"TOP":0,"MIDDLE":1,"BOTTOM":2,"JUNGLE":3})
all["2_lane"] = all["2_lane"].map({"TOP":0,"MIDDLE":1,"BOTTOM":2,"JUNGLE":3})
all["3_lane"] = all["3_lane"].map({"TOP":0,"MIDDLE":1,"BOTTOM":2,"JUNGLE":3})
all["4_lane"] = all["4_lane"].map({"TOP":0,"MIDDLE":1,"BOTTOM":2,"JUNGLE":3})

all["0_champion_attr"] = all["0_champion_attr"].map({"Assassin":0,"Fighter":1,"Mage":2,"Marksman":3,"Support":4,"Tank":5})
all["1_champion_attr"] = all["1_champion_attr"].map({"Assassin":0,"Fighter":1,"Mage":2,"Marksman":3,"Support":4,"Tank":5})
all["2_champion_attr"] = all["2_champion_attr"].map({"Assassin":0,"Fighter":1,"Mage":2,"Marksman":3,"Support":4,"Tank":5})
all["3_champion_attr"] = all["3_champion_attr"].map({"Assassin":0,"Fighter":1,"Mage":2,"Marksman":3,"Support":4,"Tank":5})
all["4_champion_attr"] = all["4_champion_attr"].map({"Assassin":0,"Fighter":1,"Mage":2,"Marksman":3,"Support":4,"Tank":5})

# K-Means
cl = 30
result = KMeans(n_clusters=cl).fit_predict(all.iloc[:,0:14])
all["cluster"] = 0
for i in range(0,len(result)):
    all["cluster"][i] = result[i]

# Trueskill-Setting
clusters = [""] * cl
print("Before Ability") 
for i in range(0,cl):
    clusters[i] = Rating()   
    print(clusters[i])

# Trueskill-Updating
for i in range(0,int(len(all)/2)):
    if(all["winorlose"][2*i+1]==True):
        clusters[all["cluster"][2*i+1]],clusters[all["cluster"][2*i]] = rate_1vs1(clusters[all["cluster"][2*i+1]],clusters[all["cluster"][2*i]])
    elif(all["winorlose"][2*i+1]==False):
        clusters[all["cluster"][2*i]],clusters[all["cluster"][2*i+1]] = rate_1vs1(clusters[all["cluster"][2*i]],clusters[all["cluster"][2*i+1]])

print("After Ability")
for i in range(0,cl):
    print(clusters[i])



con.close()
