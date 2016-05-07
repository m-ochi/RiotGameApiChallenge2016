lolclusteringchampionid<-function(season,clusterk){
  require(RMongo)
  require(rlist)
  require(rjson)
  library(magrittr)
  library(formattable)
  require(pipeR)
  clusterk<-as.integer(clusterk)
  db <- mongoDbConnect("gamedata")
  seasonkeyword<-paste('{"season":',season,'}',sep="")
  output <- dbGetQuery(db, 'logdata', seasonkeyword,0,1000)
  all<-c()
  for(k in 1:nrow(output)){
    repos <- output$participants[k] %>%
      list.load(type = "json") %>%
      list.ungroup()
    matchno<-k
    if(length(repos) == 100){
      for(i in 0:9){
        tt<-c()
        mastery<-c()
        runes<-c()
        stats<-c()
        timeline<-c()
        # エトセトラから
        tt<-cbind(repos[1+i*10],repos[2+i*10],repos[4+i*10],repos[6+i*10],repos[7+i*10],repos[9+i*10])
        tt<-data.frame(tt)
        names(tt)<-c(list.names(repos[1]),list.names(repos[2]),list.names(repos[4]),list.names(repos[6]),list.names(repos[7]),list.names(repos[9]))
        names(tt)<-paste(i,"_",names(tt),sep="")
        # masteryの処理
        mastery<-repos[3+i*10]
        mastery<-data.frame(mastery)
        names(mastery)<-paste(i,"_",names(mastery),sep="")
        # runesの処理
        runes<-repos[5+i*10]
        runes<-data.frame(runes)
        names(runes)<-paste(i,"_",names(runes),sep="")
        # statsの処理
        stats<-repos[8+i*10]
        stats<-data.frame(stats)
        names(stats)<-paste(i,"_",names(stats),sep="")
        # timelineの処理
        timeline<-repos[10+i*10]
        timeline<-data.frame(timeline)
        names(timeline)<-paste(i,"_",names(timeline),sep="")
        # 全てをくっつける
        tt<-cbind(tt,mastery,runes,stats,timeline)
        matchno<-cbind(matchno,tt)
      }
      all<-merge(matchno,all,all = TRUE)
    }
  }
  
  # なぜかlength100の1ばんが無視されてしまうので、追加しとく
  for(k in 1){
    repos <- output$participants[k] %>%
      list.load(type = "json") %>%
      list.ungroup()
    matchno<-k
    if(length(repos) == 100){
      for(i in 0:9){
        tt<-c()
        mastery<-c()
        runes<-c()
        stats<-c()
        timeline<-c()
        # エトセトラから
        tt<-cbind(repos[1+i*10],repos[2+i*10],repos[4+i*10],repos[6+i*10],repos[7+i*10],repos[9+i*10])
        tt<-data.frame(tt)
        names(tt)<-c(list.names(repos[1]),list.names(repos[2]),list.names(repos[4]),list.names(repos[6]),list.names(repos[7]),list.names(repos[9]))
        names(tt)<-paste(i,"_",names(tt),sep="")
        # masteryの処理
        mastery<-repos[3+i*10]
        mastery<-data.frame(mastery)
        names(mastery)<-paste(i,"_",names(mastery),sep="")
        # runesの処理
        runes<-repos[5+i*10]
        runes<-data.frame(runes)
        names(runes)<-paste(i,"_",names(runes),sep="")
        # statsの処理
        stats<-repos[8+i*10]
        stats<-data.frame(stats)
        names(stats)<-paste(i,"_",names(stats),sep="")
        # timelineの処理
        timeline<-repos[10+i*10]
        timeline<-data.frame(timeline)
        names(timeline)<-paste(i,"_",names(timeline),sep="")
        # 全てをくっつける
        tt<-cbind(tt,stats,timeline)
        matchno<-cbind(matchno,tt)
      }
      all<-merge(matchno,all,all = TRUE)
    }
  }
  require(stringr)
  for(i in 1:ncol(all)){
    all[,i]<-unlist(all[,i])
    if(class(all[,i])=="factor"){
      all[,i]<-as.character(all[,i])
    }
  }
  for(i in 1:ncol(all)){
    if(class(all[,i])=="character"){
      if(str_detect(names(all)[i],"highestAchievedSeasonTier")){
        all[,i]<-str_replace(all[,i], "UNRANKED", 0)
        all[,i]<-str_replace(all[,i], "BRONZE", 1)
        all[,i]<-str_replace(all[,i], "SILVER", 2)
        all[,i]<-str_replace(all[,i], "GOLD", 3)
        all[,i]<-str_replace(all[,i], "PLATINUM", 4)
        all[,i]<-str_replace(all[,i], "DIAMOND", 5)
        all[,i]<-str_replace(all[,i], "MASTER", 6)
        all[,i]<-str_replace(all[,i], "CHALLENGER", 7)
        all[,i]<-as.numeric(all[,i])
      }else if(str_detect(names(all)[i],"timeline.lane")){
        all[,i]<-str_replace(all[,i], "TOP", 0)
        all[,i]<-str_replace(all[,i], "BOTTOM", 1)
        all[,i]<-str_replace(all[,i], "MIDDLE", 2)
        all[,i]<-str_replace(all[,i], "JUNGLE", 3)
        all[,i]<-as.numeric(all[,i])
      }else if(str_detect(names(all)[i],"timeline.role")){
        all[,i]<-str_replace(all[,i], "SOLO", 0)
        all[,i]<-str_replace(all[,i], "DUO_CARRY", 1)
        all[,i]<-str_replace(all[,i], "NONE", 2)
        all[,i]<-str_replace(all[,i], "DUO_SUPPORT", 4)
        all[,i]<-str_replace(all[,i], "DUO", 3)
        all[,i]<-as.numeric(all[,i])
      }
    }
  }
  for(i in 1:ncol(all)){
    if(class(all[,i])=="logical"){
      all[,i]<-str_replace(all[,i], "TRUE", 1)
      all[,i]<-str_replace(all[,i], "FALSE", 0)
      all[,i]<-as.numeric(all[,i])
    }
  }
  # naを0にする
  all[is.na(all)]<-0
  require(cluster)
  temp<-c()
  teamco<-c()
  for(i in 1:ncol(all)){
    if(str_detect(names(all)[i],"0_stats.winner")){
      temp<-all[,i]
    }
    if(str_detect(names(all)[i],"9_stats.winner")){
      temp2<-all[,i]
    }
    if(str_detect(names(all)[i],"championId")){
      teamco<-cbind(teamco,all[,i])
    }
  }
  teamco<-data.frame(teamco)
  teamco1<-teamco[,c(1,2,3,4,5)]
  teamco2<-teamco[,c(6,7,8,9,10)]
  names(teamco1)<-c("1","2","3","4","5")
  names(teamco2)<-c("1","2","3","4","5")
  teamco2$winner<-temp2
  teamco2$matchno<-1:nrow(all)
  teamco1$winner<-temp
  teamco1$matchno<-1:nrow(all)
  teamco1<-rbind(teamco1,teamco2)
  # k-meansの最適解を見つける
  result <- clusGap(teamco1[,c(-6,-7)], kmeans, K.max = clusterk, B = 100, verbose = interactive())
  plot(result)
  # 一番Gap統計量が大きいクラスター数でやる
  unr<-unlist(result$Tab)
  unr<-data.frame(unr)
  unr$cluster<-row.names(unr)
  numcluster<-as.numeric(subset(unr,select="cluster",gap==max(gap)))
  res<-kmeans(teamco1[,c(-6,-7)],numcluster)
  teamco1$cluster<-res$cluster
  teamcluster<-seq(1:numcluster)
  teamcluster<-data.frame(teamcluster)
  for(i in 1:numcluster){
    teamcluster$total[i]<-nrow(subset(teamco1,teamco1$cluster==i))
    teamcluster$wins[i]<-nrow(subset(teamco1,teamco1$winner==1&teamco1$cluster==i))
  } 
  teamcluster$rate<-teamcluster$wins/teamcluster$total
  winorlose<-seq(1:nrow(all))
  winorlose<-data.frame(winorlose)
  for(i in 1:nrow(all)){
    winorlose$winner[i]<-subset(teamco1,teamco1$matchno==i & teamco1$winner==1,select="cluster")
    winorlose$loser[i]<-subset(teamco1,teamco1$matchno==i & teamco1$winner==0,select="cluster")
  }
  names(winorlose)<-c("matchno","winner","loser")
  require(trueskill)
  #時系列でやるならこことtの値が変わる
  winorlose$margin <- 1
  winorlose$Round<-as.factor(season)
  winorlose$mu1 <- NA
  winorlose$sigma1 <- NA
  winorlose$mu2 <- NA
  winorlose$sigma2 <- NA
  
  # 強さをrateで推定する。100倍する。
  for(i in 1:nrow(all)){
    winorlose$rate1[i]<-subset(teamcluster,select="rate",teamcluster==winorlose$winner[i])
    winorlose$rate2[i]<-subset(teamcluster,select="rate",teamcluster==winorlose$loser[i])
    winorlose$rate1[i]<-as.numeric(winorlose$rate1[i])*100
    winorlose$rate2[i]<-as.numeric(winorlose$rate2[i])*100
  }
  # 100を基準に初期平均値を決めて初期分散を決定する。
  winorlose[c("mu1","sigma1")] <- c(100 - as.numeric(winorlose$rate1), round(100 - as.numeric(winorlose$rate1) - ((100 - as.numeric(winorlose$rate1)) / 3), 1))
  winorlose[c("mu2","sigma2")] <- c(100 - as.numeric(winorlose$rate2), round(100 - as.numeric(winorlose$rate2) - ((100 - as.numeric(winorlose$rate2)) / 3), 1))
  
  parameters <- Parameters()
  # trueskillmodelで平均値・分散を更新する
  winorlose <- Trueskill(winorlose, parameters)
  teamcluster$rating<-as.numeric(teamcluster$rate)*100
  for(i in 1:nrow(teamcluster)){
    mu<-subset(winorlose,select="mu1",winner==i)
    sigma<-subset(winorlose,select="sigma1",winner==i)
    teamcluster$mu[i]<-mu[1,1]
    teamcluster$sigma[i]<-sigma[1,1]
  }
  
  #バイオリンプロットをするために平均と分散からサンプリングする
  allsample<-c()
  for(i in 1:nrow(teamcluster)){
    sample<-rnorm(100,as.numeric(teamcluster$mu[i]),as.numeric(teamcluster$sigma[i])^(1/2))
    sample<-data.frame(sample)
    sample$cluster<-i
    allsample<-rbind(allsample,sample)
  }
  # データフレームをここで何故か返す
  return(winorlose)
  return(teamco1)
  return(all)
  
  p<-
    ggplot(allsample,aes(x=as.factor(cluster),y=sample,colour=as.factor(cluster))) 
  p+
    geom_violin(trim=T,fill="#999999",linetype="blank",alpha=I(1/3))+
    theme(legend.position="none")+
    stat_summary(geom="pointrange",fun.y = mean, fun.ymin = function(x) mean(x)-sd(x), fun.ymax = function(x) mean(x)+sd(x), size=1,alpha=.5)
}

#冒頭を省くミニバージョン
lolclusteringchampionidmini<-function(season,clusterk){
  require(RMongo)
  require(rlist)
  require(rjson)
  library(magrittr)
  library(formattable)
  require(pipeR)
  clusterk<-as.integer(clusterk)
  all<-c()
  for(k in 1:nrow(output)){
    repos <- output$participants[k] %>%
      list.load(type = "json") %>%
      list.ungroup()
    matchno<-k
    if(length(repos) == 100){
      for(i in 0:9){
        tt<-c()
        mastery<-c()
        runes<-c()
        stats<-c()
        timeline<-c()
        # エトセトラから
        tt<-cbind(repos[1+i*10],repos[2+i*10],repos[4+i*10],repos[6+i*10],repos[7+i*10],repos[9+i*10])
        tt<-data.frame(tt)
        names(tt)<-c(list.names(repos[1]),list.names(repos[2]),list.names(repos[4]),list.names(repos[6]),list.names(repos[7]),list.names(repos[9]))
        names(tt)<-paste(i,"_",names(tt),sep="")
        # masteryの処理
        mastery<-repos[3+i*10]
        mastery<-data.frame(mastery)
        names(mastery)<-paste(i,"_",names(mastery),sep="")
        # runesの処理
        runes<-repos[5+i*10]
        runes<-data.frame(runes)
        names(runes)<-paste(i,"_",names(runes),sep="")
        # statsの処理
        stats<-repos[8+i*10]
        stats<-data.frame(stats)
        names(stats)<-paste(i,"_",names(stats),sep="")
        # timelineの処理
        timeline<-repos[10+i*10]
        timeline<-data.frame(timeline)
        names(timeline)<-paste(i,"_",names(timeline),sep="")
        # 全てをくっつける
        tt<-cbind(tt,mastery,runes,stats,timeline)
        matchno<-cbind(matchno,tt)
      }
      all<-merge(matchno,all,all = TRUE)
    }
  }
  
  # なぜかlength100の1ばんが無視されてしまうので、追加しとく
  for(k in 1){
    repos <- output$participants[k] %>%
      list.load(type = "json") %>%
      list.ungroup()
    matchno<-k
    if(length(repos) == 100){
      for(i in 0:9){
        tt<-c()
        mastery<-c()
        runes<-c()
        stats<-c()
        timeline<-c()
        # エトセトラから
        tt<-cbind(repos[1+i*10],repos[2+i*10],repos[4+i*10],repos[6+i*10],repos[7+i*10],repos[9+i*10])
        tt<-data.frame(tt)
        names(tt)<-c(list.names(repos[1]),list.names(repos[2]),list.names(repos[4]),list.names(repos[6]),list.names(repos[7]),list.names(repos[9]))
        names(tt)<-paste(i,"_",names(tt),sep="")
        # masteryの処理
        mastery<-repos[3+i*10]
        mastery<-data.frame(mastery)
        names(mastery)<-paste(i,"_",names(mastery),sep="")
        # runesの処理
        runes<-repos[5+i*10]
        runes<-data.frame(runes)
        names(runes)<-paste(i,"_",names(runes),sep="")
        # statsの処理
        stats<-repos[8+i*10]
        stats<-data.frame(stats)
        names(stats)<-paste(i,"_",names(stats),sep="")
        # timelineの処理
        timeline<-repos[10+i*10]
        timeline<-data.frame(timeline)
        names(timeline)<-paste(i,"_",names(timeline),sep="")
        # 全てをくっつける
        tt<-cbind(tt,stats,timeline)
        matchno<-cbind(matchno,tt)
      }
      all<-merge(matchno,all,all = TRUE)
    }
  }
  require(stringr)
  for(i in 1:ncol(all)){
    all[,i]<-unlist(all[,i])
    if(class(all[,i])=="factor"){
      all[,i]<-as.character(all[,i])
    }
  }
  for(i in 1:ncol(all)){
    if(class(all[,i])=="character"){
      if(str_detect(names(all)[i],"highestAchievedSeasonTier")){
        all[,i]<-str_replace(all[,i], "UNRANKED", 0)
        all[,i]<-str_replace(all[,i], "BRONZE", 1)
        all[,i]<-str_replace(all[,i], "SILVER", 2)
        all[,i]<-str_replace(all[,i], "GOLD", 3)
        all[,i]<-str_replace(all[,i], "PLATINUM", 4)
        all[,i]<-str_replace(all[,i], "DIAMOND", 5)
        all[,i]<-str_replace(all[,i], "MASTER", 6)
        all[,i]<-str_replace(all[,i], "CHALLENGER", 7)
        all[,i]<-as.numeric(all[,i])
      }else if(str_detect(names(all)[i],"timeline.lane")){
        all[,i]<-str_replace(all[,i], "TOP", 0)
        all[,i]<-str_replace(all[,i], "BOTTOM", 1)
        all[,i]<-str_replace(all[,i], "MIDDLE", 2)
        all[,i]<-str_replace(all[,i], "JUNGLE", 3)
        all[,i]<-as.numeric(all[,i])
      }else if(str_detect(names(all)[i],"timeline.role")){
        all[,i]<-str_replace(all[,i], "SOLO", 0)
        all[,i]<-str_replace(all[,i], "DUO_CARRY", 1)
        all[,i]<-str_replace(all[,i], "NONE", 2)
        all[,i]<-str_replace(all[,i], "DUO_SUPPORT", 4)
        all[,i]<-str_replace(all[,i], "DUO", 3)
        all[,i]<-as.numeric(all[,i])
      }
    }
  }
  for(i in 1:ncol(all)){
    if(class(all[,i])=="logical"){
      all[,i]<-str_replace(all[,i], "TRUE", 1)
      all[,i]<-str_replace(all[,i], "FALSE", 0)
      all[,i]<-as.numeric(all[,i])
    }
  }
  # naを0にする
  all[is.na(all)]<-0
  require(cluster)
  temp<-c()
  teamco<-c()
  for(i in 1:ncol(all)){
    if(str_detect(names(all)[i],"0_stats.winner")){
      temp<-all[,i]
    }
    if(str_detect(names(all)[i],"9_stats.winner")){
      temp2<-all[,i]
    }
    if(str_detect(names(all)[i],"championId")){
      teamco<-cbind(teamco,all[,i])
    }
  }
  teamco<-data.frame(teamco)
  teamco1<-teamco[,c(1,2,3,4,5)]
  teamco2<-teamco[,c(6,7,8,9,10)]
  names(teamco1)<-c("1","2","3","4","5")
  names(teamco2)<-c("1","2","3","4","5")
  teamco2$winner<-temp2
  teamco2$matchno<-1:nrow(all)
  teamco1$winner<-temp
  teamco1$matchno<-1:nrow(all)
  teamco1<-rbind(teamco1,teamco2)
  # k-meansの最適解を見つける
  result <- clusGap(teamco1[,c(-6,-7)], kmeans, K.max = clusterk, B = 100, verbose = interactive())
  plot(result)
  # 一番Gap統計量が大きいクラスター数でやる
  unr<-unlist(result$Tab)
  unr<-data.frame(unr)
  unr$cluster<-row.names(unr)
  numcluster<-as.numeric(subset(unr,select="cluster",gap==max(gap)))
  res<-kmeans(teamco1[,c(-6,-7)],numcluster)
  teamco1$cluster<-res$cluster
  teamcluster<-seq(1:numcluster)
  teamcluster<-data.frame(teamcluster)
  for(i in 1:numcluster){
    teamcluster$total[i]<-nrow(subset(teamco1,teamco1$cluster==i))
    teamcluster$wins[i]<-nrow(subset(teamco1,teamco1$winner==1&teamco1$cluster==i))
  } 
  teamcluster$rate<-teamcluster$wins/teamcluster$total
  winorlose<-seq(1:nrow(all))
  winorlose<-data.frame(winorlose)
  for(i in 1:nrow(all)){
    winorlose$winner[i]<-subset(teamco1,teamco1$matchno==i & teamco1$winner==1,select="cluster")
    winorlose$loser[i]<-subset(teamco1,teamco1$matchno==i & teamco1$winner==0,select="cluster")
  }
  names(winorlose)<-c("matchno","winner","loser")
  require(trueskill)
  #時系列でやるならこことtの値が変わる
  winorlose$margin <- 1
  winorlose$Round<-as.factor(season)
  winorlose$mu1 <- NA
  winorlose$sigma1 <- NA
  winorlose$mu2 <- NA
  winorlose$sigma2 <- NA
  
  # 強さをrateで推定する。100倍する。
  for(i in 1:nrow(all)){
    winorlose$rate1[i]<-subset(teamcluster,select="rate",teamcluster==winorlose$winner[i])
    winorlose$rate2[i]<-subset(teamcluster,select="rate",teamcluster==winorlose$loser[i])
    winorlose$rate1[i]<-as.numeric(winorlose$rate1[i])*100
    winorlose$rate2[i]<-as.numeric(winorlose$rate2[i])*100
  }
  # 100を基準に初期平均値を決めて初期分散を決定する。
  winorlose[c("mu1","sigma1")] <- c(100 - as.numeric(winorlose$rate1), round(100 - as.numeric(winorlose$rate1) - ((100 - as.numeric(winorlose$rate1)) / 3), 1))
  winorlose[c("mu2","sigma2")] <- c(100 - as.numeric(winorlose$rate2), round(100 - as.numeric(winorlose$rate2) - ((100 - as.numeric(winorlose$rate2)) / 3), 1))
  
  parameters <- Parameters()
  # trueskillmodelで平均値・分散を更新する
  winorlose <- Trueskill(winorlose, parameters)
  teamcluster$rating<-as.numeric(teamcluster$rate)*100
  for(i in 1:nrow(teamcluster)){
    mu<-subset(winorlose,select="mu1",winner==i)
    sigma<-subset(winorlose,select="sigma1",winner==i)
    teamcluster$mu[i]<-mu[1,1]
    teamcluster$sigma[i]<-sigma[1,1]
  }
  # データフレームをここで何故か返す
  return(winorlose)
  return(teamco1)
  return(all)
  
  #バイオリンプロットをするために平均と分散からサンプリングする
  allsample<-c()
  for(i in 1:nrow(teamcluster)){
    sample<-rnorm(100,as.numeric(teamcluster$mu[i]),as.numeric(teamcluster$sigma[i])^(1/2))
    sample<-data.frame(sample)
    sample$cluster<-i
    allsample<-rbind(allsample,sample)
  }
  
  p<-
    ggplot(allsample,aes(x=as.factor(cluster),y=sample,colour=as.factor(cluster))) 
  p+
    geom_violin(trim=T,fill="#999999",linetype="blank",alpha=I(1/3))+
    theme(legend.position="none")+
    stat_summary(geom="pointrange",fun.y = mean, fun.ymin = function(x) mean(x)-sd(x), fun.ymax = function(x) mean(x)+sd(x), size=1,alpha=.5)
}