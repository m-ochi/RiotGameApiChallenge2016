#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on Oct 20, 2015

クロールの流れ
１．FeaturedGamesで最近のゲームを取得
２．ParticipantsのSummonerNamesを取得
３．SummonerNamesを使ってSummonerIdを取得
４．SummonerIdを使ってSummonerGamesを取得
５．SummonerGamesからMatchStatsを取得
６．保存

@author: ochi
'''

import urllib2
import urllib
import json
import lolapi 
import os
import sys
import shutil
import datetime as dt

class LoLCrawler:

    def __init__(self):
        place = os.path.abspath(os.path.dirname(__file__))
        today = dt.datetime.today()
        todaystr = today.strftime("%Y%m%d%H")
        self.resultDir = place + "/results%s"%(todaystr)
        pass

    def run(self):
        if os.path.exists(self.resultDir):
            pass
        else:
            os.mkdir(self.resultDir)
        os.chdir(self.resultDir)
        
        api = lolapi.LoLAPI()

        loop_continue = True
        while loop_continue is True:
            featuredGamesDic, code = api.getFeaturedGames()
            if code == 200:
                print "retry getFeatureGames"
                loop_continue = False

        games = featuredGamesDic["gameList"]
        for gameDic in games:
            gameID = str(gameDic["gameId"])

        for gameDic in games:
            featured_gameID = str(gameDic["gameId"])

            participants = gameDic["participants"]
            summonerNames = self.getSummonerNames(participants)
            for summonerName in summonerNames:
                summonerDic, code = api.getSummonerBySummonerName(summonerName=summonerName)
                if code != 200:
                    print "cannot find summonerName: %s"%(summonerName)
                    continue

                key_summonerName = summonerDic.keys()[0]
                summonerid = str(summonerDic[key_summonerName]["id"])

                statsDic, code = api.getSummonerGames(summonerID=summonerid)
                if code != 200:
                    print "cannot find summonerGames summonerID: %s"%(summonerid)
                    continue
                game_ids = self.getPlayerStatsGameIDs(statsDic)

                for gameID in game_ids:
                    print "now consumed api_c: %d"%(api.api_c)
                    fileName = "gameID%s.json"%(gameID)
                    print "Start Get gameID:%s"%(gameID)
                    outDic, code = api.getMatchStats(matchID=gameID)
                    if code != 200:
                        print "cannot find Matchstats GameID: %s"%(gameID)
                        continue

                    # output for each game
                    if os.path.exists(fileName):
                        print "find same game file! gameID: %s"%(gameID)
                        os.remove(fileName)
                    else:
                        f = open(fileName, 'w')
                        line = json.dumps(outDic,indent=4,sort_keys=True)
                        f.write(line)
                        f.close()

        print "finish write featured games stats"
        print "consume api_c: %d"%(api.api_c)

        pass

    def getPlayerStatsGameIDs(self, statsDic):
        games = statsDic["games"]
  
        game_ids = []
        for a_gameDic in games:
            game_id = str(a_gameDic["gameId"])
            game_ids.append(game_id)
        return game_ids

    def getSummonerNames(self, participants):
        summonerNames = []
        for eachSummonerDic in participants:
            summonerName = eachSummonerDic["summonerName"]
            summonerNames.append(summonerName)
        return summonerNames


if __name__ == "__main__":
    obj = LoLCrawler()
    obj.run()


