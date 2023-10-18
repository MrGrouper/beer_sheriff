import json 
import requests

def main():
    print(getMatchups(6))


def getMatchups(week):
    response = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard')
    o = response.json()
    matchups = []
    for event in o["events"]:
        if event["week"]["number"] == week:
            dict = {
                "date": event["date"],
                "NFLteams": getTeams(event),
                "completed": event["competitions"][0]["status"]["type"]["completed"]
            }
            matchups.append(dict)
    return(matchups)

def getTeams(event: dict):
    teams = []
    comps = event["competitions"][0]["competitors"]
    for comp in comps:
        teams.append(comp["team"]["abbreviation"].upper())
    return(teams)


#prints event for reference 
def printRef():
    for event in o["events"]:
        if event["shortName"] == "SEA @ CIN":
            print(json.dumps(event, indent=2))

if __name__ == "__main__":
    main()
