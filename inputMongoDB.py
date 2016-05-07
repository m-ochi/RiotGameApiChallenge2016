#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 26, 2015

MongoDBに各フォルダのデータを保存する

@author: ochi
'''

import json
import os
import sys
import shutil
import datetime as dt
import pymongo
import pickle

class InputDB:

    def __init__(self):
        place = os.path.abspath(os.path.dirname(__file__))
        self.mongoDBUser = "ochi"
        self.mongoDBUserPassword = "ud0nud0n"
        self.mongoDBCollection = "game_results"
        self.dirHeader = place + '/' + "results"
        self.getGameIDsFile = place + '/' + "registerGames.pickle"
        self.start_date = dt.datetime.strptime("20151022", "%Y%m%d")
        self.end_date   = dt.datetime.strptime("20151031", "%Y%m%d")
        term = self.end_date - self.start_date
        days = term.days
        self.terms = []
        for i in range(days+1):
            the_date = self.start_date + dt.timedelta(days=i)
            the_date_str = the_date.strftime("%Y%m%d")
            self.terms.append(the_date_str)

        #runADay 用
        self.yesterday = dt.datetime.today() - dt.timedelta(days=1)
        self.yesterday_str = self.yesterday.strftime("%Y%m%d")

    def runADay(self,the_date_str):
        registeredGames = self.getRegisteredGames()
        gameIDDataDic = {}
        for i in range(0,24,1):
            the_datehour_str = "%s%02d"%(the_date_str,i)
            dirName = self.dirHeader+the_datehour_str
            if os.path.exists(dirName):
                print "Process %s"%(dirName)
                os.chdir(dirName)
                new_gameIDDataDic = self.makeGameIDDataDic()
                os.chdir("../")
                gameIDDataDic.update(new_gameIDDataDic)
            else:
                print "%s doesnt Exist."%(dirName)
                continue

        gameIDs = set(gameIDDataDic.keys())
        new_gameIDs = gameIDs - registeredGames
        new_registeredGames = self.registerData(new_gameIDs, gameIDDataDic)

        registeredGames |= set(new_registeredGames)
        self.saveRegisteredGames(registeredGames)
        print "complete! registered %s Date."%(the_date_str)
        print "new registered dataCount is %d"%(len(new_registeredGames))
        return

    def registerData(self,new_gameIDs, gameIDDataDic):
        new_registeredGames = []
        con = pymongo.MongoClient(host="localhost",port=27017)
        dbadmin = con["admin"]
        dbadmin.authenticate(self.mongoDBUser,self.mongoDBUserPassword)
        db =  con["lol"]
#        print db.collection_names()
        col = db[self.mongoDBCollection]
        for new_gameID in new_gameIDs:
            datadic = gameIDDataDic[new_gameID]
#            print datadic[datadic.keys()[0]]
            col.insert_one(datadic)
            new_registeredGames.append(new_gameID)
        con.close()
        return new_registeredGames

    def runAll(self):
        self.cleanDBCollection()
        os.remove(self.getGameIDsFile)
        print "removed %s file"%(self.getGameIDsFile)
        for term in self.terms:
            print "input start %s"%(term)
            self.runADay(term)
        return

    def cleanDBCollection(self):
        con = pymongo.MongoClient(host="localhost",port=27017)
        dbadmin = con["admin"]
        dbadmin.authenticate(self.mongoDBUser,self.mongoDBUserPassword)
        db =  con["lol"]
        db.drop_collection(self.mongoDBCollection)
        db.create_collection(self.mongoDBCollection)
        con.close()
        print "drop %s collection from DB."%(self.mongoDBCollection)
        return

    def makeGameIDDataDic(self):
        gameIDDataDic = {}
        files = os.listdir("./")
        for a_file in files:
            try:
                datadic = self.getJsonData(a_file)
            except Exception as e:
                print "Difficult to parse the file %s"%(a_file)
                print '=== エラー内容 ==='
                print 'type:' + str(type(e))
                print 'args:' + str(e.args)
                print 'message:' + e.message
                print 'e自身:' + str(e)
                continue
            gameIDDataDic[a_file] = datadic
        return gameIDDataDic

    def getJsonData(self,a_file):
        f = open(a_file,'r')
        datadic = json.load(f)
        f.close()
        return datadic

    def getRegisteredGames(self):
        if os.path.exists(self.getGameIDsFile):
            f = open(self.getGameIDsFile, 'r')
            try:
               registeredGames = pickle.load(f)
            except Exception as e:
                print '=== エラー内容 ==='
                print 'type:' + str(type(e))
                print 'args:' + str(e.args)
                print 'message:' + e.message
                print 'e自身:' + str(e)
                registeredGames = set([])
            f.close()
        else:
            print "the File: %s is NOT exist."%(self.getGameIDsFile)
            registeredGames = set([])
        return registeredGames

    def saveRegisteredGames(self, registeredGames):
        f = open(self.getGameIDsFile, 'w')
        pickle.dump(registeredGames,f)
        f.close()
        return


if __name__ == "__main__":
    obj = InputDB()
    # 全データ用
#    obj.runAll()
    # 一日用
    print "start %s DB register"%(obj.yesterday_str)
    obj.runADay(obj.yesterday_str)
    print "complete!"


