
# coding: utf-8

# In[5]:


from offense import Offense, OffenseResult
import csv
import sys
eps = sys.float_info.epsilon
finish_method_list = ['all', 'j', 'all_d','ed', 'rd', 'd', 'all_p', 'ep', 'rp', 'p', 't']

class FinishTendency:
    def __init__(self, number):
        self.number = number
        self.finish_details = []
        for method in finish_method_list:
            self.finish_details.append(FinishDetail(method))
        self.game_count = 0

    def add_finish(self, finish_method, result):
        if self.number != 'no' and finish_method != None:
            self.finish_details[0].add_result(result)
            self.finish_details[finish_method_list.index(finish_method)].add_result(result)

            if finish_method.endswith('d'):
                self.finish_details[finish_method_list.index('all_d')].add_result(result)
            if finish_method.endswith('p'):
                self.finish_details[finish_method_list.index('all_p')].add_result(result)
    
    def add_game_count(self):
        self.game_count += 1

class FinishDetail:
    def __init__(self, method):
        self.method = method
        self.count = 0
        self.score = 0
        self.fg_attempt = 0
        self.fg_made = 0
        self.three_attempt = 0
        self.three_made = 0
        self.foul = 0
        self.turnover = 0
        
    def add_result(self, result):
        self.count += 1
        if result == None or result == 't':
            self.turnover += 1
        else:
            offense_result = OffenseResult(result)
            if offense_result.shot_made != None:
                is_three = offense_result.shot_zone.endswith('3')
                if is_three:
                    self.three_attempt += 1
                    if offense_result.shot_made:
                        self.three_made += 1
                        self.score += 3
                self.fg_attempt += 1
                if offense_result.shot_made:
                    self.fg_made += 1
                if not is_three and offense_result.shot_made:
                    self.score += 2

            if offense_result.get_foul:
                self.foul += 1
            self.score += offense_result.free_throw_made
            
            
def add_finish_tendency(offenses, player_finish_tendency_dict):
    sorted_offenses_by_player = sorted(offenses, key=lambda offense: offense.player)
    tmp_player = FinishTendency(sorted_offenses_by_player[0].player)
    if tmp_player.number not in player_finish_tendency_dict:
        player_finish_tendency_dict[tmp_player.number] = tmp_player
    player_finish_tendency_dict[tmp_player.number].add_game_count()
    
    for offense in sorted_offenses_by_player:
        if offense.player != tmp_player.number:
            tmp_player = FinishTendency(offense.player)
            if tmp_player.number not in player_finish_tendency_dict:
                player_finish_tendency_dict[tmp_player.number] = tmp_player
            player_finish_tendency_dict[tmp_player.number].add_game_count()
        tmp_player.add_finish(offense.finish_method,  offense.result)

def write_finish_tendency(player_finish_tendency_dict):
    for player, finish_tendency in player_finish_tendency_dict.items():
        with open('#{}_finish_tendency.csv'.format(player), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['出手方式', 'PPP', '場均球權數', '場均得分', 'FG', '3PT', '場均製造犯規', '場均失誤'])
            for finish_detail in finish_tendency.finish_details:
                writer.writerow([
                    finish_detail.method,
                    round(finish_detail.score / (finish_detail.count + eps), 2),
                    finish_detail.count / finish_tendency.game_count,
                    finish_detail.score / finish_tendency.game_count,
                    '{}-{}, {:.1f}%'.format(
                        finish_detail.fg_made, 
                        finish_detail.fg_attempt, 
                        round(finish_detail.fg_made / (finish_detail.fg_attempt + eps), 3) * 100),
                    '{}-{}, {:.1f}%'.format(
                        finish_detail.three_made, 
                        finish_detail.three_attempt,
                        round(finish_detail.three_made / (finish_detail.three_attempt + eps), 3) *100),
                    finish_detail.foul / finish_tendency.game_count,
                    finish_detail.turnover / finish_tendency.game_count
                ])

