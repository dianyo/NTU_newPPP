
# coding: utf-8

# In[1]:


from offense import Offense, OffenseResult
import csv
import sys
eps = sys.float_info.epsilon
ball_source_list = ['all', 'dk', 'f', 'ii', 'io', 'hl', 'hp', 'pr',
                                'apr', 'ho', 'aho', 'w', 'aw', 'pu']

class CourtVision:
    def __init__(self, number):
        self.number = number
        self.court_details = []
        for ball_source in ball_source_list:
            self.court_details.append(CourtDetail(ball_source))
        self.game_count = 0
    
    def add_court(self, ball_source, result, other, player_court_vision_dict):
        if ball_source != None and other != None:
            if other not in player_court_vision_dict:
                player_court_vision_dict[other] = CourtVision(other)
                player_court_vision_dict[other].add_game_count()
            player_court_vision_dict[other].court_details[0].add_result(result)
            if ball_source in ball_source_list:
                player_court_vision_dict[other].court_details[ball_source_list.index(ball_source)].add_result(result)    
    def add_game_count(self):
        self.game_count += 1


# In[2]:


class CourtDetail:
    def __init__(self, ball_source):
        self.ball_source = ball_source
        self.count = 0
        self.assist_count = 0
        self.turnover = 0
        
    def add_result(self, result):
        self.count += 1
        if result == 't':
            self.turnover += 1
        else:
            offense_result = OffenseResult(result)
            if offense_result.shot_made:
                self.assist_count += 1


# In[ ]:


def add_court_vision(offenses, player_court_vision_dict):
    sorted_offenses_by_player = sorted(offenses, key=lambda offense: offense.player)
    tmp_player = CourtVision(sorted_offenses_by_player[0].player)
    if tmp_player.number not in player_court_vision_dict:
        player_court_vision_dict[tmp_player.number] = tmp_player
    player_court_vision_dict[tmp_player.number].add_game_count()
    
    for offense in sorted_offenses_by_player:
        if offense.player != tmp_player.number:
            tmp_player = CourtVision(offense.player)
            if tmp_player.number not in player_court_vision_dict:
                player_court_vision_dict[tmp_player.number] = tmp_player
            player_court_vision_dict[tmp_player.number].add_game_count()
        player_court_vision_dict[tmp_player.number].add_court(offense.ball_source,  offense.result, offense.other, player_court_vision_dict)


# In[5]:


def write_court_vision(player_court_vision_dict):
    for player, court_vision in player_court_vision_dict.items():
        with open('#{}_court_vision.csv'.format(player), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['傳球型態', '場均球權數', '場均助攻', '場均失誤', '失誤助攻比'])
            for court_detail in court_vision.court_details:
                writer.writerow([
                    court_detail.ball_source,
                    court_detail.count / court_vision.game_count,
                    court_detail.assist_count / court_vision.game_count,
                    court_detail.turnover / court_vision.game_count,
                    round(court_detail.assist_count / (court_detail.turnover + eps), 2)
                ])

