"""
Scaled down version of this: https://github.com/mcatovic/Automated_NHL_Goal_Light

"""

import requests
import json
import time
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
    data = {}
    while not r:
        try:
            r = requests.get(api_url) #making sure there is a connection with the API
        except (requests.ConnectionError): #Catch these errors
            print ("Could not get response from NHL.com trying again...")
            time.sleep(5)
            continue

    text = r.text.replace('loadScoreboard(', '').replace(')','')
    # print text
    try:
        data = json.loads(text)
    except:
        print data
        print "Could not parse json data, trying again.."
        results.append('invalid')

    if data:
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

                if current_only and game_result['Status'] != 'LIVE':
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
        print "Game Session started!"
        self.team = team
        self.team_type = ''
        self.live = False
        self.current_goal_count = 1

        while not self.live:
            print "Waiting for game to start..."
            data = get_scores(team=team, printout=True)[0]
            if data['Status'] == 'LIVE':
                print "Game On!"
                self.live = True
            time.sleep(5)    

        if team in data['Home Team']:
            self.team_type = 'Home'
        if team in data['Away Team']:
            self.team_type = 'Away'

        while self.live:
            self.check_for_goal()
            

    def check_for_goal(self, interval=5):
        """
        Check if current goal count has increased.  
        Do something special if it has.
        """
        print "Updating...."

        if self.live:
            data = get_scores(team=self.team, printout=False, current_only=True)

            if data[0] == 'invalid':
                pass
            else:
                if data:
                    goals = data[0]['%s Goals' % self.team_type][0]                
                    if goals > self.current_goal_count:
                        print 'GOOOOAAAALLLLL!!!'
                    else:
                        print goals
                    self.current_goal_count = goals
                    time.sleep(5)
                else:
                    print 'Game Over!'
                    self.live = False

GS = GameSession('Colorado')            