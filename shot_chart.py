
# coding: utf-8

# In[2]:


from offense import Offense, OffenseResult
import csv
import sys
eps = sys.float_info.epsilon
shot_zones_list = ['e0', 'r0', 'e1', 'm1', 'r1', 'ec2', 'e2', 'm2', 'r2', 'rc2',
                  'ec3', 'e3', 'm3', 'r3', 'rc3']
class ShotChartOverview:
    def __init__(self, number):
        self.number = number
        self.shot_zones_attempt = [0] * 15
        self.shot_zones_made = [0] * 15
        
    def result_to_shot_chart_overview(self, result):
        if result != 't':
            offense_result = OffenseResult(result)
            if offense_result.shot_made != None:
                self.shot_zones_attempt[shot_zones_list.index(offense_result.shot_zone)] += 1
                if offense_result.shot_made:
                    self.shot_zones_attempt[shot_zones_list.index(offense_result.shot_zone)] += 1

def add_shot_chart_overview(offenses, shot_chart_overview_dict):
    sorted_offenses_by_player = sorted(offenses, key=lambda offense: offense.player)
    tmp_shot_chart = ShotChartOverview(sorted_offenses_by_player[0].player)
    if tmp_shot_chart.number not in shot_chart_overview_dict:
        shot_chart_overview_dict[tmp_shot_chart.number] = tmp_shot_chart    
    
    for offense in sorted_offenses_by_player:
        if offense.player != tmp_shot_chart.number:
            tmp_shot_chart = ShotChartOverview(offense.player)
            if tmp_shot_chart.number not in shot_chart_overview_dict:
                shot_chart_overview_dict[tmp_shot_chart.number] = tmp_shot_chart
        if offense.result != None:
            shot_chart_overview_dict[tmp_shot_chart.number].result_to_shot_chart_overview(offense.result)

def write_shot_chart_overview(player_overview_dict, shot_chart_overview_dict):
    with open('shot_chart_overview.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['區域', '左側禁區', '右側禁區', '左側近距', '中間近距', 
                         '右側近距', '左底中距', '左翼中距', '弧頂中距', '右翼中距', '右底中距',
                         '左底三分', '左翼三分', '弧頂三分', '右翼三分', '右底三分', 
                         'FG', '3PT', 'PPP', '球權數'])
        writer.writerow(['代號'] + shot_zones_list + ['', '', '', ''] )
        for player, player_overview in player_overview_dict.items():
            if player == 'no' or player not in shot_chart_overview_dict:
                continue
            player_shot_chart_list = [player]
            for i in range(len(shot_zones_list)):
                player_shot_chart_list.append('{}-{}, {}%'.format(
                    shot_chart_overview_dict[player].shot_zones_made[i],
                    shot_chart_overview_dict[player].shot_zones_attempt[i],
                    round(shot_chart_overview_dict[player].shot_zones_made[i] / 
                    (shot_chart_overview_dict[player].shot_zones_attempt[i] + eps), 2)
                ))
            player_shot_chart_list += [
                '{}-{}, {:.1f}%'.format(
                        player_overview.fg_made, 
                        player_overview.fg_attempt, 
                        round(player_overview.fg_made / (player_overview.fg_attempt + eps), 3)*100),
                '{}-{}, {:.1f}%'.format(
                        player_overview.three_made, 
                        player_overview.three_attempt,
                        round(player_overview.three_made / (player_overview.three_attempt + eps), 3)*100),
                round(player_overview.score / player_overview.offense_count, 2),
                player_overview.offense_count
            ]
            writer.writerow(player_shot_chart_list)
        

