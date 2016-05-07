#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
Created on Sep 6, 2015

RATE LIMIT

@author: ochi
'''

import urllib2
import urllib
import json
import inspect
import time

class LoLAPI:

    def __init__(self, apikey="***", region="na", version="v1.2"):
        self.apikey=apikey
        self.region=region
        self.version=version
        self.BASE_DOMAIN = "https://na.api.pvp.net/"
        self.BASE_URL = self.BASE_DOMAIN + "api/lol/"
        self.sleeptime = 1
        self.api_c = 0

    def getSummaryStatsBySummonerID(self, version="v1.3", region="na", summonerID="58675282"):
        apiURL = self.BASE_URL+region+'/'+version+ "/stats/by-summoner/"+summonerID+"/summary"+"?api_key="+self.apikey
        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code

    def getRankedStatsBySummonerID(self, version="v1.3", region="na", summonerID="58675282"):
        apiURL = self.BASE_URL+region+'/'+version+ "/stats/by-summoner/"+summonerID+"/ranked"+"?api_key="+self.apikey
        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code


    def getSummonerBySummonerName(self, version="v1.4", region="na", summonerName="koinodoino"):
        enc_name = summonerName.encode("utf-8")
        quoted_name = urllib.quote(enc_name)
        apiURL = self.BASE_URL+region+'/'+version+ "/summoner/by-name/"+quoted_name+"?api_key="+self.apikey
        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code

    def getFeaturedGames(self):
        # "clientRefreshInterval"
        # "gameList"
        #     +  "gameId"
        #     +  "participants"
        #            +  "summonerName"
        apiURL = self.BASE_DOMAIN+"observer-mode/rest/featured"+"?api_key="+self.apikey
        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code

    def getSummonerGames(self, version="v1.3", region="na", summonerID="58675282"):
        apiURL = self.BASE_URL+region+'/'+version+ "/game/by-summoner/"+summonerID+"/recent"+"?api_key="+self.apikey

        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code

    def getMatchStats(self, version="v2.2", region="na", matchID="1985399804"):
        apiURL = self.BASE_URL+region+'/'+version+ "/match/"+matchID+"?api_key="+self.apikey

        res, code, datadic = self.try_urlopen(apiURL)

#        data = res.read()
#        datadic = json.loads(data)
        return datadic, code

    def getWaitTime(self, res):
        waitsec = 0
        if res.code == 200:
            waitsec = self.sleeptime
        elif res.code == 429:
            infoDic = res.info()
#            print "infoDic"
#            print infoDic
#            data = res.read()
#            print "data"
#            print data
#            print "headers"
#            print res.headers
            if "retry-after" in infoDic.keys():
                waitsec = int(infoDic["retry-after"]) + 1
            else:
                waitsec = 10
                if self.api_c < 20:
                    waitsec = 600
                    print "blacklisted me? wait for %d sec."%(waitsec)
                elif self.api_c < 100:
                    waitsec = 300
                else:
                    waitsec = waitsec
                print "RATE LIMIT!! need to wait for %d secs."%(waitsec)

        elif res.code == 404:
            waitsec = self.sleeptime
            print "This could NOT be find. wait for %d sec."%(waitsec)
        else:
            waitsec = self.sleeptime
            print "unknown response code error: response code %d, message:"%(res.code)
            print res.message

        return waitsec

    def try_urlopen(self, apiURL):

        time.sleep(self.sleeptime)

        try:
            res = urllib2.urlopen(apiURL)
            code = 200
            self.api_c += 1
        except urllib2.URLError as e:
            print 'URLEroor!%s'%(str(apiURL))
            print '=== エラー内容 ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            print 'e自身:' + str(e)
            res = e
            waitsec = self.sleeptime
            code = 404
        except Exception as e:
            print '=== エラー内容 ==='
            print 'type:' + str(type(e))
            print 'args:' + str(e.args)
            print 'message:' + e.message
            print 'e自身:' + str(e)
#            print inspect.getmembers(e)

            waitsec = self.getWaitTime(e)
            code = e.code
            if waitsec > 0:
                print "sleep %d seconds."%(waitsec)
                time.sleep(waitsec)
                self.api_c = 0 # api_c をリフレッシュ
#                res = self.try_urlopen(apiURL)
                if e.code != 404:
                    res = e
                    code = e.code
                    print "%d: Failed Retry! Continue to Next Game."%(e.code)
#                    res = urllib2.urlopen(apiURL)
#                    code = res.code
#                    self.api_c += 1
#                    if res.code != 200:
#                        print res
#                        print "404: Failed Retry! Continue to Next Game."
                else:
                    print "%d: Failed Retry! Continue to Next Game."%(e.code)
                    res = e
                    code = e.code
        if code == 200:
            data = res.read()
            datadic = json.loads(data)
        else:
            datadic = {}
        return res, code, datadic

if __name__ == "__main__":
    lolapi = LoLAPI()
    summonerName="koinodoino"
#    summonerName="laivo"
    summonerdic = lolapi.getSummonerBySummonerName(summonerName=summonerName)
    summonerid = str(summonerdic[summonerName]["id"])
    print summonerdic
#    summarydic = lolapi.getSummaryStatsBySummonerID(summonerID=summonerid)
#    print summarydic
#    print type(summarydic)

#    statsdic = lolapi.getSummonerGames(summonerID=summonerid)
#    print statsdic
#    print type(statsdic)
#    print json.dumps(statsdic,indent=4,sort_keys=True)

#    datadic = lolapi.getFeaturedGames()
#    print datadic.keys()
#    print json.dumps(datadic,indent=4,sort_keys=True)
#    print ""

#    datadic = lolapi.getSummonerGames()
#    print datadic


