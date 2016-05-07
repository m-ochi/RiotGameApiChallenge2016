#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 29, 2015

MongoDBのデータを軽く分析する例

@author: ochi
'''

import json
#import os
#import sys
#import shutil
#import datetime as dt
import pymongo
import pickle


mongoDBUser = "tang"
mongoDBUserPassword = "ud0nud0n"
mongoDBCollection = "game_results"

championIdNameDic = json.load(open("championIdName.json",'r'))
champIDs = championIdNameDic.keys()

con = pymongo.MongoClient(host="localhost",port=27017)
dbadmin = con["admin"]
dbadmin.authenticate(mongoDBUser,mongoDBUserPassword)
db =  con["lol"]

col = db[mongoDBCollection]
cursor = col.aggregate([{"$match":{"mapId":11,"queueType":"NORMAL_5x5_BLIND"}},{"$project":{"_id":0, "participants":"$participants"}},{"$unwind":"$participants"},{"$project":{"_id":0,"champ":"$participants.championId","kills":"$participants.stats.kills","assists":"$participants.stats.assists","deaths":"$participants.stats.deaths"}},{"$group":{"_id":"$champ","count":{"$sum":1},"kills":{"$sum":"$kills"},"assists":{"$sum":"$assists"},"deaths":{"$sum":"$deaths"}}}])

c_idCountDic = {}
c_idKillsDic = {}
c_idAssistsDic = {}
c_idDeathsDic = {}
c_idKDrateDic = {}
for row in cursor:
    c_idCountDic[row["_id"]]   = row["count"]
    c_idKillsDic[row["_id"]]   = row["kills"]/float(row["count"])
    c_idAssistsDic[row["_id"]] = row["assists"]/float(row["count"])
    c_idDeathsDic[row["_id"]]  = row["deaths"]/float(row["count"])
    c_idKDrateDic[row["_id"]]  = c_idKillsDic[row["_id"]]/c_idDeathsDic[row["_id"]]

def output(c_idNameDic,c_idCountDic,title='',ranking=10):
    print "Most:%s"%(title)
    i = 0
    print "{0:4s},{1:<15s},{2:10s}".format("順位","チャンピオン名","Count")
    for k,v in sorted(c_idCountDic.items(), key=lambda x:-x[1]):
        i += 1
        if i <= ranking:
            r = unicode(k)
            print "{0:>4d},{1:<15s},{2:.3f}".format(i,c_idNameDic[r],c_idCountDic[k])
        else:
            break

    print ""
    print "Least:%s"%(title)
    i = 0
    print "{0:4s},{1:<15s},{2:10s}".format("順位","チャンピオン名","Count")
    for k,v in sorted(c_idCountDic.items(), key=lambda x:x[1]):
        i += 1
        if i <= ranking:
            r = unicode(k)
            print "{0:>2d},{1:<15s},{2:.3f}".format(i,c_idNameDic[r],c_idCountDic[k])
        else:
            break
    print ""
    print ""
    print ""
    print ""
    return 

output(championIdNameDic,c_idCountDic,title="使用頻度")
output(championIdNameDic,c_idKillsDic,title="Average Kills")
output(championIdNameDic,c_idAssistsDic,title="Average Assists")
output(championIdNameDic,c_idDeathsDic,title="Average Deaths")
output(championIdNameDic,c_idKDrateDic,title="Kill-Death Rate")

con.close()

