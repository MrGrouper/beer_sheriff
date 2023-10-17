from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
from espn import getMatchups

# connect to yahoo api
sc = OAuth2(None, None, from_file='oauth2.json')

#get game object

gm = yfa.Game(sc, 'nfl')
leagues = gm.league_ids()
lg = gm.to_league('423.l.46423')
# current_week = lg.current_week()
current_week = '4'
tms = lg.teams()
team_keys = tms.keys()

def main():
    print(checkZero(makeTeams()))

#output list of teams by id with team name and roster
    #roster has player id, and selected position
def checkZero(teamList):
    list = []
    for team in teamList:
        for player in team["roster"]:
            print(player["playerName"], player['playerPoints'])
            if player["gameCompleted"] == "True" and player["playerPoints"] <= 0:
                    list.append({"team": player["teamName"],
                    "player": player["playerName"]})
    return list

        
def makeTeams():
    teamList = []
    for team_key in team_keys:
        team = lg.to_team(team_key)
        roster = team.roster(week = current_week)
        teamDict = {
            "teamID": tms[team_key]["team_id"],
            "teamName": tms[team_key]["name"],
            "roster": makeRoster(roster)
            }


        teamList.append(teamDict)
    return teamList

def getPlayerTeam(playerId):
    try:
        details = lg.player_details(int(playerId))
        team = details[0]["editorial_team_abbr"]
        return(team.upper())
    except RuntimeError:
        print(playerId)

def makeRoster(roster):
    rosterList = []
    for player in roster:
        playerName = player["name"]
        playerId = player['player_id']
        playerPos = player["selected_position"]
        playerGameStatus = checkGameComplete(playerId)
        playerPoints = calculatePoints(playerId, playerPos, playerGameStatus[2])
        dict = {
            "playerID": playerId,
            "playerName": playerName,
            "selectedPosition": playerPos,
            "playerTeam": playerGameStatus[0],
            "gameCompleted": playerGameStatus[2],
            "datePlayed": playerGameStatus[1],
            "playerPoints": playerPoints
        }
        rosterList.append(dict)
    return rosterList



def checkGameComplete(playerId):
    matchups = getMatchups(current_week)
    playerTeam = getPlayerTeam(playerId)
    for matchup in matchups:
        if playerTeam in matchup["NFLteams"]:
            return [playerTeam, matchup['date'], str(matchup["completed"])]
    return [playerTeam, 'bye', "False"]

def calculatePoints(playerId, playerPos, playerGameStatus):
    
    if playerPos == 'BN' or playerPos == "IR" or playerGameStatus == 'False':
        return 1
    else:
        if playerPos == 'DEF':
            return defPoints(playerId)
        elif playerPos == 'K':
            return kPoints(playerId)
        else: return wrtPoints(playerId)

def wrtPoints(playerId):
    stats = lg.player_stats(playerId, "week", week = current_week)
    passYds = stats[0]["Pass Yds"]/25
    passTDs = stats[0]['Pass TD'] * 6
    intercept = stats[0]["Int"] * (-2)
    rushYds = stats[0]["Rush Yds"]/10
    rushTds = stats[0]["Rush TD"] * 6
    rec = stats[0]["Rec"]
    recYds = stats[0]["Rec Yds"]/10
    recTds = stats[0]["Rec TD"]*6
    retTds = stats[0]["Ret TD"]*6
    twoPt = stats[0]["2-PT"] * 2
    fum = stats[0]["Fum Lost"]*(-2)
    fumRet = stats[0]["Fum Ret TD"]*6

    return(passYds+passTDs+intercept+rushYds+rushTds+rec+recYds+recTds+retTds+twoPt+fum+fumRet)

def kPoints(playerId):
    stats = lg.player_stats(playerId, "week", week = current_week)
    FG019 = stats[0]["FG 0-19"] * 3
    FG2029 = stats[0]["FG 20-29"] * 3
    FG3039 = stats[0]["FG 30-39"] * 3
    FG4049 =stats[0]["FG 40-49"] * 4
    FG50 = stats[0]["FG 50+"] * 5
    pat = stats[0]["PAT Made"]

    return(FG019+FG2029+FG3039+FG4049+FG50+pat)

def defPoints(playerId):
    stats = lg.player_stats(playerId, "week", week = current_week)
    sack = stats[0]["Sack"]
    int = stats[0]["Int"]*2
    fum = stats[0]["Fum Rec"]*2
    td = stats[0]["TD"] * 6
    safe = stats[0]["Safe"]*2
    blk = stats[0]["Blk Kick"]*2
    retTd = stats[0]["Ret TD"] *6
    pt0 = stats[0]['Pts Allow 0'] * 15
    pt16 = stats[0]['Pts Allow 1-6']*10
    pt713 = stats[0]['Pts Allow 7-13']*7
    pt1420 = stats[0]['Pts Allow 14-20']*4
    pt2127 = stats[0]['Pts Allow 21-27']*0
    pt2834 = stats[0]['Pts Allow 28-34']*(-1)
    pt35 = stats[0]['Pts Allow 35+']*(-4)
    xpr = stats[0]["XPR"]* 2

    return(sack+int+fum+td+safe+blk+retTd+pt0+pt16+pt713+pt1420+pt2127+pt2834+pt35+xpr)
    



main()
# print(lg.player_stats(27277, "week", week = current_week))
# print(lg.player_stats(27369, "week", week = current_week))
# print(lg.player_stats(100030, "week", week = current_week))
# print(lg.player_stats(30123, "week", week = current_week))

# print(lg.settings())


