"""
Scaled down version of this: https://github.com/mcatovic/Automated_NHL_Goal_Light

"""

import requests
import json

api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'

def get_scores(team=None, printout=True, current_only=False):
    """
    Gather score data.  Returns list of dictionaries for each game.
    
    @param:
    team:           Team to filter for, if no team specified, 
                    all available scores provided.
    printout:       Option to print out game data
    current_only:   Filters out any games that are not live.
    """
    r = False
    results = []
    while not r:
        try:
            r = requests.get(api_url) #making sure there is a connection with the API
        except (requests.ConnectionError): #Catch these errors
            print ("Could not get response from NHL.com trying again...")
            time.sleep(5)
            continue

    text = r.text.replace('loadScoreboard(', '').replace(')','')
    data = json.loads(text)
    
    for game in data['games']:
        if team and team not in [game['atn'], game['htn']]:
            pass
        else:
            game_result = {}
            game_result['Date'] = game['ts']
            game_result['Status'] = game['bs']
            game_result['Away Team'] = game['atn']
            game_result['Away Goals'] = game['ats']
            game_result['Home Team'] = game['htn']
            game_result['Home Goals'] = game['hts']

            if current_only and game_Result['Status'] != 'Live':
                pass
            else:
                results.append(game_result)   
            
            if printout:
                print 'Date ', game_result['Date']
                print game_result['Status']
                print 'Away Team: ',game_result['Away Team']
                print game_result['Away Goals']
                print 'Home Team: ',game_result['Home Team']
                print game_result['Home Goals']                
                print ' --------------------'

    
    return results

class GameSession():
    """
    Game session class used to store non-changing game data.
    """
    def __init__(self, team):
        self.team_type = ''
        self.live = False

        while not self.live:
            data = get_scores(team=team, printout=False, current_only=True)
            if data:
                self.live = True

        if team in data['Home Team']:
            self.team_type = 'Home'
        if team in data['Away Team']:
            self.team_type = 'Away'

        while self.live:
            self.announce_goal()
            

    def announce_goal(self, interval=5):
        """
        Check if current goal count has increased.  
        Do something special if it has.
        """
        if self.live:
            data = get_scores(team=self.team, printout=False, current_only=True)
            if data:
                goals = data['%s Goals'][0]
                if goals > previous_goals:
                    print 'GOOOOAAAALLLLL!!!'
                else:
                    print goals
                previous_goals = goals
                time.sleep(5)
            else:
                print 'Game Over!'
                self.live = False

GS = GameSession('Vancouver')            