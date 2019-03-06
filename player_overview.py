
# coding: utf-8

# In[9]:


from offense import Offense, OffenseResult
import sys
import csv
eps = sys.float_info.epsilon
class PlayerOverview:
    def __init__(self, number):
        self.number = number
        self.offense_count = 0
        self.score = 0
        self.fg_attempt = 0
        self.fg_made = 0
        self.three_attempt = 0
        self.three_made = 0
        self.foul = 0
        self.turnover = 0
        self.assist = 0
        self.game_count = 0
    
    def parse_offense(self, offense, player_overview_dict):
        self.offense_count += 1
        if (offense.detail_offense_mode == 't'
            or offense.result == 't'
            or offense.finish_method == 't'
            or offense.main_offense_mode == 'ft'):
            self.turnover += 1
        else:
            print(offense)
            self.result_to_player_overview(offense.result)
        
        if self.number == 'no':
            if offense.other != None:
                if offense.other not in player_overview_dict:
                    player_overview_dict[offense.other] = PlayerOverview(offense.other)
                    player_overview_dict[offense.other].add_game_count()
                player_overview_dict[offense.other].turnover += 1
                player_overview_dict[offense.other].offense_count += 1
        elif offense.detail_offense_mode != 'b':
            if offense.other != None:
                if offense.other not in player_overview_dict:
                    player_overview_dict[offense.other] = PlayerOverview(offense.other)
                player_overview_dict[offense.other].assist += 1
    
    def result_to_player_overview(self, result):
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
    
    def add_game_count(self):
        self.game_count += 1
        
def add_player_overview(offenses, player_overview_dict):
    sorted_offenses_by_player = sorted(offenses, key=lambda offense: offense.player)
    tmp_player = PlayerOverview(sorted_offenses_by_player[0].player)
    if tmp_player.number not in player_overview_dict:
        player_overview_dict[tmp_player.number] = tmp_player
    player_overview_dict[tmp_player.number].add_game_count()
    
    for offense in sorted_offenses_by_player:
        if offense.player != tmp_player.number:
            tmp_player = PlayerOverview(offense.player)
            if tmp_player.number not in player_overview_dict:
                player_overview_dict[tmp_player.number] = tmp_player
            player_overview_dict[tmp_player.number].add_game_count()
        player_overview_dict[tmp_player.number].parse_offense(offense,  player_overview_dict)

def write_player_overview(player_overview_dict):
    with open('player_overview.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(['背號', 'PPP', '場均球權數', '場均得分數', 'FG', '3PT', '場均製造犯規', '場均失誤', '場均助攻'])
        for player, player_overview in player_overview_dict.items():
            if player == 'no':
                continue
            writer.writerow([
                player, 
                round(player_overview.score / player_overview.offense_count, 2),
                player_overview.offense_count / player_overview.game_count,
                player_overview.score / player_overview.game_count,
                '{}-{}, {:.1f}%'.format(
                    player_overview.fg_made, 
                    player_overview.fg_attempt, 
                    round(player_overview.fg_made / (player_overview.fg_attempt + eps), 3) * 100),
                '{}-{}, {:.1f}%'.format(
                    player_overview.three_made, 
                    player_overview.three_attempt,
                    round(player_overview.three_made / (player_overview.three_attempt + eps), 3) * 100),
                player_overview.foul / player_overview.game_count,
                player_overview.turnover / player_overview.game_count,
                player_overview.assist / player_overview.game_count
            ])

