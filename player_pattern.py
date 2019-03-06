
# coding: utf-8

# In[2]:


from offense import Offense, OffenseResult
import csv
import sys
eps = sys.float_info.epsilon

pattern_list = ['all',
                'i',
                'f all', 'f lo', 'f bh', 'f w', 'f tr', 'f bc', 
                'pr b', 'pr m all', 'pr m r', 'pr m s', 'pr m p',
                'ho b', 'ho m all', 'ho m r', 'ho m p', 
                'w b', 'w m all', 'w m r', 'w m p', 
                'su',
                'os',
                'c',
                'pb', 
                'pu all', 'pu lp', 'pu sf', 'pu hl'
                'hs', 
                'ft', 
                'o']


# In[3]:


class PlayerPattern:
    def __init__(self, number):
        self.number = number
        self.pattern_details = []
        for pattern in pattern_list:
            self.pattern_details.append(PatternDetail(pattern))
        self.game_count = 0

    def add_pattern(self, main_offense, detail_offense, result):
        offense_pattern = main_offense
        if detail_offense != None:
            offense_pattern += (' ' + detail_offense)
       
        if self.number != 'no' and offense_pattern != None:
            self.pattern_details[0].add_result(result)
            if offense_pattern in pattern_list:
                self.pattern_details[pattern_list.index(offense_pattern)].add_result(result)
                if offense_pattern.startswith('f'):
                    self.pattern_details[pattern_list.index('f all')].add_result(result)
                if offense_pattern.startswith('pr m'):
                    self.pattern_details[pattern_list.index('pr m all')].add_result(result)
                if offense_pattern.startswith('ho m'):
                    self.pattern_details[pattern_list.index('ho m all')].add_result(result)
                if offense_pattern.startswith('pu'):
                    self.pattern_details[pattern_list.index('pu all')].add_result(result)
    def add_game_count(self):
        self.game_count += 1


# In[4]:


class PatternDetail:
    def __init__(self, pattern):
        self.pattern = pattern
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


# In[5]:


def add_player_pattern(offenses, player_pattern_dict):
    sorted_offenses_by_player = sorted(offenses, key=lambda offense: offense.player)
    tmp_player = PlayerPattern(sorted_offenses_by_player[0].player)
    if tmp_player.number not in player_pattern_dict:
        player_pattern_dict[tmp_player.number] = tmp_player
    player_pattern_dict[tmp_player.number].add_game_count()
    
    for offense in sorted_offenses_by_player:
        if offense.player != tmp_player.number:
            tmp_player = PlayerPattern(offense.player)
            if tmp_player.number not in player_pattern_dict:
                player_pattern_dict[tmp_player.number] = tmp_player
            player_pattern_dict[tmp_player.number].add_game_count()
        player_pattern_dict[tmp_player.number].add_pattern(
            offense.main_offense_mode, 
            offense.detail_offense_mode,  
            offense.result
        )
        player_pattern_dict['team'].add_pattern(
            offense.main_offense_mode, 
            offense.detail_offense_mode,  
            offense.result
        )


# In[6]:


def write_player_pattern(player_pattern_dict):
    for player, player_pattern in player_pattern_dict.items():
        if player == 'team':
            continue
        with open('#{}_player_pattern.csv'.format(player), 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['進攻模式', 'PPP', '場均球權數', '場均得分', 'FG', '3PT', '場均製造犯規', '場均失誤'])
            for pattern_detail in player_pattern.pattern_details:
                writer.writerow([
                    pattern_detail.pattern,
                    round(pattern_detail.score / (pattern_detail.count + eps), 2),
                    pattern_detail.count / player_pattern.game_count,
                    pattern_detail.score / player_pattern.game_count,
                    '{}-{}, {:.1f}%'.format(
                        pattern_detail.fg_made, 
                        pattern_detail.fg_attempt, 
                        round(pattern_detail.fg_made / (pattern_detail.fg_attempt + eps), 3) * 100),
                    '{}-{}, {:.1f}%'.format(
                        pattern_detail.three_made, 
                        pattern_detail.three_attempt,
                        round(pattern_detail.three_made / (pattern_detail.three_attempt + eps), 3) * 100),
                    pattern_detail.foul / player_pattern.game_count,
                    pattern_detail.turnover / player_pattern.game_count
                ])


# In[ ]:


def write_team_pattern(player_pattern):
    with open('team_pattern.csv', 'w+') as f:
            writer = csv.writer(f)
            writer.writerow(['進攻模式', 'PPP', '場均球權數', '場均得分', 'FG', '3PT', '場均製造犯規', '場均失誤'])
            for pattern_detail in player_pattern.pattern_details:
                writer.writerow([
                    pattern_detail.pattern,
                    round(pattern_detail.score / (pattern_detail.count + eps), 2),
                    pattern_detail.count / player_pattern.game_count,
                    pattern_detail.score / player_pattern.game_count,
                    '{}-{}, {:.1f}%'.format(
                        pattern_detail.fg_made, 
                        pattern_detail.fg_attempt, 
                        round(pattern_detail.fg_made / (pattern_detail.fg_attempt + eps), 3) * 100),
                    '{}-{}, {:.1f}%'.format(
                        pattern_detail.three_made, 
                        pattern_detail.three_attempt,
                        round(pattern_detail.three_made / (pattern_detail.three_attempt + eps), 3) * 100),
                    pattern_detail.foul / player_pattern.game_count,
                    pattern_detail.turnover / player_pattern.game_count
                ])

